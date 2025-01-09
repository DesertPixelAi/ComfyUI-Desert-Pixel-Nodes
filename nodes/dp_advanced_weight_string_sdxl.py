class DP_Advanced_Weight_String_Sdxl:
    def __init__(self):
        self.type = "DP_Advanced_Weight_String_Sdxl"
        self.output_node = True
        self.description = "Advanced weight control for SDXL prompting with multiple syntax options"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mode": (["NUMERIC", "PLUS/MINUS"],),
                "weight": ("FLOAT", {
                    "default": 1.0, 
                    "min": 0.0, 
                    "max": 2.0,
                    "step": 0.1
                }),
                "symbol_count": ("INT", {
                    "default": 1, 
                    "min": 1, 
                    "max": 3,
                    "step": 1
                }),
            },
            "optional": {
                "text": ("STRING", {"multiline": True, "forceInput": True}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "process"
    CATEGORY = "DP/String"

    def process(self, mode, weight, symbol_count, text=None):
        if not text:
            return ("",)
            
        if weight == 1.0:
            return (text,)
            
        if mode == "NUMERIC":
            return (f"({text}:{weight:.2f})",)
            
        else:
            symbols = "+" * symbol_count if weight > 1 else "-" * symbol_count
            return (f"({text}){symbols}",) 