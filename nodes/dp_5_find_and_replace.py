class DP_5_Find_And_Replace:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Text": ("STRING", {"multiline": True, "default": ""}),
            },
            "optional": {
                "rep1_with": ("STRING", {"forceInput": True}),
                "rep2_with": ("STRING", {"forceInput": True}),
                "rep3_with": ("STRING", {"forceInput": True}),
                "rep4_with": ("STRING", {"forceInput": True}),
                "rep5_with": ("STRING", {"forceInput": True}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("TEXT",)
    FUNCTION = "process"
    CATEGORY = "DP/text"

    def process(self, Text: str, **kwargs) -> tuple[str]:
        try:
            result = Text
            
            # Process each replacement if input is connected
            for i in range(1, 6):
                rep_key = f"rep{i}_with"
                if rep_key in kwargs and kwargs[rep_key] is not None:
                    search_term = f"#rep{i}"
                    result = result.replace(search_term, str(kwargs[rep_key]))
            
            return (result,)
            
        except Exception as e:
            print(f"Error in DP_5_Find_And_Replace: {str(e)}")
            return ("",) 