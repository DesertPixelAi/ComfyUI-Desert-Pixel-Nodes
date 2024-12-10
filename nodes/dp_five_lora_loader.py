import folder_paths
from nodes import LoraLoader

class DP_Five_Lora:
    """
    ComfyUI node for loading up to five LoRA models simultaneously.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "loader_state": (["ON", "OFF"],),
                "Lora_01": (['None'] + folder_paths.get_filename_list("loras"),),
                "Lora_01_Strength": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
            },
            "optional": {
                "Lora_02": (['None'] + folder_paths.get_filename_list("loras"),),
                "Lora_02_Strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Lora_03": (['None'] + folder_paths.get_filename_list("loras"),),
                "Lora_03_Strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Lora_04": (['None'] + folder_paths.get_filename_list("loras"),),
                "Lora_04_Strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Lora_05": (['None'] + folder_paths.get_filename_list("loras"),),
                "Lora_05_Strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
            }
        }
    
    RETURN_TYPES = ("MODEL", "CLIP", "STRING")
    RETURN_NAMES = ("model", "clip", "lora_info")
    FUNCTION = "apply_lora"
    CATEGORY = "DP/loaders"

    def apply_lora(self, model, clip, loader_state, Lora_01, Lora_01_Strength,
                  Lora_02="None", Lora_02_Strength=0.0,
                  Lora_03="None", Lora_03_Strength=0.0,
                  Lora_04="None", Lora_04_Strength=0.0,
                  Lora_05="None", Lora_05_Strength=0.0):
        
        weights_info = ["LoRA Models Info:"]
        
        if loader_state == "OFF":
            weights_info.append("Bypassed - No LoRAs applied")
            return (model, clip, "\n".join(weights_info))

        if Lora_01 != "None" and Lora_01_Strength != 0:
            model, clip = LoraLoader().load_lora(model, clip, Lora_01, Lora_01_Strength, Lora_01_Strength)
            weights_info.append(f"{Lora_01}: {Lora_01_Strength}")
            
        if Lora_02 != "None" and Lora_02_Strength != 0:
            model, clip = LoraLoader().load_lora(model, clip, Lora_02, Lora_02_Strength, Lora_02_Strength)
            weights_info.append(f"{Lora_02}: {Lora_02_Strength}")
            
        if Lora_03 != "None" and Lora_03_Strength != 0:
            model, clip = LoraLoader().load_lora(model, clip, Lora_03, Lora_03_Strength, Lora_03_Strength)
            weights_info.append(f"{Lora_03}: {Lora_03_Strength}")
            
        if Lora_04 != "None" and Lora_04_Strength != 0:
            model, clip = LoraLoader().load_lora(model, clip, Lora_04, Lora_04_Strength, Lora_04_Strength)
            weights_info.append(f"{Lora_04}: {Lora_04_Strength}")
            
        if Lora_05 != "None" and Lora_05_Strength != 0:
            model, clip = LoraLoader().load_lora(model, clip, Lora_05, Lora_05_Strength, Lora_05_Strength)
            weights_info.append(f"{Lora_05}: {Lora_05_Strength}")
        
        return (model, clip, "\n".join(weights_info))