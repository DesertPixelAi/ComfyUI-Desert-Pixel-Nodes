import random

class DP_Random_Character:
    def __init__(self):
        self.letters = list('abcdefghijklmnopqrstuvwxyz')
        self.numbers = list('0123456789')
        self.history = []
        
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Type": (["random_letter", "random_number", "random_mixed"], {"default": "random_letter"}),
                "Case": (["lowercase", "uppercase", "mixed"], {"default": "mixed"}),
                "Num_Chars": ("INT", {"default": 1, "min": 1, "max": 20, "step": 1, "display": "number"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Characters",)
    FUNCTION = "generate"
    CATEGORY = "DP/utils"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    def get_similar_chars(self, char):
        similar_groups = {
            'c': 'eo', 'e': 'co', 'i': 'l1', 'l': 'i1',
            'o': 'ce0', 'p': 'qb', 'q': 'pb', 'b': 'pq',
            'n': 'm', 'm': 'n', 'u': 'v', 'v': 'u',
            'w': 'vv', 'z': '2', 's': '5',
            '0': 'o', '1': 'il', '2': 'z', '5': 's',
            '6': 'b', '8': 'b', '9': '6'
        }
        return similar_groups.get(char, '')

    def generate_single_char(self, available_chars, case, char_type):
        char = random.choice(available_chars)
        
        if char_type == "random_number":
            return char
        
        if case == "uppercase":
            char = char.upper()
        elif case == "mixed":
            char = char.upper() if random.random() > 0.5 else char.lower()
            
        return char

    def generate(self, Type, Case, Num_Chars):
        result_chars = []
        history_size = 5
        
        for i in range(Num_Chars):
            random.seed(random.randint(0, 0xffffffffffffffff))
            
            if Type == "random_letter":
                available_chars = self.letters.copy()
            elif Type == "random_number":
                available_chars = self.numbers.copy()
            else:  # random_mixed
                available_chars = self.letters.copy() + self.numbers.copy()
            
            # Remove chars from history
            for char in self.history[-history_size:]:
                if char.lower() in available_chars:
                    available_chars.remove(char.lower())
            
            # Always exclude similar chars
            if self.history:
                last_char = self.history[-1].lower()
                similar_chars = self.get_similar_chars(last_char)
                available_chars = [c for c in available_chars if c not in similar_chars]
            
            # If no chars available, reset available chars
            if not available_chars:
                if Type == "random_letter":
                    available_chars = self.letters.copy()
                elif Type == "random_number":
                    available_chars = self.numbers.copy()
                else:
                    available_chars = self.letters.copy() + self.numbers.copy()
            
            char = self.generate_single_char(available_chars, Case, Type)
            result_chars.append(char)
            
            # Update history
            self.history.append(char)
            if len(self.history) > history_size:
                self.history.pop(0)
        
        return ("".join(result_chars),)

