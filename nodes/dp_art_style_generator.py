import json
import os
import random
from server import PromptServer

class DP_Art_Style_Generator:
    def __init__(self):
        self.current_index = 0
        self.styles = self.load_styles()
        self.id = str(random.randint(0, 2**64))
        self.color = "#121317"
        self.bgcolor = "#006994"
        self.last_style = None
        self.last_mode = None
        self.last_index = None
        self.input_processed = False
        
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
                    "step": 1,
                    "display": "number"
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
    RETURN_NAMES = ("medium_type", "positive_prompt", "negative_prompt",)
    FUNCTION = "generate"
    CATEGORY = "DP/text"

    def generate(self, style_name, style_index_control, index, positive_weight, unique_id):
        if not self.styles:
            return ("none", "", "")

        if style_name == "None" and style_index_control == "fixed":
            return ("", "", "")

        current_color = getattr(self, 'color', "#121317")
        current_bgcolor = getattr(self, 'bgcolor', "#006994")
        random_state = random.getstate()

        try:
            num_styles = len(self.styles)
            next_index = self.current_index  # Start from current position

            # Detect changes
            mode_changed = style_index_control != self.last_mode
            index_changed = index != self.last_index
            style_changed = style_name != self.last_style

            # Handle user input changes first
            if (index_changed or style_changed) and style_index_control == "fixed":
                if index_changed:
                    # User changed index directly
                    next_index = max(0, min(index, num_styles - 1))
                    if next_index == 0:  # Skip "None"
                        next_index = 1
                elif style_changed and style_name != "None":
                    # User selected a style
                    for i, style in enumerate(self.styles):
                        if style["name"] == style_name:
                            next_index = i
                            break
                self.current_index = next_index
            
            # Handle mode-specific behavior
            elif style_index_control == "randomize":
                while True:
                    next_index = random.randint(0, num_styles - 1)
                    if next_index != self.current_index and next_index != 0:
                        break
                self.current_index = next_index
            elif style_index_control == "increment":
                next_index = (self.current_index + 1) % num_styles
                if next_index == 0:  # Skip "None"
                    next_index = 1
                self.current_index = next_index
            elif style_index_control == "decrement":
                next_index = (self.current_index - 1) % num_styles
                if next_index == 0:  # Skip "None"
                    next_index = num_styles - 1
                self.current_index = next_index

            # Update tracking
            self.last_mode = style_index_control
            self.last_index = next_index
            self.last_style = style_name

            selected_style = self.styles[next_index]

            # Update UI
            try:
                PromptServer.instance.send_sync("update_art_style", {
                    "node_id": unique_id,
                    "style_name": selected_style["name"],
                    "index": next_index,
                    "color": current_color,
                    "bgcolor": current_bgcolor
                })
            except Exception as e:
                print(f"Error sending WebSocket message: {str(e)}")

            # Process positive prompt with weight
            positive_prompt = selected_style.get("positive", "")
            if positive_prompt:
                if positive_weight != 1.0:
                    # Format weight to always show one decimal place
                    formatted_weight = "{:.1f}".format(positive_weight)
                    positive_prompt = f"({positive_prompt}:{formatted_weight})"

            return (
                selected_style.get("name", "none"),
                positive_prompt,
                selected_style.get("negative", "")
            )

        finally:
            random.setstate(random_state)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        if kwargs.get("style_index_control") in ["randomize", "increment", "decrement"] or \
           "index" in kwargs or \
           "style_name" in kwargs:
            return float("NaN")
        return False 