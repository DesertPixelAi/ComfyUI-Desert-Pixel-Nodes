import random
from server import PromptServer

class DP_Line_Cycler:
    def __init__(self):
        self.current_index = 0
        self.id = str(random.randint(0, 2**64))

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Text": ("STRING", {"multiline": True, "default": ""}),
                "Cycler_Mode": (["increment", "decrement", "randomize", "fixed"],),
                "index": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID"
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("TEXT",)
    FUNCTION = "cycle"
    CATEGORY = "DP/text"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def cycle(self, Text, Cycler_Mode, index, unique_id):
        try:
            # Clean and validate text lines, ignore comments and empty lines
            lines = [
                line.strip() 
                for line in Text.split('\n') 
                if line.strip() and not line.strip().startswith(('/', '//', '#'))
            ]

            # Handle empty text case
            if not lines:
                return ("",)

            num_lines = len(lines)
            next_index = self.current_index

            # Detect changes
            index_changed = index != self.current_index

            # Handle fixed mode and user input changes
            if Cycler_Mode == "fixed":
                if index_changed:
                    next_index = max(0, min(index, num_lines - 1))
                    self.current_index = next_index
            # Handle mode-specific behavior
            elif Cycler_Mode == "randomize":
                while True:
                    next_index = random.randint(0, num_lines - 1)
                    if next_index != self.current_index or num_lines == 1:
                        break
                self.current_index = next_index
            elif Cycler_Mode == "increment":
                next_index = (self.current_index + 1) % num_lines
                self.current_index = next_index
            elif Cycler_Mode == "decrement":
                next_index = (self.current_index - 1) % num_lines
                self.current_index = next_index

            # Select line based on index
            selected_line = lines[self.current_index]

            # Update UI
            try:
                PromptServer.instance.send_sync("update_node", {
                    "node_id": unique_id,
                    "index_value": self.current_index,
                    "widget_name": "index",
                    "force_widget_update": True
                })
            except Exception as e:
                print(f"Error sending WebSocket message: {str(e)}")

            return (selected_line,)
            
        except Exception as e:
            print(f"Error in DP_Line_Cycler: {str(e)}")
            return ("",) 