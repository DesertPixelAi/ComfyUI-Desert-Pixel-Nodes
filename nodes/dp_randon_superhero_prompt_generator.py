import random
import os
import re

class DP_Random_Superhero_Prompt_Generator:
    def __init__(self):
        # Get the directory where the files are located
        node_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(node_dir, "data", "super_hero_prompt_generator")
        
        # Add gender list
        self.gender = ["male", "female"]
        
        # Load all text files
        self.hero_names = self.load_file(os.path.join(data_dir, "hero_names.txt"))
        self.hero_base = self.load_file(os.path.join(data_dir, "hero_base.txt"))
        self.power_source = self.load_file(os.path.join(data_dir, "power_source.txt"))
        self.costume_material = self.load_file(os.path.join(data_dir, "costume_material.txt"))
        self.costume_design = self.load_file(os.path.join(data_dir, "costume_design.txt"))
        self.powers_visual = self.load_file(os.path.join(data_dir, "powers_visual.txt"))
        self.scene_setting = self.load_file(os.path.join(data_dir, "scene_setting.txt"))
        self.action_pose = self.load_file(os.path.join(data_dir, "action_pose.txt"))
        self.lighting_effects = self.load_file(os.path.join(data_dir, "lighting_effects.txt"))
        self.atmosphere = self.load_file(os.path.join(data_dir, "atmosphere.txt"))
        self.styles = self.load_file(os.path.join(data_dir, "styles.txt"))
        self.color_schemes = self.load_file(os.path.join(data_dir, "color_schemes.txt"))
        self.hero_logos = self.load_file(os.path.join(data_dir, "hero_logos.txt"))
        self.hair_styles = self.load_file(os.path.join(data_dir, "hair_styles.txt"))
        self.hair_colors = self.load_file(os.path.join(data_dir, "hair_colors.txt"))
        self.face_masks = self.load_file(os.path.join(data_dir, "face_masks.txt"))
        self.ethnicities = self.load_file(os.path.join(data_dir, "ethnicities.txt"))
        
        # Store last fixed selections
        self.fixed_selections = {
            "hero_base": 0,
            "power_source": 0,
            "costume_material": 0,
            "costume_design": 0,
            "powers_visual": 0,
            "scene_setting": 0,
            "action_pose": 0,
            "lighting_effects": 0,
            "atmosphere": 0,
            "styles": []
        }
        self.last_seed = 0

        # Add name generation lists
        self.prefixes = [
            "Ultra", "Mega", "Super", "Hyper", "Omega", "Alpha", "Neo", "Quantum", 
            "Cosmic", "Thunder", "Shadow", "Star", "Night", "Storm", "Crystal",
            "Solar", "Lunar", "Cyber", "Techno", "Bio", "Psy", "Meta", "Astro",
            "Pyro", "Cryo", "Aero", "Terra", "Electro", "Photo", "Hydro", "Gyro",
            "Mecha", "Fusion", "Prime", "Proto", "Spectral", "Phantom", "Ghost"
        ]
        self.elements = [
            "Fire", "Ice", "Wind", "Earth", "Lightning", "Light", "Dark", "Time",
            "Space", "Metal", "Plasma", "Energy", "Gravity", "Force", "Mind",
            "Spirit", "Nature", "Tech", "Void", "Quantum", "Cosmic", "Solar",
            "Flame", "Frost", "Storm", "Stone", "Thunder", "Shadow", "Chaos"
        ]
        self.animals = [
            "Wolf", "Lion", "Tiger", "Dragon", "Phoenix", "Eagle", "Hawk", "Bear",
            "Panther", "Falcon", "Cobra", "Viper", "Fox", "Owl", "Raven", "Shark",
            "Scorpion", "Mantis", "Jaguar", "Leopard", "Griffin", "Hydra", "Wyrm",
            "Basilisk", "Chimera", "Manticore", "Kraken", "Leviathan", "Behemoth"
        ]

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
                # Skip comments, empty lines, and lines starting with '/'
                return [line.strip() for line in f 
                       if line.strip() 
                       and not line.strip().startswith(('#', '/'))
                       and not line.strip().startswith('/*')]
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

    def generate_code(self, rng):
        chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        return ''.join(rng.choice(chars) for _ in range(4))

    def generate_hero_name(self, rng):
        patterns = [
            lambda: f"{rng.choice(self.prefixes)}{rng.choice(self.elements)}",
            lambda: f"{rng.choice(self.animals)}{rng.choice(self.elements)}",
            lambda: f"{rng.choice(self.prefixes)}{rng.choice(self.animals)}-{self.generate_code(rng)}",
        ]
        return rng.choice(patterns)()

    def clean_prompt(self, prompt):
        # Remove multiple spaces
        cleaned = ' '.join(prompt.split())
        
        # Remove spaces before punctuation
        cleaned = re.sub(r'\s+([,.!?])', r'\1', cleaned)
        
        # Ensure single space after punctuation
        cleaned = re.sub(r'([,.!?])\s*', r'\1 ', cleaned)
        
        # Remove any trailing/leading whitespace
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
            hero_base = self.get_fixed_selection(self.hero_base, self.fixed_selections['hero_base'])
            power_source = self.get_fixed_selection(self.power_source, self.fixed_selections['power_source'])
            costume_material = self.get_fixed_selection(self.costume_material, self.fixed_selections['costume_material'])
            costume_design = self.get_fixed_selection(self.costume_design, self.fixed_selections['costume_design'])
            powers_visual = self.get_fixed_selection(self.powers_visual, self.fixed_selections['powers_visual'])
            scene_setting = self.get_fixed_selection(self.scene_setting, self.fixed_selections['scene_setting'])
            action_pose = self.get_fixed_selection(self.action_pose, self.fixed_selections['action_pose'])
            lighting = self.get_fixed_selection(self.lighting_effects, self.fixed_selections['lighting_effects'])
            atmosphere = self.get_fixed_selection(self.atmosphere, self.fixed_selections['atmosphere'])
            
            if not self.fixed_selections['styles']:
                self.fixed_selections['styles'] = self.get_random_styles(num_styles, rng)
            selected_styles = self.fixed_selections['styles']
        else:
            # Generate new random selections
            hero_base = rng.choice(self.hero_base)
            power_source = rng.choice(self.power_source)
            costume_material = rng.choice(self.costume_material)
            costume_design = rng.choice(self.costume_design)
            powers_visual = rng.choice(self.powers_visual)
            scene_setting = rng.choice(self.scene_setting)
            action_pose = rng.choice(self.action_pose)
            lighting = rng.choice(self.lighting_effects)
            atmosphere = rng.choice(self.atmosphere)
            selected_styles = self.get_random_styles(num_styles, rng)
            
            # Store selections for fixed mode
            self.fixed_selections['hero_base'] = self.hero_base.index(hero_base)
            self.fixed_selections['power_source'] = self.power_source.index(power_source)
            self.fixed_selections['costume_material'] = self.costume_material.index(costume_material)
            self.fixed_selections['costume_design'] = self.costume_design.index(costume_design)
            self.fixed_selections['powers_visual'] = self.powers_visual.index(powers_visual)
            self.fixed_selections['scene_setting'] = self.scene_setting.index(scene_setting)
            self.fixed_selections['action_pose'] = self.action_pose.index(action_pose)
            self.fixed_selections['lighting_effects'] = self.lighting_effects.index(lighting)
            self.fixed_selections['atmosphere'] = self.atmosphere.index(atmosphere)
            self.fixed_selections['styles'] = selected_styles

        # Select one style as the medium
        prompt_style = selected_styles[0]
        
        # Get random gender
        gender = rng.choice(self.gender)
        
        # Generate hero name by selecting from the list
        hero_name = rng.choice(self.hero_names) if self.hero_names else "Unknown Hero"
        
        # Select a color scheme
        color_scheme = rng.choice(self.color_schemes) if self.color_schemes else ""
        
        # Select a logo design
        logo_design = rng.choice(self.hero_logos) if self.hero_logos else ""
        
        # Get character details
        ethnicity = rng.choice(self.ethnicities) if self.ethnicities else ""
        face_mask = rng.choice(self.face_masks) if self.face_masks else ""
        
        # Gender-specific details with mandatory masks
        if gender == "female":
            hair_style = rng.choice(self.hair_styles) if self.hair_styles else ""
            hair_color = rng.choice(self.hair_colors) if self.hair_colors else ""
            character_details = f"with {hair_style} in {hair_color}, wearing {face_mask}"
        else:
            character_details = f"wearing {face_mask}"

        # Construct prompt with new details
        prompt = (
            f"{prompt_style} of an epic generic-superhero {gender}, in cinematic powerfull concept photo, frontal view, {hero_name} - {hero_base}, {action_pose}, "
            f"{character_details}, {power_source}, wearing a {costume_material} "
            f"{costume_design} in {color_scheme} with a {logo_design}, {powers_visual}, {scene_setting}, "
            f"{lighting}, {atmosphere}, {ethnicity}, inspired by comics art and psychedelic hyper realistic digital illustration, cool and crazy and funny generic-superhero cinematic solo scene,{', '.join(selected_styles)}"
        )
        #  highly detailed, hyper-realistic comics art,
        # Clean and format the prompt
        cleaned_prompt = self.clean_prompt(prompt)
        
        return (cleaned_prompt,)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN") 