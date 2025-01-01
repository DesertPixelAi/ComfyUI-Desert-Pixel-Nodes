class DP_Lora_Strength_Controller:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "lora_01_strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01}),
                "lora_02_strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01}),
                "lora_03_strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01}),
                "lora_04_strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01}),
                "lora_05_strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("LORA_STRENGTHS",)
    RETURN_NAMES = ("strengths",)
    FUNCTION = "process"
    CATEGORY = "DP/utils"

    def process(self, lora_01_strength, lora_02_strength, lora_03_strength, lora_04_strength, lora_05_strength):
        strengths = (lora_01_strength, lora_02_strength, lora_03_strength, lora_04_strength, lora_05_strength)
        return (strengths,) 