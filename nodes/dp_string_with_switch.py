class DP_String_With_Switch:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "UserInput": ("STRING", {"multiline": True, "default": ""}),
                "Source": (["UserInput", "PipeInput"], {"default": "UserInput"}),
            },
            "optional": {
                "PipeInText": ("STRING",),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("TEXT",)
    FUNCTION = "process"
    CATEGORY = "DP/string"

    def process(self, UserInput: str, Source: str, PipeInText: str = None) -> tuple[str]:
        try:
            if Source == "PipeInput" and PipeInText is not None:
                return (PipeInText,)
            return (UserInput,)
        except Exception as e:
            print(f"Error in DP_String_With_Switch: {str(e)}")
            return ("",)
