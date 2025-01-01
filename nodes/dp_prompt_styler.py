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
                "DepthStyle": (s().CATEGORIES["DepthStyle"],),
                "cameraAngles": (s().CATEGORIES["cameraAngles"],),
                "colorTheme": (s().CATEGORIES["colorTheme"],),
                "FaceMood": (s().CATEGORIES["FaceMood"],),
                "timeOfDay": (s().CATEGORIES["timeOfDay"],),
                "atmosphere": (s().CATEGORIES["atmosphere"],),
                "lighting": (s().CATEGORIES["lighting"],),
                "filter_effect": (s().CATEGORIES["filter"],),
                "CameraType": (s().CATEGORIES["CameraType"],),
            },
            "optional": {
                "pre_text": ("STRING", {"default": "", "multiline": False, "defaultInput": True}),
                "pre_text_B": ("STRING", {"default": "", "multiline": False, "defaultInput": True}),
                "Main_Prompt": ("STRING", {"default": "", "multiline": False, "defaultInput": True}),
                "extra_text": ("STRING", {"default": "", "multiline": False, "defaultInput": True}),
                "extra_text_B": ("STRING", {"default": "", "multiline": False, "defaultInput": True})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Modified Prompt",)
    FUNCTION = "process_prompt"
    CATEGORY = "DP/text"

    def process_prompt(self, mode, DepthStyle, cameraAngles, colorTheme, FaceMood, 
                      timeOfDay, atmosphere, lighting, filter_effect, CameraType, 
                      pre_text="", pre_text_B="", Main_Prompt="", extra_text="", extra_text_B=""):
        # Initialize result components
        components = []
        if pre_text.strip():
            components.append(pre_text.strip())
        if pre_text_B.strip():
            components.append(pre_text_B.strip())

        if mode == "ByPass_All":
            if Main_Prompt.strip():
                components.append(Main_Prompt.strip())
        else:
            # Add Main_Prompt first if it exists
            if Main_Prompt.strip():
                components.append(Main_Prompt.strip())
            
            # Handle styles based on mode
            if mode == "Randomize_All":
                # Use random selections for each category
                style_components = [
                    random.choice(self.CATEGORIES[cat]) for cat in [
                        "DepthStyle", "cameraAngles", "colorTheme", "FaceMood",
                        "timeOfDay", "atmosphere", "lighting", "filter", "CameraType"
                    ]
                ]
            else:  # Styler_ON mode
                # Use user-selected values
                style_components = [
                    comp for comp in [
                        DepthStyle, cameraAngles, colorTheme, FaceMood,
                        timeOfDay, atmosphere, lighting, filter_effect, CameraType
                    ] if comp and comp != "none"
                ]
            
            # Add non-"none" style components
            if style_components:
                components.extend([comp for comp in style_components if comp != "none"])

        # Add extra text at the end for all modes
        if extra_text.strip():
            components.append(extra_text.strip())
        if extra_text_B.strip():
            components.append(extra_text_B.strip())
            
        return (", ".join(filter(None, components)),)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        if kwargs.get('mode') == "Randomize_All":
            return float("NaN")  # Forces update on every execution
        return False

