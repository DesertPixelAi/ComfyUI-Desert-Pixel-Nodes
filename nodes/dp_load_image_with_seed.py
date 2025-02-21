import os
import torch
import numpy as np
import cv2
from PIL import Image, ImageOps
import folder_paths
from .image_effects import ImageEffects
import comfy.utils
import json

class DP_Load_Image_With_Seed:
    def __init__(self):
        self.effects = ImageEffects()
        
        # Effects with no parameters (simple on/off)
        self.BASIC_EFFECTS = {
            "original", "grayscale", "enhance", "flip_h",
            "flip_v", "rotate_90_ccw", "rotate_180", "rotate_270_ccw",
            "edge_detect", "edge_gradient", "lineart_anime"
        }

        # Effects that need strength parameter
        self.STRENGTH_EFFECTS = {
            "posterize": lambda strength: max(2, int(8 - (strength * 6))),
            "sharpen": lambda strength: strength * 2.0,
            "sepia": lambda strength: strength,
            "blur": lambda strength: strength * 10.0,
            "emboss": lambda strength: strength * 2.0,
            "palette": lambda strength: max(2, int(32 - (strength * 30))),
            "solarize": lambda strength: 1.0 - strength,
            "denoise": lambda strength: max(1, int(strength * 5)),
            "vignette": lambda strength: strength,
            "glow_edges": lambda strength: strength,
            "threshold": lambda strength: strength,
            "contrast": lambda strength: 0.5 + (strength * 1.5),
            "equalize": lambda strength: strength
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

    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = []
        for filename in os.listdir(input_dir):
            if filename.endswith(('.png', '.jpg', '.jpeg', '.webp')):
                files.append(filename)

        available_styles = [
            "original", "grayscale", "enhance", "flip_h",
            "flip_v", "rotate_90_ccw", "rotate_180", "rotate_270_ccw",
            "posterize", "sharpen", "contrast",
            "equalize", "sepia", "blur", "emboss", "palette",
            "solarize", "denoise", "vignette", "glow_edges",
            "edge_detect", "edge_gradient", "lineart_anime",
            "threshold"
        ]
        
        return {"required": {
            "image": (sorted(files), {"image_upload": True}),
            "effect_strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
            "effect_A": (available_styles, {"default": "original"}),
            "effect_B": (available_styles, {"default": "original"}),
            "resize_image": ("BOOLEAN", {"default": True}),
            "width": ("INT", {"default": 1024, "min": 64, "max": 2048, "step": 8}),
            "height": ("INT", {"default": 1024, "min": 64, "max": 2048, "step": 8}),
        }}

    def apply_effect(self, effect_name, image, strength):
        if effect_name in self.BASIC_EFFECTS:
            return getattr(self.effects, effect_name)(image)
        elif effect_name in self.STRENGTH_EFFECTS:
            mapped_strength = self.STRENGTH_EFFECTS[effect_name](strength)
            return getattr(self.effects, effect_name)(image, mapped_strength)
        return image

    def load_image_and_process(self, image, effect_strength, effect_A, effect_B, 
                             resize_image, width, height):
        prompt_text = ""
        negative_text = ""
        seed = 0
        
        # Process uploaded image
        image_path = folder_paths.get_annotated_filepath(image)
        formatted_name = os.path.splitext(os.path.basename(image_path))[0]
        
        try:
            with Image.open(image_path) as img:
                img = ImageOps.exif_transpose(img)
                # Extract seed and prompt before any processing
                seed, prompt_text = self.extract_seed_and_prompt(img)
                if img.mode == 'I':
                    img = img.point(lambda i: i * (1 / 255))
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                image = np.array(img).astype(np.float32) / 255.0
                uploaded_image = torch.from_numpy(image).unsqueeze(0)
                negative_text = img.info.get('dp_negative_or_other', '')
        except Exception as e:
            print(f"Error processing image: {e}")
            raise e

        # Resize uploaded image only if resize_image is True
        if resize_image:
            try:
                width = int(width) if width != "image" else image.shape[2]
                height = int(height) if height != "image" else image.shape[1]
            except (ValueError, AttributeError) as e:
                print(f"[Python] Error converting dimensions: {str(e)}")
                if hasattr(image, 'shape'):
                    width = image.shape[2]
                    height = image.shape[1]
                else:
                    raise ValueError("Invalid image or dimensions provided")

            samples = uploaded_image.movedim(-1,1)
            resized = comfy.utils.common_upscale(samples, width, height, "lanczos", "center")
            uploaded_image = resized.movedim(1,-1)

        # Process uploaded image with both effects
        image_A = self.apply_effect(effect_A, uploaded_image, effect_strength)
        image_B = self.apply_effect(effect_B, uploaded_image, effect_strength)

        return (image_A, image_B, formatted_name, prompt_text, negative_text, seed)

    @classmethod
    def IS_CHANGED(s, image, effect_strength=1.0, effect_A="original", effect_B="original", 
                  resize_image=True, width=1024, height=1024):
        image_path = folder_paths.get_annotated_filepath(image)
        return f"{image_path}_{effect_strength}_{effect_A}_{effect_B}_{resize_image}_{width}_{height}"

    @classmethod
    def VALIDATE_INPUTS(s, image, *args, **kwargs):
        if not folder_paths.exists_annotated_filepath(image):
            return "Invalid image file: {}".format(image)
        return True

    RETURN_TYPES = ("IMAGE", "IMAGE", "STRING", "STRING", "STRING", "INT")
    RETURN_NAMES = ("image_A", "image_B", "filename", "dp_prompt", "dp_negative_or_other", "seed")
    FUNCTION = "load_image_and_process"
    CATEGORY = "DP/image" 