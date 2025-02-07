from server import PromptServer
import random

class DP_10_String_Switch_Or_Connect:
    def __init__(self):
        self.selected_index = 1
        self.id = str(random.randint(0, 2**64))
        
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mode": ([
                    "Switch", 
                    "Connected",
                    "Connected with comma",
                    "Connected with line break",
                    "Connected with line break+",
                    "Switch Remove neg"
                ], {"default": "Switch"}),
                "index": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1}),
            },
            "optional": {
                "String_01": ("STRING", {"multiline": True, "forceInput": True}),
                "String_02": ("STRING", {"multiline": True, "forceInput": True}),
                "String_03": ("STRING", {"multiline": True, "forceInput": True}),
                "String_04": ("STRING", {"multiline": True, "forceInput": True}),
                "String_05": ("STRING", {"multiline": True, "forceInput": True}),
                "String_06": ("STRING", {"multiline": True, "forceInput": True}),
                "String_07": ("STRING", {"multiline": True, "forceInput": True}),
                "String_08": ("STRING", {"multiline": True, "forceInput": True}),
                "String_09": ("STRING", {"multiline": True, "forceInput": True}),
                "String_10": ("STRING", {"multiline": True, "forceInput": True}),
            }
        }
    
    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("TEXT", "CURRENT_INDEX",)
    FUNCTION = "process"
    CATEGORY = "DP/text"

    def process(self, mode: str, index: int, **kwargs) -> tuple[str, int]:
        try:
            # Get all connected strings
            connected_strings = {}
            for i in range(1, 11):
                string_key = f"String_{i:02d}"
                if string_key in kwargs and kwargs[string_key] is not None:
                    value = kwargs[string_key]
                    if isinstance(value, list):
                        value = " ".join(str(x) for x in value)
                    value = str(value).strip()
                    if value:  # Only add non-empty strings
                        connected_strings[i] = value

            if not connected_strings:
                return ("", 1)

            if mode == "Switch" or mode == "Switch Remove neg":
                # Format the index with leading zero
                selected_key = f"String_{index:02d}"  # This ensures "10" becomes "String_10"
                selected = kwargs.get(selected_key)
                
                if selected is not None:
                    if isinstance(selected, list):
                        selected = " ".join(str(x) for x in selected)
                    selected = str(selected).strip()
                    
                    # Handle "Switch Remove neg" mode
                    if mode == "Switch Remove neg" and selected:
                        neg_index = selected.find("--neg")
                        if neg_index != -1:
                            selected = selected[:neg_index].strip()
                else:
                    selected = ""
                    
                return (selected, index)

            # Get sorted strings
            sorted_strings = [connected_strings[k] for k in sorted(connected_strings.keys())]

            if mode == "Connected":
                result = " ".join(sorted_strings)
            elif mode == "Connected with comma":
                result = ", ".join(sorted_strings)
            elif mode == "Connected with line break":
                result = "\n".join(sorted_strings)
            elif mode == "Connected with line break+":
                result = "\n\n".join(sorted_strings)
            else:
                result = ""

            return (result, index)
            
        except Exception as e:
            print(f"Error in DP_10_String_Switch_Or_Connect: {str(e)}")
            return ("", 1)

