class DP_Random_Mode_Switch:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "random_mode": (["Crazy Random Prompt", "Random Psychedelic Punk", "Random Superhero", "Random Letter Style", "All Mixed"],),
            },
            "optional": {
                "Crazy_Random_Prompt": ("STRING", {"multiline": True, "forceInput": True}),
                "Random_Psychedelic_Punk": ("STRING", {"multiline": True, "forceInput": True}),
                "Random_Superhero": ("STRING", {"multiline": True, "forceInput": True}),
                "Random_Letter_Style": ("STRING", {"multiline": True, "forceInput": True}),
                "All_Mixed": ("STRING", {"multiline": True, "forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    FUNCTION = "process"
    CATEGORY = "DP/text"

    def process(self, random_mode, Crazy_Random_Prompt=None, Random_Psychedelic_Punk=None, Random_Superhero=None, Random_Letter_Style=None, All_Mixed=None):
        mode_map = {
            "Crazy Random Prompt": Crazy_Random_Prompt,
            "Random Psychedelic Punk": Random_Psychedelic_Punk,
            "Random Superhero": Random_Superhero,
            "Random Letter Style": Random_Letter_Style,
            "All Mixed": All_Mixed
        }
        selected = mode_map[random_mode]
        return (selected if selected is not None else "",)

class DP_Random_Mode_Controller:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "random_mode": (["Crazy Random Prompt", "Random Psychedelic Punk", "Random Superhero", "Random Letter Style", "All Mixed"], 
                        {"default": "Crazy Random Prompt"}),
            }
        }

    RETURN_TYPES = (["Crazy Random Prompt", "Random Psychedelic Punk", "Random Superhero", "Random Letter Style", "All Mixed"],)
    RETURN_NAMES = ("random_mode",)
    FUNCTION = "process"
    CATEGORY = "DP/utils"

    def process(self, random_mode):
        return (random_mode,)
