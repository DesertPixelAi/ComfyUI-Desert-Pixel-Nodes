import os
import torch
import numpy as np
from PIL import Image, PngImagePlugin
import folder_paths
from pathlib import Path
import re
import json

class DP_Save_Image_V2:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 4

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mode": (["SAVE_IMAGE", "PREVIEW_ONLY"], {"default": "SAVE_IMAGE"}),
                "image": ("IMAGE",),
                "folder_name": ("STRING", {"default": "dp_image_folder"}),
                "file_name": ("STRING", {"default": "image"}),
                "extra_text": ("STRING", {"default": ""}),
                "add_size_to_name": ("BOOLEAN", {"default": False}),
                "save_caption": ("BOOLEAN", {"default": False}),
                "image_format": (["PNG", "JPG", "JPEG", "WEBP"], {"default": "PNG"}),
            },
            "optional": {
                "prompt_and_caption_text": ("STRING", {"default": "", "defaultInput": True}),
                "negative_or_other": ("STRING", {"default": "", "defaultInput": True}),
                "format_override": ("STRING", {"default": ""}),
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
                   save_caption, image_format, prompt_and_caption_text="", negative_or_other="", 
                   format_override="", prompt=None, extra_pnginfo=None):
        # Sanitize inputs
        folder_parts = folder_name.strip().split('/') if folder_name.strip() else [""]
        folder_parts = [self.sanitize_filename(part) for part in folder_parts if part.strip()]
        folder_name = os.path.join(*folder_parts) if folder_parts else ""
        file_name = self.sanitize_filename(file_name) if file_name.strip() else "image"
        extra_text = self.sanitize_filename(extra_text)

        # Handle format override
        if format_override and format_override.strip():
            image_format = format_override.strip().upper()

        # Handle both single images and batches
        if len(image.shape) == 3:
            images = [image]
        else:
            images = [image[i] for i in range(image.shape[0])]

        results = []
        
        if mode == "PREVIEW_ONLY":
            preview_dir = folder_paths.get_temp_directory()
            
            for idx, img in enumerate(images):
                i = 255. * img.cpu().numpy()
                img_pil = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
                
                file = f"preview_{idx:05d}.png"
                image_path = os.path.join(preview_dir, file)
                img_pil.save(image_path, compress_level=1)
                
                results.append({
                    "filename": file,
                    "subfolder": "",
                    "type": "temp"
                })
        else:
            full_output_folder = self.output_dir
            if folder_name:
                full_output_folder = os.path.join(self.output_dir, folder_name)
                os.makedirs(full_output_folder, exist_ok=True)

            for idx, img in enumerate(images):
                name_parts = [file_name]
                if extra_text:
                    name_parts.append(extra_text)
                
                # Convert to PIL Image
                i = 255. * img.cpu().numpy()
                img_pil = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
                
                if add_size_to_name:
                    width, height = img_pil.size
                    name_parts.append(f"{width}x{height}")
                if len(images) > 1:
                    name_parts.append(f"{idx:04d}")

                base_name = "_".join(name_parts)

                # Add metadata for PNG format
                if image_format == "PNG":
                    metadata = PngImagePlugin.PngInfo()
                    
                    if extra_pnginfo is not None:
                        for k, v in extra_pnginfo.items():
                            metadata.add_text(k, json.dumps(v))
                    
                    if prompt_and_caption_text.strip():
                        metadata.add_text("dp_prompt", prompt_and_caption_text.strip())
                    
                    if negative_or_other.strip():
                        metadata.add_text("dp_negative_or_other", negative_or_other.strip())

                # Determine file extension based on exact format
                if image_format == "PNG":
                    ext = ".png"
                elif image_format == "JPG":
                    ext = ".jpg"
                elif image_format == "JPEG":
                    ext = ".jpeg"
                else:  # WEBP
                    ext = ".webp"
                
                file = f"{base_name}{ext}"
                image_path = os.path.join(full_output_folder, file)
                counter = 1
                while os.path.exists(image_path):
                    file = f"{base_name}_{counter:04d}{ext}"
                    image_path = os.path.join(full_output_folder, file)
                    counter += 1

                # Save with appropriate format and options
                if image_format == "PNG":
                    img_pil.save(image_path, 
                               pnginfo=metadata,
                               compress_level=self.compress_level)
                elif image_format in ["JPG", "JPEG"]:
                    img_pil.save(image_path, 
                               quality=95,
                               optimize=True)
                else:  # WEBP
                    img_pil.save(image_path, 
                               quality=95,
                               method=6)  # 6 is the highest quality compression method

                if save_caption and prompt_and_caption_text.strip():
                    caption_path = os.path.splitext(image_path)[0] + ".txt"
                    with open(caption_path, 'w', encoding='utf-8') as f:
                        f.write(prompt_and_caption_text.strip())

                results.append({
                    "filename": file,
                    "subfolder": folder_name,
                    "type": self.type
                })

        return {"ui": {"images": results}} 