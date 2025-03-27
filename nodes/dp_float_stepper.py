import random


class DP_Float_Stepper:
    def __init__(self):
        self.current_value = 0.0
        self.last_start_point = 0.0  # Track the last start point
        self.last_end_point = 0.0  # Track the last end point
        self.last_step = 0.0  # Track the last step value
        self.id = str(random.randint(0, 2**64))

        # Set DP Ocean theme colors
        self.color = "#121317"
        self.bgcolor = "#006994"
        self.properties = {"_dpColors": {"title": self.color, "body": self.bgcolor}}

    def update_widget(self, widget, value):
        # Preserve colors during widget updates
        if widget in ["title_color", "background_color"]:
            return self.color_data.get(widget, value)
        return value

    def getColors(self):
        return {"title": self.color, "body": self.bgcolor}

    def setColors(self, colors):
        self.color = colors.get("title", self.color)
        self.bgcolor = colors.get("body", self.bgcolor)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "start_point": (
                    "FLOAT",
                    {
                        "default": 0.0,
                        "min": -10.0,
                        "max": 10.0,
                        "step": 0.05,
                    },
                ),
                "end_point": (
                    "FLOAT",
                    {
                        "default": 1.0,
                        "min": -10.0,
                        "max": 10.0,
                        "step": 0.05,
                    },
                ),
                "step": (
                    "FLOAT",
                    {
                        "default": 0.05,
                        "min": 0.01,
                        "max": 1.0,
                        "step": 0.01,
                    },
                ),
            },
            "hidden": {"unique_id": "UNIQUE_ID"},
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("value",)
    FUNCTION = "step_value"
    CATEGORY = "DP/utils"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def step_value(self, start_point, end_point, step, unique_id=None):
        try:
            # Check if any inputs changed
            inputs_changed = (
                abs(start_point - self.last_start_point) > 0.0001
                or abs(end_point - self.last_end_point) > 0.0001
                or abs(step - self.last_step) > 0.0001
            )

            if inputs_changed:
                self.current_value = start_point
                self.last_start_point = start_point
                self.last_end_point = end_point
                self.last_step = step
                print(f"Inputs changed, resetting sequence to start: {start_point}")

            # Initialize if needed
            if self.current_value == 0.0 and self.last_start_point == 0.0:
                self.current_value = start_point
                self.last_start_point = start_point
                self.last_end_point = end_point
                self.last_step = step

            # Calculate next value
            next_value = round(self.current_value + step, 3)
            if next_value > end_point:
                next_value = start_point

            # Update current value
            self.current_value = next_value

            # Send update to UI
            try:
                from server import PromptServer

                PromptServer.instance.send_sync(
                    "update_node",
                    {"node_id": unique_id, "start_point": self.current_value},
                )
            except Exception as e:
                print(f"Error updating UI: {str(e)}")

            return (self.current_value,)

        except Exception as e:
            print(f"Error in step_value: {str(e)}")
            return (start_point,)


# Node registration
NODE_CLASS_MAPPINGS = {"DP_Float_Stepper": DP_Float_Stepper}

NODE_DISPLAY_NAME_MAPPINGS = {"DP_Float_Stepper": "Float Stepper"}
