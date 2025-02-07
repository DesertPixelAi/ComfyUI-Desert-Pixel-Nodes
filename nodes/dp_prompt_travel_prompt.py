import random

class DP_Prompt_Travel_Prompt:
    def __init__(self):
        self.id = str(random.randint(0, 2**64))
        
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "positive_prompt": ("STRING", {"multiline": True}),
                "negative_prompt": ("STRING", {"multiline": True}),
            },
            "optional": {
                "positive_in": ("STRING", {"multiline": True, "forceInput": True}),
                "negative_in": ("STRING", {"multiline": True, "forceInput": True}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "process"
    CATEGORY = "DP/prompt"

    def process(self, positive_prompt: str, negative_prompt: str, **kwargs) -> tuple[str]:
        try:
            result = []
            
            # Handle positive prompts
            positive_parts = []
            
            # Add positive_in if connected and has content
            if "positive_in" in kwargs and kwargs["positive_in"] is not None:
                pos_in = str(kwargs["positive_in"]).strip()
                if pos_in:
                    positive_parts.append(pos_in)
                    # Add comma if doesn't end with ", "
                    if not pos_in.endswith(", "):
                        positive_parts[-1] += ", "
            
            # Add positive_prompt if has content
            if positive_prompt:
                positive_parts.append(positive_prompt.strip())
            
            # Combine positive parts
            if positive_parts:
                result.append("".join(positive_parts))
            
            # Handle negative prompts
            negative_parts = []
            
            # Check if we have any negative prompts
            has_negative_in = "negative_in" in kwargs and kwargs["negative_in"] is not None and kwargs["negative_in"].strip()
            has_negative_prompt = negative_prompt and negative_prompt.strip()
            
            if has_negative_in or has_negative_prompt:
                # Add separator only if we have positive content and any negative content
                if result:
                    result.append(" --neg ")
                
                # Add negative_in if connected and has content
                if has_negative_in:
                    neg_in = str(kwargs["negative_in"]).strip()
                    negative_parts.append(neg_in)
                    # Add comma if doesn't end with ", " and we have more negative content coming
                    if has_negative_prompt and not neg_in.endswith(", "):
                        negative_parts[-1] += ", "
                
                # Add negative_prompt if has content
                if has_negative_prompt:
                    negative_parts.append(negative_prompt.strip())
                
                # Combine negative parts
                result.append("".join(negative_parts))
            
            return ("".join(result),)
            
        except Exception as e:
            print(f"Error in DP_Prompt_Travel_Prompt: {str(e)}")
            return ("",) 