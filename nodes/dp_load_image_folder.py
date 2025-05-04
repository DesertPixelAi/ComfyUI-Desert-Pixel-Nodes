import os
import json
import numpy as np
import torch
from PIL import Image, ImageOps, PngImagePlugin
import folder_paths
from comfy.k_diffusion.utils import FolderOfImages
from comfy.utils import common_upscale
from server import PromptServer
import random

class DP_Load_Image_Folder:
    def __init__(self):
        self.current_index = 0
        self.id = str(random.randint(0, 2**64))
        self.color = "#121317"  # Default DP Ocean title color
        self.bgcolor = "#006994"  # Default DP Ocean body color

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "directory": ("STRING", {"placeholder": "X://path/to/images", "vhs_path_extensions": []}),
                "image_load_cap": ("INT", {"default": 1, "min": 1, "max": 10000, "step": 1}),
                "skip_first_images": ("INT", {"default": 0, "min": 0, "max": 10000, "step": 1}),
                "Cycler_Mode": (["increment", "decrement", "randomize", "fixed"],),
                "index": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "resize_image": ("BOOLEAN", {"default": True}),
                "width": ("INT", {"default": 1024, "min": 64, "max": 2048, "step": 8}),
                "height": ("INT", {"default": 1024, "min": 64, "max": 2048, "step": 8}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID"
            },
        }

    def extract_prompt_from_workflow(self, workflow_data):
        try:
            # Look through all nodes in the workflow
            for node in workflow_data.values():
                if isinstance(node, dict) and 'class_type' in node:
                    # Look for CLIP Text Encode nodes
                    if node['class_type'] == 'CLIPTextEncode':
                        # Check if it's a positive prompt (not negative)
                        if 'inputs' in node and 'text' in node['inputs']:
                            title = node.get('_meta', {}).get('title', '')
                            # Make sure it's not a negative prompt
                            if 'negative' not in title.lower():
                                return node['inputs']['text']
        except:
            pass
        return None

    def extract_seed_and_prompt(self, img):
        seed = 0
        prompt = ""
        try:
            metadata = img.info
            for key in metadata:
                try:
                    # First check for DP-style prompt
                    if key.lower() == 'dp_prompt':
                        prompt = metadata[key]
                        continue

                    # Try to parse JSON data
                    data = json.loads(metadata[key])
                    
                    # Handle workflow data for seed and ComfyUI-style prompt
                    if isinstance(data, dict):
                        # Look for seed in nodes
                        if 'nodes' in data:
                            for node in data['nodes']:
                                if 'type' in node and 'widgets_values' in node:
                                    if any(sampler in node['type'].lower() for sampler in ['sampler', 'dp advanced sampler']):
                                        if node['widgets_values'] and isinstance(node['widgets_values'][0], (int, float)):
                                            seed = int(node['widgets_values'][0])
                        
                        # If no DP-style prompt was found, look for ComfyUI-style prompt
                        if not prompt:
                            workflow_prompt = self.extract_prompt_from_workflow(data)
                            if workflow_prompt:
                                prompt = workflow_prompt

                except:
                    continue
        except:
            pass
        return seed, prompt

    def load_image_and_process(self, directory, image_load_cap, skip_first_images, Cycler_Mode, index, resize_image, width, height, unique_id):
        if not os.path.isdir(directory):
            raise FileNotFoundError(f"Directory '{directory}' cannot be found.")

        # Convert set to tuple for endswith
        img_extensions = tuple(FolderOfImages.IMG_EXTENSIONS)
        
        all_files = sorted([os.path.join(directory, f) for f in os.listdir(directory) 
                          if f.lower().endswith(img_extensions)])
        
        if len(all_files) == 0:
            raise FileNotFoundError(f"No valid images found in directory: {directory}")

        # Handle cycling logic
        total_images = len(all_files)
        next_index = self.current_index

        # Detect changes
        index_changed = index != self.current_index

        # Handle cycling modes
        if Cycler_Mode == "fixed":
            if index_changed:
                next_index = max(0, min(index, total_images - image_load_cap))
                self.current_index = next_index
        elif Cycler_Mode == "randomize":
            while True:
                next_index = random.randint(0, total_images - image_load_cap)
                if next_index != self.current_index or total_images <= image_load_cap:
                    break
            self.current_index = next_index
        elif Cycler_Mode == "increment":
            next_index = (self.current_index + 1) % (total_images - image_load_cap + 1)
            self.current_index = next_index
        elif Cycler_Mode == "decrement":
            next_index = (self.current_index - 1) % (total_images - image_load_cap + 1)
            self.current_index = next_index

        # Update UI
        try:
            PromptServer.instance.send_sync("update_node", {
                "node_id": unique_id,
                "index_value": self.current_index,
                "widget_name": "index",
                "force_widget_update": True,
                "color": self.color,
                "bgcolor": self.bgcolor
            })
        except Exception as e:
            print(f"Error sending WebSocket message: {str(e)}")

        # Get the files for this batch
        dir_files = all_files[self.current_index:self.current_index + image_load_cap]

        # First pass to determine most common size and check for alpha
        sizes = {}
        has_alpha = False
        for image_path in dir_files:
            with Image.open(image_path) as i:
                i = ImageOps.exif_transpose(i)
                has_alpha |= 'A' in i.getbands()
                count = sizes.get(i.size, 0)
                sizes[i.size] = count + 1

        target_size = max(sizes.items(), key=lambda x: x[1])[0]
        if resize_image:
            target_size = (width, height)

        # Load and process all images
        images = []
        prompts = []
        negatives = []
        seeds = []
        filenames = []

        for image_path in dir_files:
            try:
                with Image.open(image_path) as img:
                    img = ImageOps.exif_transpose(img)
                    
                    # Extract metadata using the same method as dp_load_image_with_seed
                    seed, prompt = self.extract_seed_and_prompt(img)
                    negative = img.info.get('dp_negative_or_other', '')
                    filename = os.path.splitext(os.path.basename(image_path))[0]
                    
                    # Convert image
                    if img.mode == 'I':
                        img = img.point(lambda i: i * (1 / 255))
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    image = np.array(img).astype(np.float32) / 255.0
                    image = torch.from_numpy(image)[None,...]
                    
                    if image.shape[-2] != target_size[1] or image.shape[-3] != target_size[0]:
                        image = image.movedim(-1, 1)
                        image = common_upscale(image, target_size[0], target_size[1], "lanczos", "center")
                        image = image.movedim(1, -1)
                    
                    images.append(image)
                    prompts.append(prompt)
                    negatives.append(negative)
                    seeds.append(seed)
                    filenames.append(filename)

            except Exception as e:
                print(f"Error processing {image_path}: {e}")
                continue

        if not images:
            raise ValueError("No images could be processed successfully")

        # Stack all images
        images = torch.cat(images, dim=0)
        
        # Create masks
        masks = torch.zeros((images.size(0), target_size[1], target_size[0]), dtype=torch.float32)

        # Join text fields with newlines
        combined_prompt = "\n".join(filter(None, prompts))
        combined_negative = "\n".join(filter(None, negatives))
        combined_filename = "\n".join(filenames)
        
        # Use first seed or 0
        seed = seeds[0] if seeds else 0

        return (images, masks, combined_filename, combined_prompt, combined_negative, seed, images.size(0))

    @classmethod
    def IS_CHANGED(s, directory, **kwargs):
        if not os.path.isdir(directory):
            return "directory_not_found"
        return float("NaN")  # Always update to allow cycling

    @classmethod
    def VALIDATE_INPUTS(s, directory, **kwargs):
        if not os.path.isdir(directory):
            return f"Directory '{directory}' cannot be found."
        return True

    RETURN_TYPES = ("IMAGE", "MASK", "STRING", "STRING", "STRING", "INT", "INT")
    RETURN_NAMES = ("images", "masks", "filename", "dp_prompt", "dp_negative_or_other", "seed", "frame_count")
    FUNCTION = "load_image_and_process"
    CATEGORY = "DP/image" 