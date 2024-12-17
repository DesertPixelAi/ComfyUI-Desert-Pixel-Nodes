import random

class DP_3Parts_Prompt_Line_Cycler:
    version = '1.0.0'
    def __init__(self):
        self.current_index = 0
        self.last_lines_count = 0
        
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt_mode": (["MY_PROMPT", "RANDOM_PROMPT"],),
                "subject": ("STRING", {"multiline": True, "default": '', "dynamicPrompts": True}),
                "find_replace_subject": ("STRING", {"default": "#sub"}),
                "scene_description": ("STRING", {"multiline": True, "default": '', "dynamicPrompts": True}),
                "style_description": ("STRING", {"multiline": True, "default": '', "dynamicPrompts": True}),
                "index": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "subject_index_control": (['increment', 'decrement', 'randomize', 'fixed'],),
            },
            "optional": {
                "random_prompt": ("STRING", {"forceInput": True}),
            },
            "hidden": {"nodeVersion": DP_3Parts_Prompt_Line_Cycler.version},
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING", "STRING", "INT",)
    RETURN_NAMES = ("full_prompt", "filename", "subject", "scene", "style", "next_index",)
    FUNCTION = "cycle"
    CATEGORY = "DP/text"

    def get_first_five_words(self, text):
        words = text.strip().split()
        selected_words = words[:5]
        return " ".join(selected_words)

    def cycle(self, prompt_mode, subject, find_replace_subject, scene_description, style_description, index, subject_index_control, random_prompt=None):
        # If in RANDOM_PROMPT mode and random_prompt is provided
        if prompt_mode == "RANDOM_PROMPT" and random_prompt is not None:
            filename = self.get_first_five_words(random_prompt)
            return (random_prompt, filename, "", "", "", index)

        # Initialize lines for MY_PROMPT mode
        lines = [line.strip() for line in subject.split('\n') if line.strip()]
        
        # Process scene and style
        processed_scene = scene_description.strip()
        processed_style = style_description.strip()
        
        # If no subject lines, just combine scene and style
        if not lines:
            full_prompt_parts = []
            if processed_scene:
                full_prompt_parts.append(processed_scene)
            if processed_style:
                full_prompt_parts.append(processed_style)
            
            full_prompt = ", ".join(full_prompt_parts)
            filename = self.get_first_five_words(full_prompt) if full_prompt else ""
            return (full_prompt, filename, "", processed_scene, processed_style, index)

        num_lines = len(lines)
        if num_lines != self.last_lines_count:
            self.current_index = 0
            self.last_lines_count = num_lines

        next_index = index  # Initialize next_index with current index

        if subject_index_control == 'increment':
            self.current_index = (self.current_index + 1) % num_lines
            next_index = self.current_index
        elif subject_index_control == 'decrement':
            self.current_index = (self.current_index - 1) % num_lines
            next_index = self.current_index
        elif subject_index_control == 'randomize':
            next_index = random.randint(0, num_lines - 1)
        
        # Ensure index is within bounds
        index = max(0, min(index, num_lines - 1))
        
        # Get the selected subject
        selected_subject = lines[index]
        
        # Process scene and style with replacements
        processed_scene = scene_description.strip()
        processed_style = style_description.strip()
        
        # Replace tokens if they exist
        if find_replace_subject in processed_scene:
            processed_scene = processed_scene.replace(find_replace_subject, selected_subject)
            
        if find_replace_subject in processed_style:
            processed_style = processed_style.replace(find_replace_subject, selected_subject)
        
        # Build full prompt with proper formatting
        full_prompt_parts = []
        
        # Check if replacement token exists in either scene or style
        token_exists = find_replace_subject in scene_description or find_replace_subject in style_description
        
        if token_exists:
            if processed_scene:
                full_prompt_parts.append(processed_scene)
            if processed_style:
                full_prompt_parts.append(processed_style)
        else:
            full_prompt_parts.append(selected_subject)
            if processed_scene:
                full_prompt_parts.append(processed_scene)
            if processed_style:
                full_prompt_parts.append(processed_style)
            
        full_prompt = ", ".join(full_prompt_parts)
        
        # Generate filename
        if selected_subject.strip():
            filename = self.get_first_five_words(selected_subject)
        else:
            filename = self.get_first_five_words(full_prompt)
        
        return (full_prompt, filename, selected_subject, processed_scene, processed_style, next_index)
