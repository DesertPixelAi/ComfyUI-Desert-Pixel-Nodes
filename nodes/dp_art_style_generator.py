import json
import os
import random
from server import PromptServer

class DP_Art_Style_Generator:
    def __init__(self):
        self.styles = self.load_styles()
        self.current_index = 1  # Start at 1 since 0 is "None"
        self.id = str(random.randint(0, 2**64))

    def load_styles(self):
        try:
            node_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            json_path = os.path.join(node_dir, "data", "art_styles", "art_styles_v01.json")
            
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("styles", [])
        except Exception as e:
            print(f"Error loading art styles: {e}")
            return []

    @classmethod
    def INPUT_TYPES(cls):
        styles = ["None"] + [style["name"] for style in cls().styles]
        return {
            "required": {
                "style_name": (styles,),
                "style_index_control": (["fixed", "randomize", "increment", "decrement"],),
                "index": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 9999,
                    "step": 1
                }),
                "positive_weight": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 10.0,
                    "step": 0.1
                }),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID"
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING",)
    RETURN_NAMES = ("style_name", "positive_prompt", "negative_prompt",)
    FUNCTION = "generate"
    CATEGORY = "DP/text"

    def generate(self, style_name, style_index_control, index, positive_weight, unique_id):
        if not self.styles:
            return ("none", "", "")

        if style_name == "None" and style_index_control == "fixed":
            return ("", "", "")

        num_styles = len(self.styles)
        next_index = self.current_index

        # Handle fixed mode and manual style selection
        if style_index_control == "fixed":
            if style_name != "None":
                # Find index of selected style
                selected_index = next(
                    (i for i, s in enumerate(self.styles) if s["name"] == style_name),
                    self.current_index
                )
                next_index = selected_index
        else:
            # Handle mode-specific behavior
            if style_index_control == "randomize":
                while True:
                    next_index = random.randint(1, num_styles - 1)
                    if next_index != self.current_index or num_styles <= 2:
                        break
            elif style_index_control == "increment":
                next_index = (self.current_index + 1) % num_styles
                if next_index == 0:  # Skip "None"
                    next_index = 1
            elif style_index_control == "decrement":
                next_index = (self.current_index - 1)
                if next_index <= 0:
                    next_index = num_styles - 1

        # Update current index
        self.current_index = next_index
        selected_style = self.styles[next_index]

        # Process positive prompt with weight
        positive_prompt = selected_style.get("positive", "")
        if positive_prompt and positive_weight != 1.0:
            formatted_weight = "{:.1f}".format(positive_weight)
            positive_prompt = f"({positive_prompt}:{formatted_weight})"

        # Update UI
        try:
            PromptServer.instance.send_sync("dp_style_update", {
                "node_id": unique_id,
                "index": next_index,
                "style_name": selected_style["name"]
            })
        except Exception as e:
            print(f"Error sending WebSocket message: {str(e)}")

        return (
            selected_style.get("name", "none"),
            positive_prompt,
            selected_style.get("negative", "")
        ) 