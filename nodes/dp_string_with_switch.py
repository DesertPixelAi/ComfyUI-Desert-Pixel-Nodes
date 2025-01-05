import re

class DP_String_With_Switch:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Widget_Text": ("STRING", {"multiline": True, "default": ""}),
                "Source": (["Widget_Text", "Text_Input", "Connect_Both_withComma"], {"default": "Widget_Text"}),
            },
            "optional": {
                "Text_Input": ("STRING", {"forceInput": True}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("TEXT",)
    FUNCTION = "process"
    CATEGORY = "DP/text"

    def process(self, Widget_Text: str, Source: str, Text_Input: str = None) -> tuple[str]:
        try:
            # Convert list inputs to strings
            if isinstance(Widget_Text, list):
                Widget_Text = " ".join(str(x) for x in Widget_Text)
            if isinstance(Text_Input, list):
                Text_Input = " ".join(str(x) for x in Text_Input)
                
            if Source == "Text_Input" and Text_Input is not None:
                return (Text_Input,)
            elif Source == "Connect_Both_withComma":
                # If either string is empty, return the non-empty one
                if not Text_Input:
                    return (Widget_Text,) if Widget_Text else ("",)
                if not Widget_Text:
                    return (Text_Input,)
                
                # Check if Text_Input ends with comma
                if Text_Input.strip().endswith(','):
                    combined = f"{Text_Input} {Widget_Text}"
                else:
                    combined = f"{Text_Input}, {Widget_Text}"
                return (combined,)
            return (Widget_Text,)
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
                "Text_Input": ("STRING", {"forceInput": True}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("TEXT",)
    FUNCTION = "process"
    CATEGORY = "DP/text"

    def process(self, Widget_Input: str, Text_Input: str = None) -> tuple[str]:
        try:
            # Convert list inputs to strings
            if isinstance(Widget_Input, list):
                Widget_Input = " ".join(str(x) for x in Widget_Input)
            if isinstance(Text_Input, list):
                Text_Input = " ".join(str(x) for x in Text_Input)
                
            if Text_Input is not None:
                return (Text_Input,)
            if Widget_Input:
                return (Widget_Input,)
            return ("",)
        except Exception as e:
            print(f"Error in DP_String_Text: {str(e)}")
            return ("",)

class DP_5_String_Switch:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Source": (["String_1", "String_2", "String_3", "String_4", "String_5", "all_connected"], {"default": "String_1"}),
            },
            "optional": {
                "String_1": ("STRING", {"multiline": True, "forceInput": True}),
                "String_2": ("STRING", {"multiline": True, "forceInput": True}),
                "String_3": ("STRING", {"multiline": True, "forceInput": True}),
                "String_4": ("STRING", {"multiline": True, "forceInput": True}),
                "String_5": ("STRING", {"multiline": True, "forceInput": True}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("TEXT",)
    FUNCTION = "process"
    CATEGORY = "DP/text"

    def process(self, Source: str, String_1=None, String_2=None, String_3=None, String_4=None, String_5=None) -> tuple[str]:
        try:
            if Source == "all_connected":
                # Collect all non-None and non-empty strings
                strings = []
                for s in [String_1, String_2, String_3, String_4, String_5]:
                    if s is not None and str(s).strip():  # Check if string is not None and not empty after stripping
                        # Handle list inputs
                        if isinstance(s, list):
                            s = " ".join(str(x) for x in s if str(x).strip())
                        # Clean the string
                        cleaned = str(s).strip()
                        if cleaned:  # Only add non-empty strings
                            strings.append(cleaned)
                
                if not strings:  # If no valid strings found
                    return ("",)
                
                # Join strings with comma and space
                result = ", ".join(strings)
                
                # Clean up the final string
                result = result.replace('\n', ' ')  # Replace newlines with spaces
                result = re.sub(r'\s*,\s*,\s*', ', ', result)  # Remove double commas
                result = re.sub(r'\s+', ' ', result)  # Remove multiple spaces
                result = re.sub(r'\s*,\s*', ', ', result)  # Ensure proper comma spacing
                result = result.strip()  # Remove leading/trailing whitespace
                
                return (result,)
            else:
                # Original switch behavior
                string_map = {
                    "String_1": String_1,
                    "String_2": String_2,
                    "String_3": String_3,
                    "String_4": String_4,
                    "String_5": String_5
                }
                
                selected = string_map[Source]
                
                if isinstance(selected, list):
                    selected = " ".join(str(x) for x in selected)
                    
                return (selected if selected is not None else "",)
            
        except Exception as e:
            print(f"Error in DP_5_String_Switch: {str(e)}")
            return ("",)

class DP_10_String_Switch:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Source": (["String_1", "String_2", "String_3", "String_4", "String_5", 
                          "String_6", "String_7", "String_8", "String_9", "String_10", 
                          "all_connected"], {"default": "String_1"}),
            },
            "optional": {
                "String_1": ("STRING", {"multiline": True, "forceInput": True}),
                "String_2": ("STRING", {"multiline": True, "forceInput": True}),
                "String_3": ("STRING", {"multiline": True, "forceInput": True}),
                "String_4": ("STRING", {"multiline": True, "forceInput": True}),
                "String_5": ("STRING", {"multiline": True, "forceInput": True}),
                "String_6": ("STRING", {"multiline": True, "forceInput": True}),
                "String_7": ("STRING", {"multiline": True, "forceInput": True}),
                "String_8": ("STRING", {"multiline": True, "forceInput": True}),
                "String_9": ("STRING", {"multiline": True, "forceInput": True}),
                "String_10": ("STRING", {"multiline": True, "forceInput": True}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("TEXT",)
    FUNCTION = "process"
    CATEGORY = "DP/text"

    def process(self, Source: str, **kwargs) -> tuple[str]:
        try:
            def clean_string(s):
                if isinstance(s, list):
                    return " ".join(str(x).strip() for x in s if str(x).strip())
                return str(s).strip()

            if Source == "all_connected":
                # Collect all non-None and non-empty strings
                strings = []
                for i in range(1, 11):
                    s = kwargs.get(f"String_{i}")
                    if s is not None:
                        cleaned = clean_string(s)
                        if cleaned:
                            # Check if previous string ended with comma
                            if strings and not strings[-1].endswith(','):
                                strings.append(f", {cleaned}")
                            else:
                                strings.append(cleaned)
                
                # Join all strings
                if strings:
                    result = "".join(strings)
                    # Remove leading comma if present
                    return (result.lstrip(", "),)
                return ("",)
            
            # Single string mode
            selected = kwargs.get(Source)
            if selected is not None:
                return (clean_string(selected),)
            else:
                print(f"Warning: Selected input '{Source}' is not connected")
                return ("",)
            
        except Exception as e:
            print(f"Error in DP_10_String_Switch: {str(e)}")
            return ("",)
