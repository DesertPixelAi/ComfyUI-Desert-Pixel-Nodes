class DP_Transition_Frames_Selector:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "value": ("INT", {
                    "default": 8,
                    "min": 0,
                    "max": 36,
                    "step": 4
                }),
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
                "value": ("INT", {
                    "default": 24,
                    "min": 0,
                    "max": 1920,
                    "step": 8
                }),
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
                "value": ("INT", {
                    "default": 500,
                    "min": 0,
                    "max": 1000,
                    "step": 1
                }),
            },
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "get_value"
    CATEGORY = "DP/Utils"

    def get_value(self, value):
        return (value,)

class DP_Int_0_1000_4_Step:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "value": ("INT", {
                    "default": 500,
                    "min": 0,
                    "max": 1000,
                    "step": 4
                }),
            },
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "get_value"
    CATEGORY = "DP/Utils"

    def get_value(self, value):
        return (value,)

class DP_Int_0_1000_8_Step:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "value": ("INT", {
                    "default": 500,
                    "min": 0,
                    "max": 1000,
                    "step": 8
                }),
            },
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "get_value"
    CATEGORY = "DP/Utils"

    def get_value(self, value):
        return (value,)
