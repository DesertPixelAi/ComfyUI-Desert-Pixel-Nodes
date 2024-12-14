import os
import random

# Move file loading to module level
def _load_category_files():
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(current_dir, "data", "crazyPrompt")
    
    categories = {}
    files = [
        "subject.txt", "composition.txt", "lighting.txt", 
        "color_palette.txt", "atmosphere.txt", "technical_details.txt",
        "additional_elements.txt", "styles.txt"
    ]
    
    for filename in files:
        file_path = os.path.join(data_dir, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                items = [line.strip() for line in f.readlines() 
                        if line.strip() and not line.startswith('#')]
                categories[filename.replace('.txt', '')] = items or ["placeholder"]
        except FileNotFoundError:
            print(f"Warning: File {filename} not found at {file_path}")
            categories[filename.replace('.txt', '')] = ["placeholder"]
        except Exception as e:
            print(f"Error reading {filename}: {str(e)}")
            categories[filename.replace('.txt', '')] = ["placeholder"]
    
    return categories

# Cache categories at module level
CATEGORIES = _load_category_files()

class Dp_Random_Crazy_Prompt_Generator:
    def __init__(self):
        self.categories = CATEGORIES  # Use cached categories

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

    def get_random_styles(self, num_styles):
        available_styles = self.categories["styles"].copy()
        if num_styles > len(available_styles):
            num_styles = len(available_styles)
        
        return random.sample(available_styles, num_styles)  # More efficient than choice + remove

    def generate(self, style_craziness):
        # Use dict for mapping instead of get()
        style_counts = {
            1: 3,
            2: 5,
            3: 7,
            4: 9,
            5: 15
        }
        num_styles = style_counts[style_craziness]

        # Single random selection for each category
        prompt_parts = {
            category: random.choice(items)
            for category, items in self.categories.items()
            if category != "styles"
        }

        # Get styles
        selected_styles = self.get_random_styles(num_styles)
        available_styles = [s for s in self.categories["styles"] if s not in selected_styles]
        medium_style = random.choice(available_styles) if available_styles else random.choice(self.categories["styles"])
        
        # Use f-string for better performance
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
        return float("NaN")

NODE_CLASS_MAPPINGS = {
    "Dp_Random_Crazy_Prompt_Generator": Dp_Random_Crazy_Prompt_Generator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Dp_Random_Crazy_Prompt_Generator": "DP Random Crazy Prompt Generator"
}