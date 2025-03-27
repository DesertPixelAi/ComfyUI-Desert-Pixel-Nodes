class DP_Condition_Switch:
    """
    A node that switches between different pairs of conditions (positive/negative).
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "selected_pair": (
                    [
                        "Conditions 01",
                        "Conditions 02",
                        "Conditions 03",
                        "Conditions 04",
                        "Conditions 05",
                    ],
                ),
            },
            "optional": {
                "condition_positive_01": ("CONDITIONING",),
                "condition_negative_01": ("CONDITIONING",),
                "condition_positive_02": ("CONDITIONING",),
                "condition_negative_02": ("CONDITIONING",),
                "condition_positive_03": ("CONDITIONING",),
                "condition_negative_03": ("CONDITIONING",),
                "condition_positive_04": ("CONDITIONING",),
                "condition_negative_04": ("CONDITIONING",),
                "condition_positive_05": ("CONDITIONING",),
                "condition_negative_05": ("CONDITIONING",),
            },
        }

    RETURN_TYPES = ("CONDITIONING", "CONDITIONING")
    RETURN_NAMES = ("condition_positive", "condition_negative")
    FUNCTION = "switch_conditions"
    CATEGORY = "DP/conditioning"

    def switch_conditions(self, selected_pair, **kwargs):
        # Get the pair number from selection
        pair_num = int(selected_pair.split()[-1])

        # Get the corresponding conditions
        positive_key = f"condition_positive_{pair_num:02d}"
        negative_key = f"condition_negative_{pair_num:02d}"

        selected_positive = kwargs.get(positive_key)
        selected_negative = kwargs.get(negative_key)

        # Check if the selected conditions are connected
        if selected_positive is None or selected_negative is None:
            print(f"Warning: Selected {selected_pair} has unconnected conditions!")
            # Return empty conditions as fallback
            return ([], [])

        return (selected_positive, selected_negative)
