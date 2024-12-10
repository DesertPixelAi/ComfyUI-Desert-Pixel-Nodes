import os
import random

class Dp_Random_Crazy_Prompt_Generator:
    def __init__(self):
        self.categories = {
            "subject": self.load_items("subject.txt"),
            "composition": self.load_items("composition.txt"),
            "lighting": self.load_items("lighting.txt"),
            "color_palette": self.load_items("color_palette.txt"),
            "atmosphere": self.load_items("atmosphere.txt"),
            "technical_details": self.load_items("technical_details.txt"),
            "additional_elements": self.load_items("additional_elements.txt"),
            "styles": self.load_items("styles.txt")
        }

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "style_craziness": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 5,
                    "step": 1,
                    "display": "number"
                })
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "generate"
    CATEGORY = "DP/prompt"

    def load_items(self, filename):
        # Get the path to the package root directory
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Construct path to the data file
        file_path = os.path.join(current_dir, "data", "crazyPrompt", filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                items = [line.strip() for line in f.readlines() 
                        if line.strip() and not line.startswith('#')]
                if not items:
                    print(f"Warning: No items found in {filename}")
                    return ["placeholder"]
                return items
        except FileNotFoundError:
            print(f"Warning: File {filename} not found at {file_path}")
            return ["placeholder"]
        except Exception as e:
            print(f"Error reading {filename}: {str(e)}")
            return ["placeholder"]

    def get_random_styles(self, num_styles):
        # Get unique random styles
        available_styles = self.categories["styles"].copy()
        if num_styles > len(available_styles):
            num_styles = len(available_styles)
        
        selected_styles = []
        for _ in range(num_styles):
            if not available_styles:
                break
            style = random.choice(available_styles)
            selected_styles.append(style)
            available_styles.remove(style)
        
        return selected_styles

    def generate(self, style_craziness):
        # Map style_craziness to number of styles
        style_counts = {
            1: 3,
            2: 5,
            3: 7,
            4: 9,
            5: 15
        }
        num_styles = style_counts.get(style_craziness, 3)

        # Generate random selections for each category
        prompt_parts = {
            "subject": random.choice(self.categories["subject"]),
            "composition": random.choice(self.categories["composition"]),
            "lighting": random.choice(self.categories["lighting"]),
            "color_palette": random.choice(self.categories["color_palette"]),
            "atmosphere": random.choice(self.categories["atmosphere"]),
            "technical_details": random.choice(self.categories["technical_details"]),
            "additional_elements": random.choice(self.categories["additional_elements"])
        }

        # Get multiple unique styles
        selected_styles = self.get_random_styles(num_styles)
        
        # Get an additional random style for the medium type at the start
        available_styles = [s for s in self.categories["styles"] if s not in selected_styles]
        medium_style = random.choice(available_styles) if available_styles else random.choice(self.categories["styles"])
        
        # Construct the prompt with medium style at the start
        prompt = (
            f"{medium_style}, "
            f"{prompt_parts['subject']}, "
            f"{prompt_parts['composition']}, "
            f"{prompt_parts['lighting']}, "
            f"{prompt_parts['color_palette']}, "
            f"{prompt_parts['atmosphere']}, "
            f"{prompt_parts['technical_details']}, "
            f"{prompt_parts['additional_elements']}, "
            f"in the style of {', '.join(selected_styles)}"
        )

        return (prompt,)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        # Ensure we generate a new random prompt each time
        return float("NaN")

NODE_CLASS_MAPPINGS = {
    "Dp_Random_Crazy_Prompt_Generator": Dp_Random_Crazy_Prompt_Generator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Dp_Random_Crazy_Prompt_Generator": "DP Random Crazy Prompt Generator"
}