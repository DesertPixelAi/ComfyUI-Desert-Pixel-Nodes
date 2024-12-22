import os
import random

def _load_style_file(filename):
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "styles", filename)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            styles = [line.strip() for line in f.readlines() 
                     if line.strip() and not line.startswith('#')]
            return ["none"] + styles
    except FileNotFoundError:
        print(f"Warning: Style file {filename} not found at {file_path}. Using default empty list.")
        return ["none"]

STYLE_CATEGORIES = {
    "DepthStyle": _load_style_file("depth_styles.txt"),
    "cameraAngles": _load_style_file("camera_angles.txt"),
    "colorTheme": _load_style_file("color_themes.txt"),
    "FaceMood": _load_style_file("face_moods.txt"),
    "timeOfDay": _load_style_file("time_of_day.txt"),
    "atmosphere": _load_style_file("atmosphere.txt"),
    "lighting": _load_style_file("lighting.txt"),
    "filter": _load_style_file("filters.txt"),
    "CameraType": _load_style_file("camera_types.txt")
}

class DP_Prompt_Styler:
    def __init__(self):
        self.CATEGORIES = STYLE_CATEGORIES

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mode": (["Styler_ON", "ByPass_All", "Randomize_All"],),
                "Main_Prompt": ("STRING", {"default": "", "multiline": False}),
                "DepthStyle": (s().CATEGORIES["DepthStyle"],),
                "cameraAngles": (s().CATEGORIES["cameraAngles"],),
                "colorTheme": (s().CATEGORIES["colorTheme"],),
                "FaceMood": (s().CATEGORIES["FaceMood"],),
                "timeOfDay": (s().CATEGORIES["timeOfDay"],),
                "atmosphere": (s().CATEGORIES["atmosphere"],),
                "lighting": (s().CATEGORIES["lighting"],),
                "filter_effect": (s().CATEGORIES["filter"],),
                "CameraType": (s().CATEGORIES["CameraType"],),
                "extra_text": ("STRING", {"default": "", "multiline": False})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Modified Prompt",)
    FUNCTION = "process_prompt"
    CATEGORY = "DP/text"

    def process_prompt(self, mode, Main_Prompt, DepthStyle, cameraAngles, colorTheme, FaceMood, 
                      timeOfDay, atmosphere, lighting, filter_effect, CameraType, extra_text):
        if mode == "ByPass_All":
            return (Main_Prompt.strip(),)
        
        elif mode == "Randomize_All":
            # Get random selections for each category
            random_selections = {
                "DepthStyle": random.choice(self.CATEGORIES["DepthStyle"]),
                "cameraAngles": random.choice(self.CATEGORIES["cameraAngles"]),
                "colorTheme": random.choice(self.CATEGORIES["colorTheme"]),
                "FaceMood": random.choice(self.CATEGORIES["FaceMood"]),
                "timeOfDay": random.choice(self.CATEGORIES["timeOfDay"]),
                "atmosphere": random.choice(self.CATEGORIES["atmosphere"]),
                "lighting": random.choice(self.CATEGORIES["lighting"]),
                "filter": random.choice(self.CATEGORIES["filter"]),
                "CameraType": random.choice(self.CATEGORIES["CameraType"])
            }
            
            components = [Main_Prompt.strip()]
            style_components = [
                comp for comp in [
                    random_selections["DepthStyle"],
                    random_selections["cameraAngles"],
                    random_selections["colorTheme"],
                    random_selections["FaceMood"],
                    random_selections["timeOfDay"],
                    random_selections["atmosphere"],
                    random_selections["lighting"],
                    random_selections["filter"],
                    random_selections["CameraType"],
                    extra_text.strip()
                ] if comp and comp != "none"
            ]
            
        else:  # mode == "Styler_ON"
            components = [Main_Prompt.strip()]
            style_components = [
                comp for comp in [
                    DepthStyle, cameraAngles, colorTheme, FaceMood, timeOfDay,
                    atmosphere, lighting, filter_effect, CameraType, extra_text.strip()
                ] if comp and comp != "none"
            ]
        
        if style_components:
            components.extend(style_components)
            
        # More efficient string joining
        result = ", ".join(comp for comp in components if comp)
        
        # Single regex replacement instead of multiple .replace() calls
        import re
        result = re.sub(r'\s*,\s*', ', ', result)
        
        return (result,)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        if kwargs.get('mode') == "Randomize_All":
            return float("NaN")  # Forces update on every execution
        return False

