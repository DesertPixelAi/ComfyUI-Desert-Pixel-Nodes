import random
import os
import re

class DP_Random_Psychedelic_Punk_Generator:
    def __init__(self):
        # Get the directory where the files are located
        node_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(node_dir, "data", "psychedelic_punk")
        
        # Add gender list
        self.gender = ["male", "female"]
        
        # Load all text files
        self.subject = self.load_file(os.path.join(data_dir, "subject.txt"))
        self.setting = self.load_file(os.path.join(data_dir, "setting.txt"))
        self.style = self.load_file(os.path.join(data_dir, "style.txt"))
        self.color_palette = self.load_file(os.path.join(data_dir, "color_palette.txt"))
        self.lighting = self.load_file(os.path.join(data_dir, "lighting.txt"))
        self.additional_elements = self.load_file(os.path.join(data_dir, "additional_elements.txt"))
        self.final_touch = self.load_file(os.path.join(data_dir, "final_touch.txt"))
        self.camera_angles = self.load_file(os.path.join(data_dir, "camera_angles.txt"))
        
        # Store last fixed selections
        self.fixed_selections = {
            "subject": 0,
            "setting": 0,
            "color_palette": 0,
            "lighting": 0,
            "additional_elements": 0,
            "styles": [],
            "final_touch": 0,
            "gender": 0,  # Add gender to fixed selections
            "camera_angle": 0  # Add camera angle to fixed selections
        }
        self.last_seed = 0

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "style_complexity": ("INT", {
                    "default": 3,
                    "min": 1,
                    "max": 5,
                    "step": 1,
                    "display": "number"
                }),
                "generation_mode": (["fixed", "randomize"], {"default": "randomize"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "DP/text"

    def load_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f 
                       if line.strip() 
                       and not line.strip().startswith('#')]
        except Exception as e:
            print(f"Error loading file {path}: {e}")
            return []

    def get_random_styles(self, num_styles, rng):
        available_styles = self.style.copy()
        if num_styles > len(available_styles):
            num_styles = len(available_styles)
        return rng.sample(available_styles, num_styles)

    def get_fixed_selection(self, items, index):
        return items[index % len(items)]

    def clean_prompt(self, prompt):
        # Remove multiple spaces
        cleaned = ' '.join(prompt.split())
        # Remove spaces before punctuation
        cleaned = re.sub(r'\s+([,.!?])', r'\1', cleaned)
        # Ensure single space after punctuation
        cleaned = re.sub(r'([,.!?])\s*', r'\1 ', cleaned)
        # Remove trailing/leading whitespace
        cleaned = cleaned.strip()
        return cleaned

    def generate(self, style_complexity, generation_mode):
        if generation_mode == "randomize":
            seed = random.randint(0, 0xffffffffffffffff)
            self.last_seed = seed
        else:
            seed = self.last_seed

        rng = random.Random(seed)
        
        style_counts = {1: 2, 2: 3, 3: 4, 4: 6, 5: 8}
        num_styles = style_counts[style_complexity]

        if generation_mode == "fixed":
            # Use fixed selections
            subject = self.get_fixed_selection(self.subject, self.fixed_selections['subject'])
            setting = self.get_fixed_selection(self.setting, self.fixed_selections['setting'])
            color_palette = self.get_fixed_selection(self.color_palette, self.fixed_selections['color_palette'])
            lighting = self.get_fixed_selection(self.lighting, self.fixed_selections['lighting'])
            additional_elements = self.get_fixed_selection(self.additional_elements, self.fixed_selections['additional_elements'])
            
            if not self.fixed_selections['styles']:
                self.fixed_selections['styles'] = self.get_random_styles(num_styles, rng)
            selected_styles = self.fixed_selections['styles']
            final_touch = self.get_fixed_selection(self.final_touch, self.fixed_selections['final_touch'])
            camera_angle = self.get_fixed_selection(self.camera_angles, self.fixed_selections['camera_angle'])
        else:
            # Generate new random selections
            subject = rng.choice(self.subject)
            setting = rng.choice(self.setting)
            color_palette = rng.choice(self.color_palette)
            lighting = rng.choice(self.lighting)
            additional_elements = rng.choice(self.additional_elements)
            selected_styles = self.get_random_styles(num_styles, rng)
            
            # Store selections for fixed mode
            self.fixed_selections['subject'] = self.subject.index(subject)
            self.fixed_selections['setting'] = self.setting.index(setting)
            self.fixed_selections['color_palette'] = self.color_palette.index(color_palette)
            self.fixed_selections['lighting'] = self.lighting.index(lighting)
            self.fixed_selections['additional_elements'] = self.additional_elements.index(additional_elements)
            self.fixed_selections['styles'] = selected_styles
            final_touch = rng.choice(self.final_touch)
            camera_angle = rng.choice(self.camera_angles)
            self.fixed_selections['final_touch'] = self.final_touch.index(final_touch)
            self.fixed_selections['camera_angle'] = self.camera_angles.index(camera_angle)

        # Select primary style for medium
        primary_style = selected_styles[0] if selected_styles else "psychedelic art"

        # Modify subject to include gender
        subject = subject.replace("a ", f"a {self.gender[self.fixed_selections['gender']]} ")

        # Construct prompt with camera angle after subject
        prompt = (
            f"{primary_style} psychedelic futuristic hyper realistic illustration of {subject}, "
            f"{camera_angle}, "
            f"{setting}, underground punk hipster cybrorg atmosphere, "
            f"{lighting}, "
            f"{color_palette}, "
            f"{additional_elements}, "
            f"in the style of {', '.join(selected_styles)}, high quality, high detail, sharp focus, "
            f"{final_touch}"
        )

        # Clean and format the prompt
        cleaned_prompt = self.clean_prompt(prompt)
        
        return (cleaned_prompt,)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN") 