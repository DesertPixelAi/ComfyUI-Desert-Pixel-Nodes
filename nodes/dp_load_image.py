import os
import torch
import numpy as np
import cv2
from PIL import Image, ImageOps
import folder_paths
from .image_effects import ImageEffects
import comfy.utils

class DP_Load_Image_Effects:
    def __init__(self):
        self.effects = ImageEffects()
        
        # Effects with no parameters (simple on/off)
        self.BASIC_EFFECTS = {
            "original",
            "grayscale",
            "enhance",
            "flip_h",
            "flip_v",
            "rotate_90_ccw",
            "rotate_180",
            "rotate_270_ccw",
            "edge_detect",
            "edge_gradient",
            "lineart_anime"
        }

        # Effects that need strength parameter
        self.STRENGTH_EFFECTS = {
            "posterize": lambda strength: max(2, int(8 - (strength * 6))),      # 8 (weak) to 2 (strong)
            "sharpen": lambda strength: strength * 2.0,                         # 0.0 to 2.0
            "sepia": lambda strength: strength,                                 # 0.0 to 1.0
            "blur": lambda strength: strength * 10.0,                          # 0.0 to 10.0
            "emboss": lambda strength: strength * 2.0,                         # 0.0 to 2.0
            "palette": lambda strength: max(2, int(32 - (strength * 30))),     # 32 (weak) to 2 (strong)
            "solarize": lambda strength: 1.0 - strength,                       # 1.0 (weak) to 0.0 (strong)
            "denoise": lambda strength: max(1, int(strength * 5)),            # 1 to 5 (integer)
            "vignette": lambda strength: strength,                            # 0.0 to 1.0
            "glow_edges": lambda strength: strength,                          # 0.0 to 1.0
            "threshold": lambda strength: strength,                           # 0.0 to 1.0
            "contrast": lambda strength: 0.5 + (strength * 1.5),             # 0.5 (weak) to 2.0 (strong)
            "equalize": lambda strength: strength                            # Added equalize
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
            "effect_strength": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
            "uploaded_image_effect_A": (available_styles, {"default": "original"}),
            "uploaded_image_effect_B": (available_styles, {"default": "grayscale"}),
            "input_image_01_effect": (available_styles, {"default": "original"}),
            "input_image_02_effect": (available_styles, {"default": "grayscale"}),
            "width": ("INT", {"default": 1024, "min": 64, "max": 2048, "step": 8}),
            "height": ("INT", {"default": 1024, "min": 64, "max": 2048, "step": 8}),
        },
        "optional": {
            "Image_Input_01": ("IMAGE", {"forceInput": True}),
            "Image_Input_02": ("IMAGE", {"forceInput": True})
        }}

    def apply_effect(self, effect_name, image, strength):
        if effect_name in self.BASIC_EFFECTS:
            # Use existing effect without strength parameter
            return getattr(self.effects, effect_name)(image)
        elif effect_name in self.STRENGTH_EFFECTS:
            # Map the 0-1 strength to appropriate parameter range
            mapped_strength = self.STRENGTH_EFFECTS[effect_name](strength)
            return getattr(self.effects, effect_name)(image, mapped_strength)
        return image

    def load_image_and_process(self, image, effect_strength, uploaded_image_effect_A, uploaded_image_effect_B,
                             input_image_01_effect, input_image_02_effect, width, height,
                             Image_Input_01=None, Image_Input_02=None):
        prompt_text = ""
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
        except Exception as e:
            print(f"Error processing image: {e}")
            raise e

        # Resize uploaded image
        samples = uploaded_image.movedim(-1,1)
        resized = comfy.utils.common_upscale(samples, width, height, "lanczos", "center")
        uploaded_image = resized.movedim(1,-1)

        # Process uploaded image with both effects
        uploaded_image_01 = self.apply_effect(uploaded_image_effect_A, uploaded_image, effect_strength)
        uploaded_image_02 = self.apply_effect(uploaded_image_effect_B, uploaded_image, effect_strength)
        results.extend([uploaded_image_01, uploaded_image_02])

        # Process input images if provided, otherwise use uploaded image with selected effect
        for input_image, effect in [(Image_Input_01, input_image_01_effect),
                                  (Image_Input_02, input_image_02_effect)]:
            if input_image is not None:
                # Resize input image
                samples = input_image.movedim(-1,1)
                resized = comfy.utils.common_upscale(samples, width, height, "lanczos", "center")
                processed = resized.movedim(1,-1)
                # Apply effect
                processed = self.apply_effect(effect, processed, effect_strength)
                results.append(processed)
            else:
                # Use uploaded image with the effect selected for this input
                fallback = self.apply_effect(effect, uploaded_image, effect_strength)
                results.append(fallback)

        return (formatted_name, *results, prompt_text)

    @classmethod
    def IS_CHANGED(s, image, effect_strength, uploaded_image_effect_A, uploaded_image_effect_B,
                   input_image_01_effect, input_image_02_effect, width, height,
                   Image_Input_01=None, Image_Input_02=None):
        if Image_Input_01 is not None or Image_Input_02 is not None:
            return True
        image_path = folder_paths.get_annotated_filepath(image)
        return image_path

    @classmethod
    def VALIDATE_INPUTS(s, image, effect_strength, uploaded_image_effect_A, uploaded_image_effect_B,
                       input_image_01_effect, input_image_02_effect, width, height,
                       Image_Input_01=None, Image_Input_02=None):
        if Image_Input_01 is not None or Image_Input_02 is not None:
            return True
        if not folder_paths.exists_annotated_filepath(image):
            return "Invalid image file: {}".format(image)
        return True

    RETURN_TYPES = ("STRING", "IMAGE", "IMAGE", "IMAGE", "IMAGE", "STRING")
    RETURN_NAMES = ("filename", "uploaded_image_01", "uploaded_image_02", 
                   "input_image_01", "input_image_02", "prompt")
    FUNCTION = "load_image_and_process"
    CATEGORY = "DP/image"

