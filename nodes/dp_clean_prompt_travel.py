# Enhanced Prompt string cleaner node for travel
import re


class DP_Clean_Prompt_Travel:
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
        text = input_text
        # Remove special characters
        text = re.sub(r"[\(\)/\\\|\^\*\{\}\[\]]", "", text)
        # Replace underscores with spaces
        text = text.replace("_", " ")

        return (text,)
