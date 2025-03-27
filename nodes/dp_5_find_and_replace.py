class DP_5_Find_And_Replace:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "01_find": ("STRING", {"default": "#rep1"}),
                "01_replace_with": ("STRING", {"default": ""}),
                "02_find": ("STRING", {"default": "#rep2"}),
                "02_replace_with": ("STRING", {"default": ""}),
                "03_find": ("STRING", {"default": "#rep3"}),
                "03_replace_with": ("STRING", {"default": ""}),
                "04_find": ("STRING", {"default": "#rep4"}),
                "04_replace_with": ("STRING", {"default": ""}),
                "05_find": ("STRING", {"default": "#rep5"}),
                "05_replace_with": ("STRING", {"default": ""}),
            },
            "optional": {
                "Text": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("TEXT",)
    FUNCTION = "process"
    CATEGORY = "DP/text"

    def process(self, Text: str = None, **kwargs) -> tuple[str]:
        try:
            if Text is None:
                return ("",)

            result = Text

            # Process each replacement pair
            for i in range(1, 6):
                num = str(i).zfill(2)
                find_key = f"{num}_find"
                replace_key = f"{num}_replace_with"

                if find_key in kwargs and replace_key in kwargs:
                    find_term = str(kwargs[find_key])
                    replace_term = str(kwargs[replace_key])
                    if find_term:  # Only replace if find term is not empty
                        result = result.replace(find_term, replace_term)

            return (result,)

        except Exception as e:
            print(f"Error in DP_5_Find_And_Replace: {str(e)}")
            return ("",)
