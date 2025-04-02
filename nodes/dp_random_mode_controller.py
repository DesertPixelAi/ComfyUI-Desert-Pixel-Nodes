class DP_Random_Mode_Switch:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "random_mode": (
                    [
                        "Crazy Random Prompt",
                        "Random Psychedelic Punk",
                        "Random Superhero",
                        "Random Vehicle",
                        "Random Letter Style",
                        "All Mixed",
                    ],
                ),
                "random_token_limit": ("INT", {"default": 72, "min": 0, "max": 512}),
            },
            "optional": {
                "Crazy_Random_Prompt": (
                    "STRING",
                    {"multiline": True, "forceInput": True},
                ),
                "Random_Psychedelic_Punk": (
                    "STRING",
                    {"multiline": True, "forceInput": True},
                ),
                "Random_Superhero": ("STRING", {"multiline": True, "forceInput": True}),
                "Random_Vehicle": ("STRING", {"multiline": True, "forceInput": True}),
                "Random_Letter_Style": (
                    "STRING",
                    {"multiline": True, "forceInput": True},
                ),
                "All_Mixed": ("STRING", {"multiline": True, "forceInput": True}),
            },
        }

    RETURN_TYPES = (
        "STRING",
        "INT",
    )
    RETURN_NAMES = (
        "string",
        "random_token_limit",
    )
    FUNCTION = "process"
    CATEGORY = "DP/text"

    def process(
        self,
        random_mode,
        random_token_limit,
        Crazy_Random_Prompt=None,
        Random_Psychedelic_Punk=None,
        Random_Superhero=None,
        Random_Vehicle=None,
        Random_Letter_Style=None,
        All_Mixed=None,
    ):
        mode_map = {
            "Crazy Random Prompt": Crazy_Random_Prompt,
            "Random Psychedelic Punk": Random_Psychedelic_Punk,
            "Random Superhero": Random_Superhero,
            "Random Vehicle": Random_Vehicle,
            "Random Letter Style": Random_Letter_Style,
            "All Mixed": All_Mixed,
        }
        selected = mode_map[random_mode]
        return (
            selected if selected is not None else "",
            random_token_limit,
        )


class DP_Random_Mode_Controller:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "random_mode": (
                    [
                        "Crazy Random Prompt",
                        "Random Psychedelic Punk",
                        "Random Superhero",
                        "Random Vehicle",
                        "Random Letter Style",
                        "All Mixed",
                    ],
                    {"default": "Crazy Random Prompt"},
                ),
                "random_token_limit": ("INT", {"default": 72, "min": 0, "max": 512}),
            }
        }

    RETURN_TYPES = (
        [
            "Crazy Random Prompt",
            "Random Psychedelic Punk",
            "Random Superhero",
            "Random Vehicle",
            "Random Letter Style",
            "All Mixed",
        ],
        "INT",
    )
    RETURN_NAMES = (
        "random_mode",
        "random_token_limit",
    )
    FUNCTION = "process"
    CATEGORY = "DP/utils"

    def process(self, random_mode, random_token_limit):
        return (
            random_mode,
            random_token_limit,
        )
