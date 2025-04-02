import os


def read_int_settings(filename):
    default_settings = {"min": 0, "max": 1000}

    try:
        # Get the path to the package root directory
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Construct path to the data file
        file_path = os.path.join(current_dir, "data", "draggable_ints", filename)

        settings_list = []
        current_settings = None

        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("#"):
                    if current_settings:
                        settings_list.append(current_settings)
                    current_settings = default_settings.copy()
                elif "=" in line:
                    key, value = line.split("=")
                    key = key.strip()
                    value = int(value.strip())
                    if current_settings:
                        current_settings[key] = value

            if current_settings:
                settings_list.append(current_settings)

        return settings_list
    except Exception as e:
        print(f"Error reading int settings from {filename}: {e}")
        return [default_settings.copy() for _ in range(3)]


class DP_Transition_Frames_Selector:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "value": ("INT", {"default": 8, "min": 0, "max": 36, "step": 4}),
            },
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "get_value"
    CATEGORY = "DP/utils"

    def get_value(self, value):
        return (value,)


class DP_Diff_Int_8step_selector:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "value": ("INT", {"default": 24, "min": 0, "max": 1920, "step": 8}),
            },
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "get_value"
    CATEGORY = "DP/Utils"

    def get_value(self, value):
        return (value,)


class DP_Int_0_1000:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "value": ("INT", {"default": 500, "min": 0, "max": 1000, "step": 1}),
            },
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "get_value"
    CATEGORY = "DP/Utils"

    def get_value(self, value):
        return (value,)


class DP_Draggable_Int_1step:
    @classmethod
    def INPUT_TYPES(s):
        settings = read_int_settings("draggable_int_settings.txt")[0]
        return {
            "required": {
                "value": (
                    "INT",
                    {
                        "default": 500,
                        "min": settings["min"],
                        "max": settings["max"],
                        "step": 1,
                    },
                ),
            },
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "get_value"
    CATEGORY = "DP/Utils"

    def get_value(self, value):
        return (value,)


class DP_Draggable_Int_4step:
    @classmethod
    def INPUT_TYPES(s):
        settings = read_int_settings("draggable_int_settings.txt")[1]
        return {
            "required": {
                "value": (
                    "INT",
                    {
                        "default": 500,
                        "min": settings["min"],
                        "max": settings["max"],
                        "step": 4,
                    },
                ),
            },
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "get_value"
    CATEGORY = "DP/Utils"

    def get_value(self, value):
        return (value,)


class DP_Draggable_Int_8step:
    @classmethod
    def INPUT_TYPES(s):
        settings = read_int_settings("draggable_int_settings.txt")[2]
        return {
            "required": {
                "value": (
                    "INT",
                    {
                        "default": 500,
                        "min": settings["min"],
                        "max": settings["max"],
                        "step": 8,
                    },
                ),
            },
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "get_value"
    CATEGORY = "DP/Utils"

    def get_value(self, value):
        return (value,)
