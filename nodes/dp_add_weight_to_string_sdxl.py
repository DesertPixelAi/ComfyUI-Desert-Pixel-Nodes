class DP_Add_Weight_To_String_Sdxl:
    def __init__(self):
        self.type = "DP_Add_Weight_To_String_Sdxl"
        self.output_node = True
        self.description = "Add weight to a string for SDXL prompting"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "weight": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.1}),
            },
            "optional": {
                "text": ("STRING", {"multiline": True, "forceInput": True}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "process"
    CATEGORY = "DP/String"

    def process(self, weight, text=None):
        if not text:
            return ("",)
            
        if weight == 1.0:
            return (text,)
            
        return (f"({text}:{weight:.2f})",) 