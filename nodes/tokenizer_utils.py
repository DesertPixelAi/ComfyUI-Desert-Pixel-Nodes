import re
from typing import Dict
from transformers import AutoTokenizer

class FluxTokenizer:
    _tokenizer1 = None
    _tokenizer2 = None
    
    @classmethod
    def _init_tokenizers(cls):
        if cls._tokenizer1 is None:
            try:
                cls._tokenizer1 = AutoTokenizer.from_pretrained("openai/clip-vit-large-patch14")
                cls._tokenizer2 = AutoTokenizer.from_pretrained("laion/CLIP-ViT-bigG-14-laion2B-39B-b160k")
            except Exception as e:
                print(f"Warning: Could not load CLIP tokenizers for Flux. Using fallback. Error: {e}")
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text for tokenization"""
        return re.sub(r'\s+', ' ', text.strip())
    
    @classmethod
    def count_tokens(cls, text: str) -> int:
        """Accurate token counting for Flux using SDXL tokenizers"""
        if not text:
            return 0
            
        cls._init_tokenizers()
        
        try:
            if cls._tokenizer1 and cls._tokenizer2:
                # Use both CLIP tokenizers like SDXL
                count1 = len(cls._tokenizer1.encode(text))
                count2 = len(cls._tokenizer2.encode(text))
                return max(count1, count2)
        except Exception as e:
            print(f"Warning: Flux token counting failed. Using fallback. Error: {e}")
        
        # Fallback to simple counting if tokenizers fail
        tokens = re.findall(r'\w+|[^\w\s]', text.lower())
        return len(tokens)
    
    @classmethod
    def split_tokens_multi(cls, text: str, max_tokens_1: int, max_tokens_2: int) -> tuple[str, str, str]:
        """Split text into three parts based on token counts"""
        text = cls.clean_text(text)
        
        # Initialize parts
        current_text = text
        part1 = part2 = part3 = ""
        
        # Calculate first part
        if max_tokens_1 > 0:
            words = current_text.split()
            temp_text = ""
            for word in words:
                test_text = (temp_text + " " + word).strip()
                if cls.count_tokens(test_text) <= max_tokens_1:
                    temp_text = test_text
                else:
                    break
            part1 = temp_text
            current_text = current_text[len(temp_text):].strip()
        
        # Calculate second part
        if max_tokens_2 > 0 and current_text:
            words = current_text.split()
            temp_text = ""
            for word in words:
                test_text = (temp_text + " " + word).strip()
                if cls.count_tokens(test_text) <= max_tokens_2:
                    temp_text = test_text
                else:
                    break
            part2 = temp_text
            current_text = current_text[len(temp_text):].strip()
        
        # Remaining text goes to part3
        part3 = current_text
        
        return part1, part2, part3
    
    @staticmethod
    def analyze_prompt_with_splits(text: str, max_tokens_1: int, max_tokens_2: int) -> Dict:
        """Analyze prompt and return token information with three-way split"""
        text = FluxTokenizer.clean_text(text)
        part1, part2, part3 = FluxTokenizer.split_tokens_multi(text, max_tokens_1, max_tokens_2)
        
        # Count tokens for each part
        tokens_part1 = FluxTokenizer.count_tokens(part1)
        tokens_part2 = FluxTokenizer.count_tokens(part2)
        tokens_part3 = FluxTokenizer.count_tokens(part3)
        
        # Calculate total tokens
        total_tokens = tokens_part1 + tokens_part2 + tokens_part3
        
        # Create info string with line breaks
        info = f"Total token count = {total_tokens}\nPart 01 = {tokens_part1} tokens\nPart 02 = {tokens_part2} tokens\nPart 03 = {tokens_part3} tokens"
        
        return {
            "info": info,
            "part1": part1,
            "part2": part2,
            "part3": part3
        }

