import os
import torch
import numpy as np
from PIL import Image, ImageOps
import folder_paths
from pathlib import Path
import re
import json

class DP_Load_Image_V2:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 4

    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = []
        for filename in os.listdir(input_dir):
            if filename.endswith(('.png', '.jpg', '.jpeg', '.webp')):
                files.append(filename)
        
        return {"required": {
            "image": (sorted(files), {"image_upload": True}),
            "resize_image": ("BOOLEAN", {"default": True}),
            "width": ("INT", {"default": 1024, "min": 64, "max": 2048, "step": 8}),
            "height": ("INT", {"default": 1024, "min": 64, "max": 2048, "step": 8}),
            "preserve_alpha": ("BOOLEAN", {"default": True}),
        }}

    def load_image_and_process(self, image, resize_image, width, height, preserve_alpha):
        # Process uploaded image
        image_path = folder_paths.get_annotated_filepath(image)
        formatted_name = os.path.splitext(os.path.basename(image_path))[0]
        prompt_text = ""
        negative_text = ""
        
        # Get image format and preserve exact extension
        image_format = os.path.splitext(image_path)[1].lower()
        if image_format == '.jpg':
            image_format = 'JPG'
        elif image_format == '.jpeg':
            image_format = 'JPEG'
        elif image_format == '.png':
            image_format = 'PNG'
        elif image_format == '.webp':
            image_format = 'WEBP'
        
        try:
            with Image.open(image_path) as img:
                img = ImageOps.exif_transpose(img)
                
                # Extract mask from alpha channel if it exists
                has_alpha = 'A' in img.getbands() or (img.mode == 'P' and 'transparency' in img.info)
                
                if has_alpha:
                    if 'A' in img.getbands():
                        alpha = np.array(img.getchannel('A')).astype(np.float32) / 255.0
                    else:  # P with transparency
                        alpha = np.array(img.convert('RGBA').getchannel('A')).astype(np.float32) / 255.0
                    
                    # Create inverted mask (ComfyUI convention: 0=keep, 1=discard)
                    mask = 1.0 - alpha
                    mask = torch.from_numpy(mask)
                else:
                    mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")
                
                # Process the image
                if img.mode == 'I':
                    img = img.point(lambda i: i * (1 / 255))
                
                # Handle image conversion based on preserve_alpha setting
                if preserve_alpha and has_alpha:
                    if img.mode != 'RGBA':
                        img = img.convert('RGBA')
                    # Process as RGBA (4 channels)
                    image_array = np.array(img).astype(np.float32) / 255.0
                else:
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    # Process as RGB (3 channels)
                    image_array = np.array(img).astype(np.float32) / 255.0
                
                uploaded_image = torch.from_numpy(image_array).unsqueeze(0)
                prompt_text = img.info.get('dp_prompt', '')
                negative_text = img.info.get('dp_negative_or_other', '')
        except Exception as e:
            print(f"Error processing image: {e}")
            raise e

        # Resize uploaded image only if resize_image is True
        if resize_image:
            try:
                width = int(width) if width != "image" else image_array.shape[1]
                height = int(height) if height != "image" else image_array.shape[0]
            except (ValueError, AttributeError) as e:
                print(f"[Python] Error converting dimensions: {str(e)}")
                if hasattr(image_array, 'shape'):
                    width = image_array.shape[1]
                    height = image_array.shape[0]
                else:
                    raise ValueError("Invalid image or dimensions provided")

            samples = uploaded_image.movedim(-1,1)
            resized = comfy.utils.common_upscale(samples, width, height, "lanczos", "center")
            uploaded_image = resized.movedim(1,-1)
            
            # Also resize the mask if needed
            if mask.shape[0] != height or mask.shape[1] != width:
                mask = mask.unsqueeze(0).unsqueeze(0)  # Add batch and channel dimensions
                mask_resized = torch.nn.functional.interpolate(mask, size=(height, width), mode='bilinear', align_corners=False)
                mask = mask_resized.squeeze(0).squeeze(0)  # Remove batch and channel dimensions

        return (uploaded_image, mask, formatted_name, prompt_text, negative_text, image_format)

    @classmethod
    def IS_CHANGED(s, image, resize_image=True, width=1024, height=1024, preserve_alpha=True):
        image_path = folder_paths.get_annotated_filepath(image)
        return f"{image_path}_{resize_image}_{width}_{height}_{preserve_alpha}"

    @classmethod
    def VALIDATE_INPUTS(s, image, *args, **kwargs):
        if not folder_paths.exists_annotated_filepath(image):
            return "Invalid image file: {}".format(image)
        return True

    RETURN_TYPES = ("IMAGE", "MASK", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("image", "mask", "filename", "dp_prompt", "dp_negative_or_other", "image_format")
    FUNCTION = "load_image_and_process"
    CATEGORY = "DP/image" 