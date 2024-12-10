import os

class DPAspectRatioPicker:
    @classmethod
    def load_ratios_from_file(cls):
        base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "aspect_ratio")
        file_path = os.path.join(base_path, "my_aspect_ratios.txt")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                ratios = []
                for line in f.readlines():
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split(',')
                        if len(parts) >= 3:
                            name = parts[0].strip()
                            width = parts[1].strip()
                            height = parts[2].strip()
                            ratios.append({"name": name, "width": width, "height": height})
                return ratios
        except FileNotFoundError:
            print(f"Warning: File {file_path} not found. Using default ratios.")
            return [{"name": "Default (1:1)", "width": "1024", "height": "1024"}]

    @classmethod
    def INPUT_TYPES(cls):
        ratios = cls.load_ratios_from_file()
        dropdown_options = [ratio["name"] for ratio in ratios]
        return {
            "required": {
                "aspect_ratio": (dropdown_options,),
            }
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "pick_aspect_ratio"
    CATEGORY = "DP/utils"

    def get_dimensions_for_ratio(self, aspect_ratio_name):
        ratios = self.load_ratios_from_file()
        for ratio in ratios:
            if ratio["name"] == aspect_ratio_name:
                try:
                    return int(ratio["width"]), int(ratio["height"])
                except ValueError:
                    break
        return 1024, 1024  # Default dimensions if lookup fails

    def pick_aspect_ratio(self, aspect_ratio):
        width, height = self.get_dimensions_for_ratio(aspect_ratio)
        return (width, height)

NODE_CLASS_MAPPINGS = {
    "DPAspectRatioPicker": DPAspectRatioPicker
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DPAspectRatioPicker": "DP Aspect Ratio Picker"
}
