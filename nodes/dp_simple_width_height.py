import os


class DP_Aspect_Ratio_Picker:
    # Cache ratios at class level
    _cached_ratios = None

    @classmethod
    def load_ratios_from_file(cls):
        # Return cached ratios if already loaded
        if cls._cached_ratios is not None:
            return cls._cached_ratios

        base_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "data", "aspect_ratio"
        )
        files = ["my_aspect_ratios.txt", "custom_aspect_ratios.txt"]
        ratios = []

        for file_name in files:
            file_path = os.path.join(base_path, file_name)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    ratios.extend(
                        {
                            "name": parts[0].strip(),
                            "width": parts[1].strip(),
                            "height": parts[2].strip(),
                        }
                        for raw_line in f.readlines()
                        if (line := raw_line.strip())
                        and not line.startswith("#")
                        and len(parts := line.split(",")) >= 3
                    )
            except FileNotFoundError:
                print(f"Warning: File {file_path} not found. Skipping.")

        cls._cached_ratios = ratios or [
            {"name": "Default (1:1)", "width": "1024", "height": "1024"}
        ]
        return cls._cached_ratios

    @classmethod
    def INPUT_TYPES(cls):
        ratios = cls.load_ratios_from_file()
        return {
            "required": {
                "aspect_ratio": ([ratio["name"] for ratio in ratios],),
            },
            "optional": {
                "custom_settings": ("CUSTOM_SETTINGS",),
            },
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "pick_aspect_ratio"
    CATEGORY = "DP/utils"

    def get_dimensions_for_ratio(self, aspect_ratio_name):
        ratios = self._cached_ratios  # Use cached ratios
        for ratio in ratios:
            if ratio["name"] == aspect_ratio_name:
                try:
                    return int(ratio["width"]), int(ratio["height"])
                except ValueError:
                    break
        return 1024, 1024  # Default dimensions if lookup fails

    def pick_aspect_ratio(self, aspect_ratio, custom_settings=None):
        if custom_settings is not None:
            try:
                width, height = custom_settings
                return int(width), int(height)
            except:
                pass
        return self.get_dimensions_for_ratio(aspect_ratio)
