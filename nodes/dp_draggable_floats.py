# ComfyUI custom nodes by DP/utils
# Simple float input/output node

import os


def read_float_settings(filename, num_inputs=1):
    default_settings = {
        "min": 0.00,
        "max": 1.00,
        "default": 1.00,
        "step": 0.01,
        "slider": False,
    }

    try:
        # Get the path to the package root directory
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Construct path to the data file
        file_path = os.path.join(current_dir, "data", "draggable_floats", filename)

        with open(file_path, "r") as f:
            content = f.read().strip().split("\n\n")
            settings_list = []

            for i in range(num_inputs):
                if i < len(content):
                    settings = default_settings.copy()
                    lines = content[i].strip().split("\n")
                    for line in lines:
                        key, value = line.split("=")
                        key = key.strip()
                        value = value.strip()
                        if key == "slider":
                            settings[key] = value.lower() == "true"
                        else:
                            settings[key] = float(value)
                    settings_list.append(settings)
                else:
                    settings_list.append(default_settings.copy())

            return settings_list
    except Exception as e:
        print(f"Error reading float settings from {filename}: {e}")
        return [default_settings.copy() for _ in range(num_inputs)]


class DP_Draggable_Floats_1:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        settings = read_float_settings("float_min_max_1_input.txt")[0]
        return {
            "required": {
                "float_value": (
                    "FLOAT",
                    {
                        "default": settings["default"],
                        "min": settings["min"],
                        "max": settings["max"],
                        "step": settings["step"],
                        "display": "slider" if settings["slider"] else "number",
                    },
                ),
            }
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("float_value",)
    FUNCTION = "process"
    CATEGORY = "DP/utils"

    def process(self, float_value):
        return (float_value,)


class DP_Draggable_Floats_2:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        settings = read_float_settings("float_min_max_2_input.txt", 2)
        return {
            "required": {
                "float_value1": (
                    "FLOAT",
                    {
                        "default": settings[0]["default"],
                        "min": settings[0]["min"],
                        "max": settings[0]["max"],
                        "step": settings[0]["step"],
                        "display": "slider" if settings[0]["slider"] else "number",
                    },
                ),
                "float_value2": (
                    "FLOAT",
                    {
                        "default": settings[1]["default"],
                        "min": settings[1]["min"],
                        "max": settings[1]["max"],
                        "step": settings[1]["step"],
                        "display": "slider" if settings[1]["slider"] else "number",
                    },
                ),
            }
        }

    RETURN_TYPES = ("FLOAT", "FLOAT")
    RETURN_NAMES = ("float_value1", "float_value2")
    FUNCTION = "process"
    CATEGORY = "DP/utils"

    def process(self, float_value1, float_value2):
        return (float_value1, float_value2)


class DP_Draggable_Floats_3:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        settings = read_float_settings("float_min_max_3_input.txt", 3)
        return {
            "required": {
                "float_value1": (
                    "FLOAT",
                    {
                        "default": settings[0]["default"],
                        "min": settings[0]["min"],
                        "max": settings[0]["max"],
                        "step": settings[0]["step"],
                        "display": "slider" if settings[0]["slider"] else "number",
                    },
                ),
                "float_value2": (
                    "FLOAT",
                    {
                        "default": settings[1]["default"],
                        "min": settings[1]["min"],
                        "max": settings[1]["max"],
                        "step": settings[1]["step"],
                        "display": "slider" if settings[1]["slider"] else "number",
                    },
                ),
                "float_value3": (
                    "FLOAT",
                    {
                        "default": settings[2]["default"],
                        "min": settings[2]["min"],
                        "max": settings[2]["max"],
                        "step": settings[2]["step"],
                        "display": "slider" if settings[2]["slider"] else "number",
                    },
                ),
            }
        }

    RETURN_TYPES = ("FLOAT", "FLOAT", "FLOAT")
    RETURN_NAMES = ("float_value1", "float_value2", "float_value3")
    FUNCTION = "process"
    CATEGORY = "DP/utils"

    def process(self, float_value1, float_value2, float_value3):
        return (float_value1, float_value2, float_value3)
