class DP_Prompt_Random_Switch:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mode": (["USER_PROMPT", "RANDOM_PROMPT"], {"default": "USER_PROMPT"}),
                "cond_user": ("CONDITIONING",),
                "cond_random": ("CONDITIONING",),
                "prompt_user": ("STRING", {"default": "", "multiline": True}),
                "prompt_random": ("STRING", {"default": "", "multiline": True}),
                "file_name": ("STRING", {"default": ""})
            }
        }
    
    RETURN_TYPES = ("INT", "CONDITIONING", "STRING", "STRING")
    RETURN_NAMES = ("selected_mode", "condition", "prompt", "the_file_name")
    FUNCTION = "switch"
    CATEGORY = "DP/utils"

    def switch(self, mode, cond_user, cond_random, prompt_user, prompt_random, file_name):
        selected_mode = 1 if mode == "USER_PROMPT" else 2
        
        if mode == "USER_PROMPT":
            the_file_name = file_name
        else:
            try:
                after_comma = prompt_random.split(',', 1)[1].strip()
                words = after_comma.split()[:5]
                the_file_name = '_'.join(words)
            except:
                the_file_name = "default_name"
        
        return (
            selected_mode,
            cond_user if mode == "USER_PROMPT" else cond_random,
            prompt_user if mode == "USER_PROMPT" else prompt_random,
            the_file_name
        )

# For ComfyUI registration
NODE_CLASS_MAPPINGS = {
    "DP_Prompt_Random_Switch": DP_Prompt_Random_Switch
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DP_Prompt_Random_Switch": "DP Prompt Random Switch"
} 