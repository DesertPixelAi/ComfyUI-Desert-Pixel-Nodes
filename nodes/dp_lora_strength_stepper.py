import random

class DP_Lora_Strength_Stepper:
    def __init__(self):
        self.current_value = 0.0
        self.last_start_point = 0.0  # Track the last start point
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
                "start_point": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 2.5,
                    "step": 0.05,
                }),
                "step": ("FLOAT", {
                    "default": 0.05,
                    "min": 0.01,
                    "max": 0.5,
                    "step": 0.01,
                }),
                "lora_name": ("STRING", {
                    "multiline": False,
                    "default": "lora"
                }),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID"
            },
        }

    RETURN_TYPES = ("FLOAT", "STRING",)
    RETURN_NAMES = ("value", "strength_as_text",)
    FUNCTION = "step_value"
    CATEGORY = "DP/utils"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def step_value(self, start_point, step, lora_name, unique_id=None):
        try:
            # Check if start_point was changed by user
            if abs(start_point - self.last_start_point) > 0.0001:  # Using small epsilon for float comparison
                self.current_value = start_point
                self.last_start_point = start_point
                print(f"Start point changed to: {start_point}, resetting sequence")
            
            # Initialize if needed
            if self.current_value == 0.0 and self.last_start_point == 0.0:
                self.current_value = start_point
                self.last_start_point = start_point

            # Calculate next value
            next_value = round(self.current_value + step, 3)
            if next_value > 1.5:
                next_value = start_point

            # Update current value
            self.current_value = next_value
            
            # Create formatted string output
            strength_text = f"#{lora_name}_{self.current_value:.2f}"
            
            # Send update to UI
            try:
                from server import PromptServer
                PromptServer.instance.send_sync("update_node", {
                    "node_id": unique_id,
                    "start_point": self.current_value
                })
            except Exception as e:
                print(f"Error updating UI: {str(e)}")

            return (self.current_value, strength_text)
            
        except Exception as e:
            print(f"Error in step_value: {str(e)}")
            strength_text = f"{lora_name}_{start_point:.2f}"
            return (start_point, strength_text)

# Node registration
NODE_CLASS_MAPPINGS = {
    "DP_Lora_Strength_Stepper": DP_Lora_Strength_Stepper
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DP_Lora_Strength_Stepper": "Lora Strength Stepper"
} 