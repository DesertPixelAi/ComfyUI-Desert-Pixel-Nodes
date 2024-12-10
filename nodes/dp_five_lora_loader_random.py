import folder_paths
import random
from nodes import LoraLoader

class DP_Five_Lora_Random:
    """
    ComfyUI node for loading up to five LoRA models with random strength values.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "loader_state": (["ON", "OFF"],),
                "Lora_01": (['None'] + folder_paths.get_filename_list("loras"),),
                "Lora_01_Strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Random_Min": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Random_Max": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
            },
            "optional": {
                "Lora_02": (['None'] + folder_paths.get_filename_list("loras"),),
                "Lora_02_Strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Random_Min_2": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Random_Max_2": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Lora_03": (['None'] + folder_paths.get_filename_list("loras"),),
                "Lora_03_Strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Random_Min_3": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Random_Max_3": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Lora_04": (['None'] + folder_paths.get_filename_list("loras"),),
                "Lora_04_Strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Random_Min_4": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Random_Max_4": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Lora_05": (['None'] + folder_paths.get_filename_list("loras"),),
                "Lora_05_Strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Random_Min_5": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Random_Max_5": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
            }
        }
    
    RETURN_TYPES = ("MODEL", "CLIP", "STRING")
    RETURN_NAMES = ("model", "clip", "lora_info")
    FUNCTION = "apply_lora"
    CATEGORY = "DP/loaders"
    
    IS_CHANGED = True

    def get_random_strength(self, strength, min_val, max_val):
        if min_val == 0 and max_val == 0:
            return strength
        # Round to 2 decimal places for cleaner values
        return round(random.uniform(min_val, max_val), 2)

    def apply_lora(self, model, clip, loader_state,
                  Lora_01, Lora_01_Strength, Random_Min, Random_Max,
                  Lora_02="None", Lora_02_Strength=1.0, Random_Min_2=0.0, Random_Max_2=0.0,
                  Lora_03="None", Lora_03_Strength=1.0, Random_Min_3=0.0, Random_Max_3=0.0,
                  Lora_04="None", Lora_04_Strength=1.0, Random_Min_4=0.0, Random_Max_4=0.0,
                  Lora_05="None", Lora_05_Strength=1.0, Random_Min_5=0.0, Random_Max_5=0.0):
        
        weights_info = ["LoRA Models Info:"]

        if loader_state == "OFF":
            weights_info.append("Bypassed - No LoRAs applied")
            return (model, clip, "\n".join(weights_info))

        if Lora_01 != "None":
            strength = self.get_random_strength(Lora_01_Strength, Random_Min, Random_Max)
            model, clip = LoraLoader().load_lora(model, clip, Lora_01, strength, strength)
            weights_info.append(f"{Lora_01}: {strength}")
            
        if Lora_02 != "None":
            strength = self.get_random_strength(Lora_02_Strength, Random_Min_2, Random_Max_2)
            model, clip = LoraLoader().load_lora(model, clip, Lora_02, strength, strength)
            weights_info.append(f"{Lora_02}: {strength}")
            
        if Lora_03 != "None":
            strength = self.get_random_strength(Lora_03_Strength, Random_Min_3, Random_Max_3)
            model, clip = LoraLoader().load_lora(model, clip, Lora_03, strength, strength)
            weights_info.append(f"{Lora_03}: {strength}")
            
        if Lora_04 != "None":
            strength = self.get_random_strength(Lora_04_Strength, Random_Min_4, Random_Max_4)
            model, clip = LoraLoader().load_lora(model, clip, Lora_04, strength, strength)
            weights_info.append(f"{Lora_04}: {strength}")
            
        if Lora_05 != "None":
            strength = self.get_random_strength(Lora_05_Strength, Random_Min_5, Random_Max_5)
            model, clip = LoraLoader().load_lora(model, clip, Lora_05, strength, strength)
            weights_info.append(f"{Lora_05}: {strength}")
            
        return (model, clip, "\n".join(weights_info))