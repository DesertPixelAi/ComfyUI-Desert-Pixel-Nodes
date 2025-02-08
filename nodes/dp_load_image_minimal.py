import os
import torch
import numpy as np
from PIL import Image, ImageOps
import folder_paths
from .image_effects import ImageEffects
import comfy.utils

class DP_Load_Image_Minimal:
    def __init__(self):
        self.effects = ImageEffects()

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
        }}

    def load_image_and_process(self, image, resize_image, width, height):
        # Process uploaded image
        image_path = folder_paths.get_annotated_filepath(image)
        formatted_name = os.path.splitext(os.path.basename(image_path))[0]
        prompt_text = ""
        negative_text = ""
        
        try:
            with Image.open(image_path) as img:
                img = ImageOps.exif_transpose(img)
                if img.mode == 'I':
                    img = img.point(lambda i: i * (1 / 255))
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                image = np.array(img).astype(np.float32) / 255.0
                uploaded_image = torch.from_numpy(image).unsqueeze(0)
                prompt_text = img.info.get('dp_prompt', '')
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

        return (uploaded_image, formatted_name, prompt_text, negative_text)

    @classmethod
    def IS_CHANGED(s, image, resize_image=True, width=1024, height=1024):
        image_path = folder_paths.get_annotated_filepath(image)
        return f"{image_path}_{resize_image}_{width}_{height}"

    @classmethod
    def VALIDATE_INPUTS(s, image, *args, **kwargs):
        if not folder_paths.exists_annotated_filepath(image):
            return "Invalid image file: {}".format(image)
        return True

    RETURN_TYPES = ("IMAGE", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("image", "filename", "dp_prompt", "dp_negative_or_other")
    FUNCTION = "load_image_and_process"
    CATEGORY = "DP/image" 