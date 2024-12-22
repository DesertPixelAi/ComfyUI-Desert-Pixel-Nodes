import re
from typing import Dict

class FluxTokenizer:
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text for tokenization"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        return text
    
    @staticmethod
    def count_tokens(text: str) -> int:
        """Basic token counting for Flux"""
        if not text:
            return 0
        # Split on whitespace and punctuation
        tokens = re.findall(r'\w+|[^\w\s]', text.lower())
        return len(tokens)
    
    @staticmethod
    def split_tokens_multi(text: str, max_tokens_1: int, max_tokens_2: int) -> tuple[str, str, str]:
        """Split text into three parts based on token counts"""
        text = FluxTokenizer.clean_text(text)
        tokens = re.findall(r'\w+|[^\w\s]', text)
        
        # Initialize parts
        part1 = ""
        part2 = ""
        part3 = ""
        
        # Calculate first part
        if max_tokens_1 > 0 and tokens:
            if len(tokens) <= max_tokens_1:
                part1 = " ".join(tokens)
                tokens = []
            else:
                part1 = " ".join(tokens[:max_tokens_1])
                tokens = tokens[max_tokens_1:]
        
        # Calculate second part
        if max_tokens_2 > 0 and tokens:
            if len(tokens) <= max_tokens_2:
                part2 = " ".join(tokens)
                tokens = []
            else:
                part2 = " ".join(tokens[:max_tokens_2])
                tokens = tokens[max_tokens_2:]
        
        # Remaining tokens go to part3
        if tokens:
            part3 = " ".join(tokens)
        
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

