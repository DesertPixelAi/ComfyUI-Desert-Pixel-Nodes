import re


class DP_2_String_Switch:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "String_01": ("STRING", {"multiline": True, "default": ""}),
                "String_02": ("STRING", {"multiline": True, "default": ""}),
                "Source": (["String_01", "String_02"], {"default": "String_01"}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("TEXT",)
    FUNCTION = "process"
    CATEGORY = "DP/text"

    def process(self, String_01: str, String_02: str, Source: str) -> tuple[str]:
        try:
            # Convert list inputs to strings
            if isinstance(String_01, list):
                String_01 = " ".join(str(x) for x in String_01)
            if isinstance(String_02, list):
                String_02 = " ".join(str(x) for x in String_02)
                
            if Source == "String_02":
                return (String_02,)
            return (String_01,)
        except Exception as e:
            print(f"Error in DP_2_String_Switch: {str(e)}")
            return ("",)

class DP_String_Text:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Widget_Input": ("STRING", {"multiline": True, "default": ""}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("TEXT",)
    FUNCTION = "process"
    CATEGORY = "DP/text"

    def process(self, Widget_Input: str) -> tuple[str]:
        try:
            # Convert list inputs to strings
            if isinstance(Widget_Input, list):
                Widget_Input = " ".join(str(x) for x in Widget_Input)
                
            if Widget_Input:
                return (Widget_Input,)
            return ("",)
        except Exception as e:
            print(f"Error in DP_String_Text: {str(e)}")
            return ("",)

class DP_String_Text_With_Sdxl_Weight:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Widget_Input": ("STRING", {"multiline": True, "default": ""}),
                "weight": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.1}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("TEXT",)
    FUNCTION = "process"
    CATEGORY = "DP/text"

    def process(self, Widget_Input: str, weight: float) -> tuple[str]:
        try:
            # Convert list inputs to strings
            if isinstance(Widget_Input, list):
                Widget_Input = " ".join(str(x) for x in Widget_Input)
                
            if Widget_Input:
                return (f"({Widget_Input}:{weight})",)
            return ("",)
        except Exception as e:
            print(f"Error in DP_String_Text_With_Sdxl_Weight: {str(e)}")
            return ("",)