class DP_3_String_Switch_Or_Connect:
    def __init__(self):
        self.selected_index = 1
        self.id = str(random.randint(0, 2**64))
        
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mode": ([
                    "Switch", 
                    "Connected",
                    "Connected with comma",
                    "Connected with line break",
                    "Connected with line break+"
                ], {"default": "Switch"}),
                "index": ("INT", {"default": 1, "min": 1, "max": 3, "step": 1}),
            },
            "optional": {
                "String_01": ("STRING", {"multiline": True, "forceInput": True}),
                "String_02": ("STRING", {"multiline": True, "forceInput": True}),
                "String_03": ("STRING", {"multiline": True, "forceInput": True}),
            }
        }
    
    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("TEXT", "CURRENT_INDEX",)
    FUNCTION = "process"
    CATEGORY = "DP/text"

    def process(self, mode: str, index: int, **kwargs) -> tuple[str, int]:
        try:
            # Get all connected strings
            connected_strings = {}
            for i in range(1, 4):
                string_key = f"String_{i:02d}"
                if string_key in kwargs and kwargs[string_key] is not None:
                    value = kwargs[string_key]
                    if isinstance(value, list):
                        value = " ".join(str(x) for x in value)
                    value = str(value).strip()
                    if value:  # Only add non-empty strings
                        connected_strings[i] = value

            if not connected_strings:
                return ("", 1)

            if mode == "Switch":
                selected_key = f"String_{index:02d}"
                selected = kwargs.get(selected_key)
                
                if selected is not None:
                    if isinstance(selected, list):
                        selected = " ".join(str(x) for x in selected)
                    selected = str(selected).strip()
                else:
                    selected = ""
                    
                return (selected, index)

            # Get sorted strings
            sorted_strings = [connected_strings[k] for k in sorted(connected_strings.keys())]

            if mode == "Connected":
                result = " ".join(sorted_strings)
            elif mode == "Connected with comma":
                result = ", ".join(sorted_strings)
            elif mode == "Connected with line break":
                result = "\n".join(sorted_strings)
            elif mode == "Connected with line break+":
                result = "\n\n".join(sorted_strings)
            else:
                result = ""

            return (result, index)
            
        except Exception as e:
            print(f"Error in DP_3_String_Switch_Or_Connect: {str(e)}")
            return ("", 1)

class DP_5_String_Switch_Or_Connect:
    def __init__(self):
        self.selected_index = 1
        self.id = str(random.randint(0, 2**64))
        
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mode": ([
                    "Switch", 
                    "Connected",
                    "Connected with comma",
                    "Connected with line break",
                    "Connected with line break+"
                ], {"default": "Switch"}),
                "index": ("INT", {"default": 1, "min": 1, "max": 5, "step": 1}),
            },
            "optional": {
                "String_01": ("STRING", {"multiline": True, "forceInput": True}),
                "String_02": ("STRING", {"multiline": True, "forceInput": True}),
                "String_03": ("STRING", {"multiline": True, "forceInput": True}),
                "String_04": ("STRING", {"multiline": True, "forceInput": True}),
                "String_05": ("STRING", {"multiline": True, "forceInput": True}),
            }
        }
    
    RETURN_TYPES = ("STRING", "INT",)
    RETURN_NAMES = ("TEXT", "CURRENT_INDEX",)
    FUNCTION = "process"
    CATEGORY = "DP/text"

    def process(self, mode: str, index: int, **kwargs) -> tuple[str, int]:
        try:
            # Get all connected strings
            connected_strings = {}
            for i in range(1, 6):
                string_key = f"String_{i:02d}"
                if string_key in kwargs and kwargs[string_key] is not None:
                    value = kwargs[string_key]
                    if isinstance(value, list):
                        value = " ".join(str(x) for x in value)
                    value = str(value).strip()
                    if value:  # Only add non-empty strings
                        connected_strings[i] = value

            if not connected_strings:
                return ("", 1)

            if mode == "Switch":
                selected_key = f"String_{index:02d}"
                selected = kwargs.get(selected_key)
                
                if selected is not None:
                    if isinstance(selected, list):
                        selected = " ".join(str(x) for x in selected)
                    selected = str(selected).strip()
                else:
                    selected = ""
                    
                return (selected, index)

            # Get sorted strings
            sorted_strings = [connected_strings[k] for k in sorted(connected_strings.keys())]

            if mode == "Connected":
                result = " ".join(sorted_strings)
            elif mode == "Connected with comma":
                result = ", ".join(sorted_strings)
            elif mode == "Connected with line break":
                result = "\n".join(sorted_strings)
            elif mode == "Connected with line break+":
                result = "\n\n".join(sorted_strings)
            else:
                result = ""

            return (result, index)
            
        except Exception as e:
            print(f"Error in DP_5_String_Switch_Or_Connect: {str(e)}")
            return ("", 1) 