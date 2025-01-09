# Enhanced Prompt string cleaner node
import re

class DP_clean_prompt:
    def __init__(self):
        pass
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_text": ("STRING", {"multiline": True, "forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("clean_text",)
    FUNCTION = "clean"
    CATEGORY = "DP/text"

    def clean(self, input_text):
        # Process the text in steps
        text = input_text
        
        # Replace escaped parentheses with temporary markers
        text = text.replace(r'\(', '###LEFTPAR###').replace(r'\)', '###RIGHTPAR###')
        
        # Replace multiple newlines with single newline (instead of space)
        text = re.sub(r'\n{2,}', '\n', text)
        
        # Replace underscores with spaces
        text = text.replace('_', ' ')
        
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
        
        # Restore escaped parentheses
        text = text.replace('###LEFTPAR###', '(').replace('###RIGHTPAR###', ')')
        
        # Remove leading/trailing commas, spaces, and dots
        text = re.sub(r'^[,\s\.]+', '', text)
        text = re.sub(r'[,\s\.]+$', '', text)
        
        return (text,)

