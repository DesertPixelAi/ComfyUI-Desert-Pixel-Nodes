import folder_paths
from nodes import LoraLoader

class DP_Five_Lora:
    """
    ComfyUI node for loading up to five LoRA models simultaneously.
    """
    def __init__(self):
        self.lora_loader = LoraLoader()  # Reuse single instance
    
    @classmethod
    def INPUT_TYPES(cls):
        lora_files = ['None'] + folder_paths.get_filename_list("loras")  # Cache list
        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "loader_state": (["ON", "OFF"],),
                "Lora_01": (lora_files,),
                "Lora_01_Strength": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
            },
            "optional": {
                "Lora_02": (lora_files,),
                "Lora_02_Strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Lora_03": (lora_files,),
                "Lora_03_Strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Lora_04": (lora_files,),
                "Lora_04_Strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01, "display": "slider"}),
                "Lora_05": (lora_files,),
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
        
        if loader_state == "OFF":
            return (model, clip, "LoRA Models Info:\nBypassed - No LoRAs applied")

        weights_info = ["LoRA Models Info:"]
        loras = [
            (Lora_01, Lora_01_Strength),
            (Lora_02, Lora_02_Strength),
            (Lora_03, Lora_03_Strength),
            (Lora_04, Lora_04_Strength),
            (Lora_05, Lora_05_Strength)
        ]
        
        # Process all LoRAs in a single loop
        for lora_name, strength in loras:
            if lora_name != "None" and strength != 0:
                model, clip = self.lora_loader.load_lora(
                    model, clip, lora_name, strength, strength
                )
                weights_info.append(f"{lora_name}: {strength}")
        
        return (model, clip, "\n".join(weights_info))