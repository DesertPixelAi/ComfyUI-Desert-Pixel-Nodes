import torch
from typing import List, Union, Dict, Any, Tuple

class DP_Condition_Mixer:
    """
    A node that mixes base conditions with ControlNet conditions using a weight parameter.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base_positive": ("CONDITIONING",),
                "base_negative": ("CONDITIONING",),
                "controlnet_weight": ("FLOAT", {
                    "default": 1.0, 
                    "min": 0.0, 
                    "max": 1.0, 
                    "step": 0.05
                }),
            },
            "optional": {
                "controlnet_positive": ("CONDITIONING",),
                "controlnet_negative": ("CONDITIONING",),
            }
        }
    
    RETURN_TYPES = ("CONDITIONING", "CONDITIONING")
    RETURN_NAMES = ("positive", "negative")
    FUNCTION = "mix_conditions"
    CATEGORY = "DP/conditioning"

    def mix_conditions(self, base_positive, base_negative, controlnet_weight, 
                      controlnet_positive=None, controlnet_negative=None):
        # If no controlnet conditions provided, return base conditions
        if controlnet_positive is None or controlnet_negative is None:
            return (base_positive, base_negative)

        # When weight is 0, return only base conditions
        if controlnet_weight == 0:
            return (base_positive, base_negative)

        # Mix positive conditions
        mixed_positive = list(base_positive)  # Start with base conditions
        
        # Add controlnet conditions with adjusted weights
        for cond in controlnet_positive:
            if isinstance(cond, tuple) and len(cond) >= 2:
                if isinstance(cond[1], dict) and 'control' in cond[1]:
                    new_control = cond[1].copy()
                    new_control['control'] = float(controlnet_weight)
                    mixed_positive.append((cond[0], new_control))

        # Mix negative conditions (same logic)
        mixed_negative = list(base_negative)  # Start with base conditions
        
        # Add controlnet conditions with adjusted weights
        for cond in controlnet_negative:
            if isinstance(cond, tuple) and len(cond) >= 2:
                if isinstance(cond[1], dict) and 'control' in cond[1]:
                    new_control = cond[1].copy()
                    new_control['control'] = float(controlnet_weight)
                    mixed_negative.append((cond[0], new_control))

        return (mixed_positive, mixed_negative) 