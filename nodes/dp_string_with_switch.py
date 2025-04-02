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
            },
            "optional": {
                "String_01": ("STRING", {"multiline": True, "forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("TEXT",)
    FUNCTION = "process"
    CATEGORY = "DP/text"

    def process(self, Widget_Input: str, String_01: str = None) -> tuple[str]:
        try:
            # Convert list inputs to strings
            if isinstance(Widget_Input, list):
                Widget_Input = " ".join(str(x) for x in Widget_Input)
            if isinstance(String_01, list):
                String_01 = " ".join(str(x) for x in String_01)

            # If both inputs are empty, return empty string
            if not Widget_Input and (String_01 is None or not String_01):
                return ("",)

            # If String_01 is not connected, just return Widget_Input
            if String_01 is None:
                return (Widget_Input,)

            # Prepare String_01 by ensuring it ends with a comma
            if String_01 and not String_01.strip().endswith(","):
                String_01 = String_01.strip() + ","

            # Combine the texts
            result = f"{String_01} {Widget_Input}".strip()
            return (result,)
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
                "weight": (
                    "FLOAT",
                    {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.1},
                ),
            },
            "optional": {
                "String_01": ("STRING", {"multiline": True, "forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("TEXT",)
    FUNCTION = "process"
    CATEGORY = "DP/text"

    def process(
        self, Widget_Input: str, weight: float, String_01: str = None
    ) -> tuple[str]:
        try:
            # Convert list inputs to strings
            if isinstance(Widget_Input, list):
                Widget_Input = " ".join(str(x) for x in Widget_Input)
            if isinstance(String_01, list):
                String_01 = " ".join(str(x) for x in String_01)

            # If both inputs are empty, return empty string
            if not Widget_Input and (String_01 is None or not String_01):
                return ("",)

            # Prepare combined text
            if String_01:
                if not String_01.strip().endswith(","):
                    String_01 = String_01.strip() + ","
                combined_text = (
                    f"{String_01} {Widget_Input}" if Widget_Input else String_01
                )
            else:
                combined_text = Widget_Input if Widget_Input else ""

            # If weight is 1.0, return the text without weight formatting
            if weight == 1.0:
                return (combined_text.strip(),)

            # Apply weight if there's text
            if combined_text:
                return (f"({combined_text.strip()}:{weight:.2f})",)
            return ("",)

        except Exception as e:
            print(f"Error in DP_String_Text_With_Sdxl_Weight: {str(e)}")
            return ("",)
