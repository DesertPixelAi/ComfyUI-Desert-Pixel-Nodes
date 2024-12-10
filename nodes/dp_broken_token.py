class DPBrokenToken:
    """
    A ComfyUI node for analyzing and splitting Flux prompts based on user-defined token counts.
    """
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "Enter your prompt here"
                }),
                "max_tokens_part_1": ("INT", {
                    "default": 77,
                    "min": 0,
                    "max": 2000,
                    "step": 1
                }),
                "max_tokens_part_2": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 2000,
                    "step": 1
                })
            }
        }
    
    RETURN_TYPES = ("INT", "STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("total_tokens", "info", "Text part 1", "Text part 2", "Text part 3")
    FUNCTION = "analyze_tokens"
    CATEGORY = "DP/text"
    
    def analyze_tokens(self, prompt: str, max_tokens_part_1: int, max_tokens_part_2: int):
        from .tokenizer_utils import FluxTokenizer
        
        # Analyze the prompt
        result = FluxTokenizer.analyze_prompt_with_splits(prompt, max_tokens_part_1, max_tokens_part_2)
        
        # Extract the total token count from the info string
        info = result["info"]
        try:
            # Find the token count in the info string
            token_count_str = info.split("Total token count = ")[1].split("\n")[0]
            total_tokens = int(token_count_str)
        except:
            total_tokens = 0  # Fallback if parsing fails
        
        return (
            total_tokens,  # Return the parsed total tokens
            result["info"],
            result["part1"],
            result["part2"],
            result["part3"]
        )

NODE_CLASS_MAPPINGS = {
    "DPBrokenToken": DPBrokenToken
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DPBrokenToken": "DP Broken Token (Flux)"
}