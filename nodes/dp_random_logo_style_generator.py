import os
import random


class DP_Random_Logo_Style_Generator:
    def __init__(self):
        # Get the directory where the files are located
        node_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        data_dir = os.path.join(node_dir, "data", "logo_style_generator")

        self.textures = self.load_file(os.path.join(data_dir, "texture.txt"))
        self.color_palettes = self.load_file(
            os.path.join(data_dir, "color_palette.txt")
        )
        self.lighting = self.load_file(os.path.join(data_dir, "lighting.txt"))
        self.additional_elements = self.load_file(
            os.path.join(data_dir, "additional_elements.txt")
        )
        self.styles = self.load_file(os.path.join(data_dir, "styles.txt"))

        # Store last fixed selections
        self.fixed_selections = {
            "texture": 0,
            "color": 0,
            "lighting": 0,
            "elements": 0,
            "styles": [],
        }
        self.last_seed = 0

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "style_complexity": (
                    "INT",
                    {"default": 3, "min": 1, "max": 5, "step": 1, "display": "number"},
                ),
                "generation_mode": (["fixed", "randomize"], {"default": "randomize"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "DP/text"

    def load_file(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"Error loading file {path}: {e}")
            return []

    def get_random_styles(self, num_styles, rng):
        available_styles = self.styles.copy()
        if num_styles > len(available_styles):
            num_styles = len(available_styles)
        return rng.sample(available_styles, num_styles)

    def get_fixed_selection(self, items, index):
        return items[index % len(items)]

    def generate(self, style_complexity, generation_mode):
        # Create or reuse seed based on generation mode
        if generation_mode == "randomize":
            seed = random.randint(0, 0xFFFFFFFFFFFFFFFF)
            self.last_seed = seed
        else:
            seed = self.last_seed

        # Create seeded random number generator
        rng = random.Random(seed)

        # Map complexity to number of styles
        style_counts = {1: 2, 2: 3, 3: 4, 4: 6, 5: 8}
        num_styles = style_counts[style_complexity]

        if generation_mode == "fixed":
            # Use fixed selections based on seed
            texture = f"with {self.get_fixed_selection(self.textures, self.fixed_selections['texture'])}"
            color = self.get_fixed_selection(
                self.color_palettes, self.fixed_selections["color"]
            )
            lighting = self.get_fixed_selection(
                self.lighting, self.fixed_selections["lighting"]
            )
            elements = self.get_fixed_selection(
                self.additional_elements, self.fixed_selections["elements"]
            )

            if not self.fixed_selections["styles"]:
                # Initialize fixed styles if not set
                self.fixed_selections["styles"] = self.get_random_styles(
                    num_styles, rng
                )
            selected_styles = self.fixed_selections["styles"]
        else:
            # Generate new random selections
            texture = f"with {rng.choice(self.textures)}"
            color = rng.choice(self.color_palettes)
            lighting = rng.choice(self.lighting)
            elements = rng.choice(self.additional_elements)
            selected_styles = self.get_random_styles(num_styles, rng)

            # Store selections for fixed mode
            self.fixed_selections["texture"] = self.textures.index(
                texture[5:]
            )  # Remove "with " prefix
            self.fixed_selections["color"] = self.color_palettes.index(color)
            self.fixed_selections["lighting"] = self.lighting.index(lighting)
            self.fixed_selections["elements"] = self.additional_elements.index(elements)
            self.fixed_selections["styles"] = selected_styles

        # Construct prompt
        prompt = (
            f"{texture}, {color}, "
            f"{lighting}, {elements}, "
            f"ultra detailed, professional 3D rendering, octane render, "
            f"in the style of {', '.join(selected_styles)}"
        )

        return (prompt,)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")
