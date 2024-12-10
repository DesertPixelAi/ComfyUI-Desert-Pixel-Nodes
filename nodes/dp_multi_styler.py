import os

class DpPromptStyler:
    @classmethod
    def load_styles_from_file(cls, filename):
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "styles", filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                # Read lines and filter out empty lines and comments
                styles = [line.strip() for line in f.readlines() 
                         if line.strip() and not line.startswith('#')]
                # Always add "none" as first option
                return ["none"] + styles
        except FileNotFoundError:
            print(f"Warning: Style file {filename} not found at {file_path}. Using default empty list.")
            return ["none"]

    def __init__(self):
        # Load all style categories from files
        self.CATEGORIES = {
            "DepthStyle": self.load_styles_from_file("depth_styles.txt"),
            "cameraAngles": self.load_styles_from_file("camera_angles.txt"),
            "colorTheme": self.load_styles_from_file("color_themes.txt"),
            "FaceMood": self.load_styles_from_file("face_moods.txt"),
            "timeOfDay": self.load_styles_from_file("time_of_day.txt"),
            "atmosphere": self.load_styles_from_file("atmosphere.txt"),
            "lighting": self.load_styles_from_file("lighting.txt"),
            "filter": self.load_styles_from_file("filters.txt"),
            "CameraType": self.load_styles_from_file("camera_types.txt")
        }
        
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Main_Prompt": ("STRING", {"default": "", "multiline": False}),
                "DepthStyle": (s().CATEGORIES["DepthStyle"],),
                "cameraAngles": (s().CATEGORIES["cameraAngles"],),
                "colorTheme": (s().CATEGORIES["colorTheme"],),  # Changed from action
                "FaceMood": (s().CATEGORIES["FaceMood"],),
                "timeOfDay": (s().CATEGORIES["timeOfDay"],),
                "atmosphere": (s().CATEGORIES["atmosphere"],),
                "lighting": (s().CATEGORIES["lighting"],),
                "filter": (s().CATEGORIES["filter"],),
                "CameraType": (s().CATEGORIES["CameraType"],),
                "extra_text": ("STRING", {"default": "", "multiline": False})  # Changed from EndExtras
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Modified Prompt",)
    FUNCTION = "process_prompt"
    CATEGORY = "DP/text"

    def process_prompt(self, Main_Prompt, DepthStyle, cameraAngles, colorTheme, FaceMood, 
                      timeOfDay, atmosphere, lighting, filter, CameraType, extra_text):  # Updated parameters
        result = ""
        parts = []
        
        if Main_Prompt.strip():
            result = Main_Prompt.strip() + ", " + result

        components = [
            DepthStyle, cameraAngles, colorTheme, FaceMood, timeOfDay,
            atmosphere, lighting, filter, CameraType, extra_text.strip()  # Updated list
        ]
        
        parts = [comp for comp in components if comp and comp != "none"]
            
        if parts:
            result = result + " " + ", ".join(parts)
        
        # Clean up formatting
        while "  " in result:
            result = result.replace("  ", " ")
        while ",," in result:
            result = result.replace(",,", ",")
        
        result = result.replace(" ,", ",")
        result = result.replace(", ", ",")
        result = result.replace(",", ", ")
        
        return (result,)

NODE_CLASS_MAPPINGS = {
    "DpPromptStyler": DpPromptStyler
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DpPromptStyler": "Desert Pixel Styler"
}