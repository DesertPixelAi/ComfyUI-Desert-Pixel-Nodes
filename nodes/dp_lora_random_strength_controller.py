class DP_Lora_Random_Strength_Controller:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "lora_01_strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01}),
                "lora_01_min": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3.0, "step": 0.01}),
                "lora_01_max": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01}),
                "lora_02_strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01}),
                "lora_02_min": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3.0, "step": 0.01}),
                "lora_02_max": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01}),
                "lora_03_strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01}),
                "lora_03_min": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3.0, "step": 0.01}),
                "lora_03_max": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01}),
                "lora_04_strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01}),
                "lora_04_min": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3.0, "step": 0.01}),
                "lora_04_max": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01}),
                "lora_05_strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01}),
                "lora_05_min": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3.0, "step": 0.01}),
                "lora_05_max": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 3.0, "step": 0.01}),
            }
        }

    RETURN_TYPES = ("LORA_RANDOM_STRENGTHS",)
    RETURN_NAMES = ("random_strengths",)
    FUNCTION = "process"
    CATEGORY = "DP/utils"

    def process(self, lora_01_strength, lora_01_min, lora_01_max,
                lora_02_strength, lora_02_min, lora_02_max,
                lora_03_strength, lora_03_min, lora_03_max,
                lora_04_strength, lora_04_min, lora_04_max,
                lora_05_strength, lora_05_min, lora_05_max):
        random_strengths = (
            (lora_01_strength, lora_01_min, lora_01_max),
            (lora_02_strength, lora_02_min, lora_02_max),
            (lora_03_strength, lora_03_min, lora_03_max),
            (lora_04_strength, lora_04_min, lora_04_max),
            (lora_05_strength, lora_05_min, lora_05_max)
        )
        return (random_strengths,) 