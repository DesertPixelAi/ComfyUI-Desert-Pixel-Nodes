class DP_Custom_Aspect_Ratio:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": ("INT", {"default": 1024, "min": 256, "max": 2048, "step": 8}),
                "height": (
                    "INT",
                    {"default": 1024, "min": 256, "max": 2048, "step": 8},
                ),
            }
        }

    RETURN_TYPES = ("CUSTOM_SETTINGS",)
    RETURN_NAMES = ("custom_settings",)
    FUNCTION = "get_dimensions"
    CATEGORY = "DP/utils"

    def get_dimensions(self, width, height):
        custom_settings = (width, height)
        return (custom_settings,)
