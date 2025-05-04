import json
import os
import random
from server import PromptServer

class DP_Versatile_Prompt_Subjects_Generator:
    def __init__(self):
        self.prompts = self.load_prompts()
        self.current_index = 1  # Start at 1 since 0 is "None"
        self.id = str(random.randint(0, 2**64))
        self.category_counts = {}  # Track counts per category
        self.category_last_indices = {}  # Track last used index per category
        self.used_indices_per_category = {}  # Track used indices for each category in randomize mode
        self.last_mode = None  # Track last used mode to detect mode changes

    def load_prompts(self):
        try:
            node_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            json_path = os.path.join(node_dir, "data", "versatile_prompts", "versatile_prompts.json")
            
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("prompts", [])
        except Exception as e:
            print(f"Error loading versatile prompts: {e}")
            return []

    @classmethod
    def INPUT_TYPES(cls):
        prompts = ["None"] + [f"{prompt['category']} - {prompt['prompt']}" for prompt in cls().prompts]
        return {
            "required": {
                "prompt_name": (prompts,),
                "prompt_index_control": (["fixed", "randomize", "increment", "decrement"],),
                "index": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 9999,
                    "step": 1
                }),
                "max_from_category": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 10,
                    "step": 1
                }),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID"
            },
        }

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("category", "prompt",)
    FUNCTION = "generate"
    CATEGORY = "DP/text"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        # Force update on every execution
        return float("NaN")

    def get_next_index_in_category(self, current_category, current_index, direction=1):
        category_indices = [i for i, p in enumerate(self.prompts) 
                          if p['category'] == current_category]
        if not category_indices:
            return current_index
        
        current_pos = category_indices.index(current_index) if current_index in category_indices else -1
        if current_pos == -1:
            return category_indices[0]
        
        next_pos = (current_pos + direction) % len(category_indices)
        return category_indices[next_pos]

    def get_next_category(self, current_category, direction=1):
        categories = sorted(set(p['category'] for p in self.prompts))
        current_pos = categories.index(current_category) if current_category in categories else -1
        if current_pos == -1:
            return categories[0]
        
        next_pos = (current_pos + direction) % len(categories)
        return categories[next_pos]

    def generate(self, prompt_name, prompt_index_control, index, max_from_category, unique_id):
        if not self.prompts:
            return ("none", "")

        # Reset tracking if mode changed
        if self.last_mode != prompt_index_control:
            self.used_indices_per_category = {}
            self.category_counts = {}
            self.last_mode = prompt_index_control

        num_prompts = len(self.prompts)
        next_index = self.current_index

        # Handle manual prompt selection first
        if prompt_name != "None":
            selected_index = next(
                (i for i, p in enumerate(self.prompts) 
                 if f"{p['category']} - {p['prompt']}" == prompt_name),
                0
            )
            if prompt_index_control == "fixed":
                next_index = selected_index
        
        # Handle mode-specific behavior
        if prompt_index_control != "fixed" or prompt_name == "None":
            current_prompt = self.prompts[self.current_index]
            current_category = current_prompt['category']

            if max_from_category > 0:
                # Initialize category count if needed
                if current_category not in self.category_counts:
                    self.category_counts[current_category] = 1

                if prompt_index_control in ["increment", "decrement"]:
                    direction = 1 if prompt_index_control == "increment" else -1
                    
                    # Check if we need to move to next category
                    if self.category_counts[current_category] >= max_from_category:
                        next_category = self.get_next_category(current_category, direction)
                        self.category_counts = {next_category: 1}
                        next_index = next(i for i, p in enumerate(self.prompts) 
                                        if p['category'] == next_category)
                    else:
                        next_index = self.get_next_index_in_category(current_category, 
                                                                    self.current_index, 
                                                                    direction)
                        self.category_counts[current_category] += 1

                elif prompt_index_control == "randomize":
                    # Initialize used indices for current category if needed
                    if current_category not in self.used_indices_per_category:
                        self.used_indices_per_category[current_category] = set()

                    # Get available indices for current category (not yet used)
                    available_indices = [i for i, p in enumerate(self.prompts) 
                                       if p['category'] == current_category and 
                                       i not in self.used_indices_per_category[current_category]]
                    
                    # If no available indices in current category or reached max, move to next
                    if (not available_indices or 
                        len(self.used_indices_per_category[current_category]) >= max_from_category):
                        next_category = self.get_next_category(current_category)
                        # Reset used indices for new category
                        self.used_indices_per_category[next_category] = set()
                        self.category_counts = {next_category: 1}
                        available_indices = [i for i, p in enumerate(self.prompts) 
                                           if p['category'] == next_category]
                        current_category = next_category

                    # Choose random unused index
                    next_index = random.choice(available_indices)
                    self.used_indices_per_category[current_category].add(next_index)
                    self.category_counts[current_category] = len(self.used_indices_per_category[current_category])

            else:
                # Original behavior when max_from_category is 0
                if prompt_index_control == "randomize":
                    if num_prompts > 1:
                        while True:
                            next_index = random.randint(0, num_prompts - 1)
                            if next_index != self.current_index or num_prompts <= 2:
                                break
                elif prompt_index_control == "increment":
                    next_index = (self.current_index + 1) % num_prompts
                elif prompt_index_control == "decrement":
                    next_index = (self.current_index - 1)
                    if next_index < 0:
                        next_index = num_prompts - 1

        # Update current index
        self.current_index = next_index

        # Get selected prompt
        if prompt_name == "None":
            selected_prompt = {"category": "", "prompt": ""}
        else:
            selected_prompt = self.prompts[next_index]

        # Update UI
        try:
            PromptServer.instance.send_sync("dp_versatile_prompt_update", {
                "node_id": unique_id,
                "index": next_index,
                "prompt_name": "None" if prompt_name == "None" else f"{selected_prompt['category']} - {selected_prompt['prompt']}"
            })
        except Exception as e:
            print(f"Error sending WebSocket message: {str(e)}")

        return (
            selected_prompt.get("category", ""),
            selected_prompt.get("prompt", "")
        ) 