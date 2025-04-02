import random

from server import PromptServer


class DP_Text_Preview:
    def __init__(self):
        self.id = str(random.randint(0, 2**64))
        self.color = "#121317"  # Default DP Ocean title color
        self.bgcolor = "#006994"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "any_input": ("*", {"forceInput": True}),
                "display_text": (
                    "STRING",
                    {
                        "multiline": True,
                        "height": 120,
                    },
                ),
            },
            "hidden": {
                "text": ("STRING", {"forceInput": True}),
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "show_text"
    CATEGORY = "DP/utils"
    INPUT_IS_LIST = True
    OUTPUT_IS_OPTIONAL = True
    OUTPUT_NODE = True

    @classmethod
    def VALIDATE_INPUTS(cls, input_types):
        return True

    def format_value(self, value):
        if value is None:
            return ""
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, bool):
            return str(value)
        elif isinstance(value, str):
            if "/" in value and "." in value:
                return value.split("/")[-1].split(".")[0]
            return value
        elif isinstance(value, list):
            return str(value[0]) if value else ""
        else:
            try:
                if hasattr(value, "model_name"):
                    return str(value.model_name)
                elif hasattr(value, "name"):
                    return str(value.name)
                elif hasattr(value, "model_path"):
                    return str(value.model_path).split("/")[-1].split(".")[0]
            except:
                pass
            return str(value)

    def show_text(
        self,
        unique_id=None,
        extra_pnginfo=None,
        text=None,
        any_input=None,
        display_text="",
    ):
        # Handle text input if it's a list
        text_value = text[0] if isinstance(text, list) and text else ""
        if isinstance(text_value, list):
            text_value = " ".join(str(x) for x in text_value)

        any_value = any_input[0] if isinstance(any_input, list) else any_input
        formatted_any = self.format_value(any_value)

        if text_value and formatted_any:
            display_value = f"{text_value}\n{formatted_any}"
        elif text_value:
            display_value = text_value
        elif formatted_any:
            display_value = formatted_any
        else:
            display_value = display_text or ""

        try:
            if unique_id:
                PromptServer.instance.send_sync(
                    "update_node",
                    {
                        "node_id": unique_id[0],
                        "widget_values": {"display_text": display_value},
                    },
                )
        except Exception as e:
            print(f"Error updating widget: {str(e)}")

        return (display_value,)
