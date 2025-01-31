import os
import torch
import numpy as np
import cv2
from PIL import Image, ImageOps
import folder_paths
from .image_effects import ImageEffects
import comfy.utils

class DP_Load_Image_Effects_Small:
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
        results = []
        
        # Process uploaded image
        image_path = folder_paths.get_annotated_filepath(image)
        formatted_name = os.path.splitext(os.path.basename(image_path))[0]
        
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
                # Fallback to original image dimensions if conversion fails
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

        return (image_A, image_B, formatted_name, prompt_text, negative_text)

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

    RETURN_TYPES = ("IMAGE", "IMAGE", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("image_A", "image_B", "filename", "dp_prompt", "dp_negative_or_other")
    FUNCTION = "load_image_and_process"
    CATEGORY = "DP/image" 