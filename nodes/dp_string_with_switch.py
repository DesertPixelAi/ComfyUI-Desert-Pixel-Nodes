class DP_String_With_Switch:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Widget_Input": ("STRING", {"multiline": True, "default": ""}),
                "Source": (["Widget_Input", "Text_Input"], {"default": "Widget_Input"}),
            },
            "optional": {
                "Text_Input": ("STRING", {"forceInput": True}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("TEXT",)
    FUNCTION = "process"
    CATEGORY = "DP/text"

    def process(self, Widget_Input: str, Source: str, Text_Input: str = None) -> tuple[str]:
        try:
            if Source == "Text_Input" and Text_Input is not None:
                return (Text_Input,)
            return (Widget_Input,)
        except Exception as e:
            print(f"Error in DP_String_With_Switch: {str(e)}")
            return ("",)

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
            },
            "optional": {
                "Text_Input": ("STRING", {"forceInput": True}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("TEXT",)
    FUNCTION = "process"
    CATEGORY = "DP/text"

    def process(self, Widget_Input: str, Text_Input: str = None) -> tuple[str]:
        try:
            if Text_Input is not None:
                return (Text_Input,)
            if Widget_Input:
                return (Widget_Input,)
            return ("",)
        except Exception as e:
            print(f"Error in DP_String_Text: {str(e)}")
            return ("",)
