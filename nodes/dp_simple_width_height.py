import os

class DP_Aspect_Ratio_Picker:
    # Cache ratios at class level
    _cached_ratios = None
    
    @classmethod
    def load_ratios_from_file(cls):
        # Return cached ratios if already loaded
        if cls._cached_ratios is not None:
            return cls._cached_ratios
            
        base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "aspect_ratio")
        file_path = os.path.join(base_path, "my_aspect_ratios.txt")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                ratios = []
                # More efficient list comprehension instead of loop
                ratios = [
                    {
                        "name": parts[0].strip(),
                        "width": parts[1].strip(),
                        "height": parts[2].strip()
                    }
                    for raw_line in f.readlines()
                    if (line := raw_line.strip()) and not line.startswith('#')
                    and len(parts := line.split(',')) >= 3
                ]
                
                cls._cached_ratios = ratios or [{"name": "Default (1:1)", "width": "1024", "height": "1024"}]
                return cls._cached_ratios
                
        except FileNotFoundError:
            print(f"Warning: File {file_path} not found. Using default ratios.")
            cls._cached_ratios = [{"name": "Default (1:1)", "width": "1024", "height": "1024"}]
            return cls._cached_ratios

    @classmethod
    def INPUT_TYPES(cls):
        ratios = cls.load_ratios_from_file()
        return {
            "required": {
                "aspect_ratio": ([ratio["name"] for ratio in ratios],),
            }
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

    def pick_aspect_ratio(self, aspect_ratio):
        width, height = self.get_dimensions_for_ratio(aspect_ratio)
        return (width, height)

