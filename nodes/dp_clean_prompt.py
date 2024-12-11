# ComfyUI custom nodes by DreamProphet
# Enhanced Prompt string cleaner node
import re

class DP_clean_prompt:
    def __init__(self):
        pass
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_text": ("STRING", {"multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("clean_text",)
    FUNCTION = "clean"
    CATEGORY = "DP/text"

    def clean(self, input_text):
        # Process the text in steps
        text = input_text
        
        # Replace multiple newlines with spaces
        text = re.sub(r'\n+', ' ', text)
        
        # Handle weight notation patterns like (2,) or (1.5)
        # Temporarily replace valid weight notations to protect them
        text = re.sub(r'\(\s*\d+\.?\d*\s*,?\s*\)', lambda m: m.group().replace(',', '###COMMA###'), text)
        
        # Replace dots and multiple dots with commas
        text = re.sub(r'\.+', ',', text)
        
        # Replace any single quotes with spaces
        text = re.sub(r"'+", ' ', text)
        
        # First remove all spaces around commas
        text = re.sub(r'\s*,\s*', ',', text)
        
        # Then remove multiple consecutive commas
        text = re.sub(r',+', ',', text)
        
        # Fix cases where words are accidentally joined with commas (like "tech,nologically")
        text = re.sub(r'([a-zA-Z]),([a-zA-Z])', r'\1, \2', text)
        
        # Now add a single space after each comma
        text = re.sub(r',', ', ', text)
        
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Restore protected weight notation commas
        text = text.replace('###COMMA###', ',')
        
        # Clean up any trailing commas before weight notations
        text = re.sub(r',\s*(\(\d+\.?\d*,?\))', r' \1', text)
        
        # Trim whitespace from start and end
        text = text.strip()
        
        return (text,)

NODE_CLASS_MAPPINGS = {
    "DP_clean_prompt": DP_clean_prompt
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DP_clean_prompt": "DP Clean Prompt"
}