class DP_IF_INT_CONDITION:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "if_value": ("INT", {"default": 0, "min": -18446744073709551615, "max": 18446744073709551615}),
                "if_logic": (["equal", "smaller", "bigger"],),
                "compare_if_with": ("INT", {"default": 0, "min": -18446744073709551615, "max": 18446744073709551615}),
                "or_value": ("INT", {"default": 0, "min": -18446744073709551615, "max": 18446744073709551615}),
                "compare_or_with": (["off", "equal", "smaller", "bigger"],),
                "compare_or_value": ("INT", {"default": 0, "min": -18446744073709551615, "max": 18446744073709551615}),
                "result_if_true": ("INT", {"default": 1, "min": -18446744073709551615, "max": 18446744073709551615}),
                "result_if_false": ("INT", {"default": 0, "min": -18446744073709551615, "max": 18446744073709551615}),
            }
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "execute"
    CATEGORY = "Desert Pixel/Logic"

    def execute(self, if_value, if_logic, compare_if_with, or_value, compare_or_with, compare_or_value, result_if_true, result_if_false):
        result = result_if_false
        condition_met = False
        
        # Check first condition
        if if_logic == "equal":
            if if_value == compare_if_with:
                condition_met = True
        elif if_logic == "smaller":
            if if_value < compare_if_with:
                condition_met = True
        elif if_logic == "bigger":
            if if_value > compare_if_with:
                condition_met = True
        
        # Check second condition (OR) if not off and first condition wasn't met
        if not condition_met and compare_or_with != "off":
            if compare_or_with == "equal" and or_value == compare_or_value:
                condition_met = True
            elif compare_or_with == "smaller" and or_value < compare_or_value:
                condition_met = True
            elif compare_or_with == "bigger" and or_value > compare_or_value:
                condition_met = True
        
        # Set result if either condition was met
        if condition_met:
            result = result_if_true
                
        return (result,)

NODE_CLASS_MAPPINGS = {
    "DP IF Int Condition": DP_IF_INT_CONDITION
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DP IF Int Condition": "IF Int Condition"
}
