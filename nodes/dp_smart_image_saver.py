import os
import torch
import numpy as np
from PIL import Image, PngImagePlugin
import folder_paths
from pathlib import Path
import re
import json
from server import PromptServer

class DP_smart_saver:
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
                "folder_name": ("STRING", {"default": "folder_name"}),
                "file_name": ("STRING", {"default": "my_file_name"}),
                "extra_text": ("STRING", {"default": ""}),
                "add_size_to_name": ("BOOLEAN", {"default": False}),
                "save_caption": ("BOOLEAN", {"default": False}),
                "caption_text": ("STRING", {"default": ""})
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"}
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("file_info",)
    FUNCTION = "save_image"
    OUTPUT_NODE = True
    CATEGORY = "DP/image"

    def sanitize_filename(self, name):
        # Remove spaces and special characters
        name = re.sub(r'[^\w\-_]', '_', name)
        return name

    def get_unique_file_path(self, base_path, name, ext):
        """Generate unique filename with auto-increment"""
        counter = 1
        file_path = os.path.join(base_path, f"{name}.{ext}")
        while os.path.exists(file_path):
            file_path = os.path.join(base_path, f"{name}_{counter:04d}.{ext}")
            counter += 1
        return file_path

    def save_image(self, mode, image, folder_name, file_name, extra_text, add_size_to_name, save_caption, caption_text, prompt=None, extra_pnginfo=None):
        # Sanitize inputs
        folder_name = self.sanitize_filename(folder_name)
        file_name = self.sanitize_filename(file_name)
        extra_text = self.sanitize_filename(extra_text)

        # Create full output folder path
        full_output_folder = self.output_dir
        if folder_name:
            full_output_folder = os.path.join(self.output_dir, folder_name)
            if mode == "SAVE_IMAGE":
                os.makedirs(full_output_folder, exist_ok=True)

        # Prepare filename components
        name_parts = [file_name]
        if extra_text:
            name_parts.append(extra_text)
        if add_size_to_name:
            height, width = image.shape[1:3]
            name_parts.append(f"{width}x{height}")

        # Join name parts with underscores
        base_name = "_".join(name_parts)

        # Get unique file paths
        image_path = self.get_unique_file_path(full_output_folder, base_name, "png")
        base_name = os.path.splitext(os.path.basename(image_path))[0]

        # Save the image with metadata
        i = 255. * image.cpu().numpy()
        i = i.squeeze(0) if len(i.shape) == 4 else i
        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

        # Get workflow and create metadata
        metadata = PngImagePlugin.PngInfo()
        
        if prompt is not None:
            metadata.add_text("prompt", json.dumps(prompt))
        if extra_pnginfo is not None:
            for x in extra_pnginfo:
                metadata.add_text(x, json.dumps(extra_pnginfo[x]))
        
        # Save image with metadata
        img.save(image_path, 
                pnginfo=metadata,
                compress_level=self.compress_level)

        # Save caption if enabled
        if save_caption and caption_text:
            caption_path = os.path.join(full_output_folder, f"{base_name}.txt")
            with open(caption_path, 'w', encoding='utf-8') as f:
                f.write(caption_text)

        # Prepare preview data
        results = []
        subfolder = folder_name if folder_name else ""
        file = os.path.basename(image_path)
            
        results.append({
            "filename": file,
            "subfolder": subfolder,
            "type": self.type
        })

        # Get dimensions for output
        height, width = image.shape[1:3]
        
        if mode == "SAVE_IMAGE":
            # Get file size in bytes and convert to appropriate unit
            file_size_bytes = os.path.getsize(image_path)
            if file_size_bytes >= 1024 * 1024:
                file_size = round(file_size_bytes / (1024 * 1024), 1)
                size_str = f"{file_size} mb"
            else:
                file_size = round(file_size_bytes / 1024)
                size_str = f"{file_size} kb"
            
            output_text = f"{full_output_folder}\nfile name: {file}\ndimensions WxH: {width}x{height}\nsize: {size_str}"
        else:
            # Preview mode - only show dimensions
            output_text = f"PREVIEW MODE\ndimensions WxH: {width}x{height}"
            file = "preview_only.png"  # Dummy filename for preview

        # Return both the folder path and UI data for preview
        return {"ui": {"images": results}, "result": (output_text,)}

# For ComfyUI registration
NODE_CLASS_MAPPINGS = {
    "DP_smart_saver": DP_smart_saver
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DP_smart_saver": "DP Smart Image Saver"
}