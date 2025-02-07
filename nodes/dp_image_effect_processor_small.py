import torch
import numpy as np
from PIL import Image
import comfy.utils
from .image_effects import ImageEffects

class DP_Image_Effect_Processor_Small:
    def __init__(self):
        self.effects = ImageEffects()
        
        # Effects with no parameters (simple on/off)
        self.BASIC_EFFECTS = {
            "original", "grayscale", "flip_h",
            "flip_v", "rotate_90_ccw", "rotate_180", "rotate_270_ccw",
            "edge_detect", "edge_gradient", "lineart_anime",
            "desaturate"
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
            "equalize": lambda strength: strength,
            "enhance": lambda strength: strength * 2.0
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
            "image_effect": (available_styles, {"default": "original"}),
        },
        "optional": {
            "image": ("IMAGE", {"forceInput": True}),
        }}

    def apply_effect(self, effect_name, image, strength):
        # Ensure image is in the correct format (B,H,W,C)
        if len(image.shape) == 3:
            image = image.unsqueeze(0)
        
        if effect_name == "original":
            return image
        elif effect_name in self.BASIC_EFFECTS:
            method = getattr(self.effects, effect_name)
            if effect_name in ["rotate_90_ccw", "rotate_180", "rotate_270_ccw"]:
                return method(image)
            return method(image)
        elif effect_name in self.STRENGTH_EFFECTS:
            mapped_strength = self.STRENGTH_EFFECTS[effect_name](strength)
            method = getattr(self.effects, effect_name)
            return method(image, mapped_strength)
        return image

    def process_image(self, effect_strength, image_effect, image=None):
        if image is not None:
            processed = self.apply_effect(image_effect, image, effect_strength)
            return (processed,)
        return (None,)

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image_output",)
    FUNCTION = "process_image"
    CATEGORY = "DP/Image" 