import os
import torch
import numpy as np
from PIL import Image, PngImagePlugin
import folder_paths
from pathlib import Path
import re
import json
from server import PromptServer

class DP_Save_Preview_Image:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 4

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mode": (["SAVE_IMAGE", "PREVIEW_ONLY"], {"default": "PREVIEW_ONLY"}),
                "image": ("IMAGE",),
                "folder_name": ("STRING", {"default": "dp_image_folder"}),
                "file_name": ("STRING", {"default": "image"}),
                "extra_text": ("STRING", {"default": ""}),
                "add_size_to_name": ("BOOLEAN", {"default": False}),
                "save_caption": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "prompt_text": ("STRING", {"default": "", "forceInput": True})
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"}
        }

    RETURN_TYPES = ()
    FUNCTION = "save_image"
    OUTPUT_NODE = True
    CATEGORY = "DP/image"

    def sanitize_filename(self, name):
        name = re.sub(r'[^\w\-_]', '_', name)
        return name

    def save_image(self, mode, image, folder_name, file_name, extra_text, add_size_to_name, 
                   save_caption, prompt_text, prompt=None, extra_pnginfo=None):
        # Sanitize inputs
        folder_name = self.sanitize_filename(folder_name) if folder_name.strip() else ""
        file_name = self.sanitize_filename(file_name) if file_name.strip() else "image"
        extra_text = self.sanitize_filename(extra_text)

        # Handle both single images and batches
        if len(image.shape) == 3:
            images = [image]
        else:
            images = [image[i] for i in range(image.shape[0])]

        results = []
        
        if mode == "PREVIEW_ONLY":
            # For preview mode, use temp directory
            preview_dir = folder_paths.get_temp_directory()
            
            for idx, img in enumerate(images):
                # Convert to PIL Image
                i = 255. * img.cpu().numpy()
                img_pil = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
                
                # Generate a preview filename
                file = f"preview_{idx:05d}.png"
                
                # Save to temp directory
                image_path = os.path.join(preview_dir, file)
                img_pil.save(image_path, compress_level=1)
                
                results.append({
                    "filename": file,
                    "subfolder": "",
                    "type": "temp"
                })
        else:
            # Create full output folder path
            full_output_folder = self.output_dir
            if folder_name:
                full_output_folder = os.path.join(self.output_dir, folder_name)
                os.makedirs(full_output_folder, exist_ok=True)

            for idx, img in enumerate(images):
                # Prepare filename components
                name_parts = [file_name]
                if extra_text:
                    name_parts.append(extra_text)
                if add_size_to_name:
                    height, width = img.shape[1:3]
                    name_parts.append(f"{width}x{height}")
                if len(images) > 1:
                    name_parts.append(f"{idx:04d}")

                # Join name parts with underscores
                base_name = "_".join(name_parts)

                # Convert to PIL Image
                i = 255. * img.cpu().numpy()
                img_pil = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

                # Create metadata
                metadata = PngImagePlugin.PngInfo()
                
                # Save prompt text if provided
                if prompt_text.strip():
                    metadata.add_text("dp_prompt", prompt_text.strip())
                
                # Add extra pnginfo if available
                if extra_pnginfo is not None:
                    for x in extra_pnginfo:
                        metadata.add_text(x, json.dumps(extra_pnginfo[x]))

                # Save the image
                file = f"{base_name}.png"
                image_path = os.path.join(full_output_folder, file)
                counter = 1
                while os.path.exists(image_path):
                    file = f"{base_name}_{counter:04d}.png"
                    image_path = os.path.join(full_output_folder, file)
                    counter += 1

                img_pil.save(image_path, 
                           pnginfo=metadata,
                           compress_level=self.compress_level)

                # Save caption if enabled
                if save_caption and prompt_text.strip():
                    caption_path = os.path.splitext(image_path)[0] + ".txt"
                    with open(caption_path, 'w', encoding='utf-8') as f:
                        f.write(prompt_text.strip())

                results.append({
                    "filename": file,
                    "subfolder": folder_name,
                    "type": self.type
                })

        return {"ui": {"images": results}}

