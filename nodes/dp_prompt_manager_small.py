import random
from server import PromptServer

class DP_Prompt_Manager_Small:
    version = '1.0.0'
    
    def __init__(self):
        self.last_lines_count = 0
        self.current_index = 0
        self.id = str(random.randint(0, 2**64))
        self.color = "#121317"  # Default DP Ocean title color
        self.bgcolor = "#006994"  # Default DP Ocean body color

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt_mode": (["Prompt_Manager_Prompt", "Random_Prompt", "Loaded_Image_Prompt", "Other_Prompt"],),
                "subject": ("STRING", {"multiline": True, "default": '', "dynamicPrompts": True}),
                "subject_index_control": (['increment', 'decrement', 'randomize', 'fixed'],),
                "index": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "find_replace_subject": ("STRING", {"default": "#sub"}),
                "scene_description": ("STRING", {"multiline": True, "default": '', "dynamicPrompts": True}),
                "find_replace_general": ("STRING", {"default": "#place_holder"}),
                "replace_general_with": ("STRING", {"default": "new_word"}),
            },
            "optional": {
                "random_prompt": ("STRING", {"forceInput": True}),
                "loaded_image_metadata": ("STRING", {"forceInput": True}),
                "other_prompt": ("STRING", {"forceInput": True}),
            },
            "hidden": {
                "nodeVersion": DP_Prompt_Manager_Small.version,
                "unique_id": "UNIQUE_ID"
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("Main_Prompt", "filename", "subject", "scene",)
    FUNCTION = "cycle"
    CATEGORY = "DP/text"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def get_first_five_words(self, text):
        if not text or not text.strip():
            return "comfyui_image"
        
        # Remove special characters and replace with space
        cleaned_text = ''.join(char if char.isalnum() else ' ' for char in text)
        
        # Split by any whitespace and filter out empty strings
        words = [word for word in cleaned_text.split() if word]
        
        # Take first 5 words and join with single space
        return ' '.join(words[:5])

    def cycle(self, prompt_mode, subject, find_replace_subject, scene_description, subject_index_control, index, 
              unique_id, find_replace_general, replace_general_with, random_prompt=None, 
              loaded_image_metadata=None, other_prompt=None):
        # Store the current state
        current_color = getattr(self, 'color', "#121317")
        current_bgcolor = getattr(self, 'bgcolor', "#006994")
        random_state = random.getstate()
        
        try:
            # Handle different prompt modes first
            if prompt_mode == "Random_Prompt" and random_prompt is not None:
                full_prompt = random_prompt
                filename = self.get_first_five_words(full_prompt)
                return (full_prompt, filename, "", "")
            elif prompt_mode == "Loaded_Image_Prompt" and loaded_image_metadata is not None:
                full_prompt = loaded_image_metadata
                filename = self.get_first_five_words(full_prompt)
                return (full_prompt, filename, "", "")
            elif prompt_mode == "Other_Prompt" and other_prompt is not None:
                full_prompt = other_prompt
                filename = self.get_first_five_words(full_prompt)
                return (full_prompt, filename, "", "")

            # Clean and validate subject list
            lines = [line.strip() for line in subject.split('\n') if line.strip() and not line.strip().startswith('[Python]')]
            processed_scene = scene_description.strip()

            # Handle empty subject case
            if not lines:
                if processed_scene:
                    filename = self.get_first_five_words(processed_scene)
                    return (processed_scene, filename, "", processed_scene)
                else:
                    return ("", "", "", "")

            num_lines = len(lines)
            next_index = self.current_index

            # Detect changes
            index_changed = index != self.current_index

            # Handle fixed mode and user input changes
            if subject_index_control == "fixed":
                if index_changed:
                    next_index = max(0, min(index, num_lines - 1))
                    self.current_index = next_index
            # Handle mode-specific behavior
            elif subject_index_control == "randomize":
                while True:
                    next_index = random.randint(0, num_lines - 1)
                    if next_index != self.current_index:
                        break
                self.current_index = next_index
            elif subject_index_control == "increment":
                next_index = (self.current_index + 1) % num_lines
                self.current_index = next_index
            elif subject_index_control == "decrement":
                next_index = (self.current_index - 1) % num_lines
                self.current_index = next_index

            # Select subject based on index
            selected_subject = lines[self.current_index]

            # Apply general find & replace to scene_description first
            if find_replace_general and find_replace_general in scene_description:
                processed_scene = scene_description.replace(find_replace_general, replace_general_with)
            else:
                processed_scene = scene_description.strip()

            # Then handle subject replacement
            if find_replace_subject in processed_scene:
                processed_scene = processed_scene.replace(find_replace_subject, selected_subject)
            
            # Build full prompt
            full_prompt_parts = []
            token_exists = find_replace_subject in scene_description
            
            if token_exists:
                if processed_scene:
                    full_prompt_parts.append(processed_scene)
            else:
                full_prompt_parts.append(selected_subject)
                if processed_scene:
                    full_prompt_parts.append(processed_scene)
                
            full_prompt = ", ".join(full_prompt_parts)
            filename = self.get_first_five_words(full_prompt)

            # Update UI
            try:
                PromptServer.instance.send_sync("subject.update", {
                    "node": self.id,
                    "new_subject": selected_subject,
                    "index": self.current_index,
                    "widget_name": "index",
                    "force_widget_update": True
                })
                
                PromptServer.instance.send_sync("update_node", {
                    "node_id": unique_id,
                    "index_value": self.current_index,
                    "color": current_color,
                    "bgcolor": current_bgcolor
                })
            except Exception as e:
                print(f"[Python] Error sending WebSocket message: {str(e)}")

            return (full_prompt, filename, selected_subject, processed_scene)
            
        finally:
            random.setstate(random_state)

class DP_Prompt_Mode_Controller:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt_mode": (["Prompt_Manager_Prompt", "Random_Prompt", "Loaded_Image_Prompt", "Other_Prompt"], 
                              {"default": "Prompt_Manager_Prompt"}),
            }
        }

    RETURN_TYPES = (["Prompt_Manager_Prompt", "Random_Prompt", "Loaded_Image_Prompt", "Other_Prompt"],)
    RETURN_NAMES = ("prompt_mode",)
    FUNCTION = "process"
    CATEGORY = "DP/utils"

    def process(self, prompt_mode):
        return (prompt_mode,)