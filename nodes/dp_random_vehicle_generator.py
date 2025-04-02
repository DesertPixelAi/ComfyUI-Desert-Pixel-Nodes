import os
import random
import re


class DP_Random_Vehicle_Generator:
    def __init__(self):
        # Get the directory where the files are located
        node_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(node_dir, "data", "vehicle_types")

        # Load all vehicle component descriptions
        self.body_types = self.load_file(os.path.join(data_dir, "body_type.txt"))
        self.tires = self.load_file(os.path.join(data_dir, "tires_description.txt"))
        self.camera_angles = self.load_file(
            os.path.join(data_dir, "vehicle_camera_angle_and_filter.txt")
        )
        self.color_themes = self.load_file(
            os.path.join(data_dir, "vehicle_color_theme.txt")
        )
        self.scene_descriptions = self.load_file(
            os.path.join(data_dir, "vehicle_scene_description.txt")
        )
        self.art_styles = self.load_file(
            os.path.join(data_dir, "vehicle_art_styles.txt")
        )

        # Store last fixed selections
        self.fixed_selections = {
            "body": 0,
            "tires": 0,
            "camera": 0,
            "color": 0,
            "scene": 0,
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
                return [
                    line.strip()
                    for line in f
                    if line.strip() and not line.strip().startswith("#")
                ]
        except Exception as e:
            print(f"Error loading file {path}: {e}")
            return []

    def get_random_styles(self, num_styles, rng):
        available_styles = self.art_styles.copy()
        if num_styles > len(available_styles):
            num_styles = len(available_styles)
        return rng.sample(available_styles, num_styles)

    def get_fixed_selection(self, items, index):
        return items[index % len(items)]

    def clean_prompt(self, prompt):
        # Remove multiple spaces
        cleaned = " ".join(prompt.split())
        # Remove spaces before punctuation
        cleaned = re.sub(r"\s+([,.!?])", r"\1", cleaned)
        # Ensure single space after punctuation
        cleaned = re.sub(r"([,.!?])\s*", r"\1 ", cleaned)
        # Remove trailing/leading whitespace
        cleaned = cleaned.strip()
        return cleaned

    def generate(self, style_complexity, generation_mode):
        if generation_mode == "randomize":
            seed = random.randint(0, 0xFFFFFFFFFFFFFFFF)
            self.last_seed = seed
        else:
            seed = self.last_seed

        rng = random.Random(seed)

        # Map complexity to number of styles (1=1, 5=10)
        style_counts = {1: 1, 2: 3, 3: 5, 4: 7, 5: 10}
        num_styles = style_counts[style_complexity]

        if generation_mode == "fixed":
            # Use fixed selections
            body = self.get_fixed_selection(
                self.body_types, self.fixed_selections["body"]
            )
            tires = self.get_fixed_selection(self.tires, self.fixed_selections["tires"])
            camera = self.get_fixed_selection(
                self.camera_angles, self.fixed_selections["camera"]
            )
            color = self.get_fixed_selection(
                self.color_themes, self.fixed_selections["color"]
            )
            scene = self.get_fixed_selection(
                self.scene_descriptions, self.fixed_selections["scene"]
            )

            if not self.fixed_selections["styles"]:
                self.fixed_selections["styles"] = self.get_random_styles(
                    num_styles, rng
                )
            selected_styles = self.fixed_selections["styles"]
        else:
            # Generate new random selections
            body = rng.choice(self.body_types)
            tires = rng.choice(self.tires)
            camera = rng.choice(self.camera_angles)
            color = rng.choice(self.color_themes)
            scene = rng.choice(self.scene_descriptions)
            selected_styles = self.get_random_styles(num_styles, rng)

            # Store selections for fixed mode
            self.fixed_selections["body"] = self.body_types.index(body)
            self.fixed_selections["tires"] = self.tires.index(tires)
            self.fixed_selections["camera"] = self.camera_angles.index(camera)
            self.fixed_selections["color"] = self.color_themes.index(color)
            self.fixed_selections["scene"] = self.scene_descriptions.index(scene)
            self.fixed_selections["styles"] = selected_styles

        # Construct the prompt
        prompt = (
            f"epic vehicle photography, big cinematic concept vehicle in the center of the frame, "
            f"{camera},the vehicle designed with {body}, and{tires}, "
            f"{color}, {scene}, vehicle concept photo, "
            f"highly detailed, sharp focus, in the style of {', '.join(selected_styles)}"
        )

        # Clean and format the prompt
        cleaned_prompt = self.clean_prompt(prompt)

        return (cleaned_prompt,)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")
