import torch
import numpy as np
from PIL import Image
import comfy.utils
from .image_effects import ImageEffects

class DP_Image_Effect_Processor:
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
            "effect_strength": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
            "image_01_effect": (available_styles, {"default": "original"}),
            "image_02_effect": (available_styles, {"default": "grayscale"}),
            "image_03_effect": (available_styles, {"default": "enhance"}),
            "image_04_effect": (available_styles, {"default": "edge_detect"}),
            "width": ("INT", {"default": 1024, "min": 64, "max": 2048, "step": 8}),
            "height": ("INT", {"default": 1024, "min": 64, "max": 2048, "step": 8}),
        },
        "optional": {
            "image_input_01": ("IMAGE", {"forceInput": True}),
            "image_input_02": ("IMAGE", {"forceInput": True}),
            "image_input_03": ("IMAGE", {"forceInput": True}),
            "image_input_04": ("IMAGE", {"forceInput": True})
        }}

    def apply_effect(self, effect_name, image, strength):
        if effect_name in self.BASIC_EFFECTS:
            return getattr(self.effects, effect_name)(image)
        elif effect_name in self.STRENGTH_EFFECTS:
            mapped_strength = self.STRENGTH_EFFECTS[effect_name](strength)
            return getattr(self.effects, effect_name)(image, mapped_strength)
        return image

    def process_images(self, effect_strength, image_01_effect, image_02_effect,
                      image_03_effect, image_04_effect, width, height,
                      image_input_01=None, image_input_02=None,
                      image_input_03=None, image_input_04=None):
        results = []
        prompt_text = ""
        
        # Process each input image if provided
        for input_image, effect in [
            (image_input_01, image_01_effect),
            (image_input_02, image_02_effect),
            (image_input_03, image_03_effect),
            (image_input_04, image_04_effect)
        ]:
            if input_image is not None:
                # Resize input image
                samples = input_image.movedim(-1,1)
                resized = comfy.utils.common_upscale(samples, width, height, "lanczos", "center")
                processed = resized.movedim(1,-1)
                # Apply effect
                processed = self.apply_effect(effect, processed, effect_strength)
                results.append(processed)
            else:
                results.append(None)

        return (*results, prompt_text)

    RETURN_TYPES = ("IMAGE", "IMAGE", "IMAGE", "IMAGE", "STRING")
    RETURN_NAMES = ("image_output_01", "image_output_02", "image_output_03", "image_output_04", "prompt")
    FUNCTION = "process_images"
    CATEGORY = "DP/Image"