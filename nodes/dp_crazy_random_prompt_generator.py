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

class DP_Random_Crazy_Prompt_Generator:
    def __init__(self):
        self.categories = CATEGORIES  # Use cached categories
        # Store last fixed selections
        self.fixed_selections = {
            "subject": 0,
            "composition": 0,
            "lighting": 0,
            "color_palette": 0,
            "atmosphere": 0,
            "technical_details": 0,
            "additional_elements": 0,
            "medium_style": 0,
            "styles": []
        }
        self.last_seed = 0

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
                }),
                "generation_mode": (["fixed", "randomize"], {"default": "randomize"})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "generate"
    CATEGORY = "DP/text"

    def get_random_styles(self, num_styles, rng):
        available_styles = self.categories["styles"].copy()
        if num_styles > len(available_styles):
            num_styles = len(available_styles)
        return rng.sample(available_styles, num_styles)

    def get_fixed_selection(self, items, index):
        return items[index % len(items)]

    def generate(self, style_craziness, generation_mode):
        # Create or reuse seed based on generation mode
        if generation_mode == "randomize":
            seed = random.randint(0, 0xffffffffffffffff)
            self.last_seed = seed
        else:
            seed = self.last_seed

        # Create seeded random number generator
        rng = random.Random(seed)

        style_counts = {
            1: 3,
            2: 5,
            3: 7,
            4: 9,
            5: 15
        }
        num_styles = style_counts[style_craziness]

        if generation_mode == "fixed":
            # Use fixed selections
            prompt_parts = {
                category: self.get_fixed_selection(self.categories[category], self.fixed_selections[category])
                for category in self.categories.keys()
                if category != "styles"
            }
            
            if not self.fixed_selections['styles']:
                # Initialize fixed styles if not set
                self.fixed_selections['styles'] = self.get_random_styles(num_styles, rng)
            selected_styles = self.fixed_selections['styles']
            
            # Get fixed medium style
            available_styles = [s for s in self.categories["styles"] if s not in selected_styles]
            medium_style = self.get_fixed_selection(available_styles, self.fixed_selections['medium_style']) if available_styles else self.get_fixed_selection(self.categories["styles"], 0)
        else:
            # Generate new random selections
            prompt_parts = {
                category: rng.choice(items)
                for category, items in self.categories.items()
                if category != "styles"
            }
            
            selected_styles = self.get_random_styles(num_styles, rng)
            available_styles = [s for s in self.categories["styles"] if s not in selected_styles]
            medium_style = rng.choice(available_styles) if available_styles else rng.choice(self.categories["styles"])
            
            # Store selections for fixed mode
            for category in prompt_parts:
                self.fixed_selections[category] = self.categories[category].index(prompt_parts[category])
            self.fixed_selections['styles'] = selected_styles
            self.fixed_selections['medium_style'] = available_styles.index(medium_style) if available_styles else 0

        # Construct prompt
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

