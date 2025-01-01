import re
import logging

logger = logging.getLogger('DP_Nodes')

class DP_Strings_Connector:
    def __init__(self):
        pass
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "separator": ("STRING", {"default": " ", "multiline": False}),
            },
            "optional": {
                "string1": ("STRING", {"multiline": True, "forceInput": True}),
                "string2": ("STRING", {"multiline": True, "forceInput": True}),
                "string3": ("STRING", {"multiline": True, "forceInput": True}),
                "string4": ("STRING", {"multiline": True, "forceInput": True}),
                "string5": ("STRING", {"multiline": True, "forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "connect_strings"
    CATEGORY = "DP/text"

    def connect_strings(self, separator=" ", string1=None, string2=None, string3=None, string4=None, string5=None):
        try:
            # Collect all non-None strings
            strings = []
            for s in [string1, string2, string3, string4, string5]:
                if s is not None:
                    # Clean the string: remove extra whitespace, newlines, etc.
                    cleaned = re.sub(r'\s+', ' ', s.strip())
                    if cleaned:  # Only add non-empty strings
                        strings.append(cleaned)
            
            # If no valid strings, return empty string
            if not strings:
                logger.debug("No valid strings to connect")
                return ("",)
            
            # Use space if separator is empty
            sep = " " if not separator.strip() else separator.strip()
            
            # Join strings with separator
            result = sep.join(strings)
            
            # Clean up the final string
            result = re.sub(r'\s*[,]+\s*', ', ', result)  # Fix comma spacing
            result = re.sub(r'\s*[.]+\s*', '. ', result)  # Fix period spacing
            result = re.sub(r'\s+', ' ', result)  # Remove multiple spaces
            result = result.strip()  # Remove leading/trailing whitespace
            
            logger.debug(f"Connected strings result: '{result}'")
            return (result,)
            
        except Exception as e:
            logger.error(f"Error connecting strings: {str(e)}")
            return ("",)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

# Node registration
NODE_CLASS_MAPPINGS = {
    "DP_Strings_Connector": DP_Strings_Connector
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DP_Strings_Connector": "Strings Connector"
} 