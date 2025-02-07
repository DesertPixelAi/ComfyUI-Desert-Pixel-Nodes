# File: smart_prompt_compressor.py
import re
from typing import Dict, List, Tuple
import numpy as np
from transformers import AutoTokenizer
from .tokenizer_utils import FluxTokenizer

class DP_SmartPromptCompressor:
    """
    A ComfyUI node that intelligently compresses prompts to fit within token limits
    while preserving the most important semantic information.
    """
    
    def __init__(self):
        # Initialize importance weights for different prompt elements
        self.importance_weights = {
            'subject': 1.0,      # Core subject matter
            'style': 0.9,       # Artistic style
            'scene': 0.8,       # Scene description
            'effect': 0.7,      # Visual effects
            'composition': 0.6,  # Technical composition
            'quality': 0.9,     # Add quality terms
            'color': 0.8,       # Add color terms
            'lighting': 0.8,    # Add lighting terms
            'emotion': 0.85     # Add emotional terms
        }
        
        # Keywords that indicate different element types
        self.element_indicators = {
            'subject': ['featuring', 'portrait', 'character', 'person', 'hero', 'figure', 
                       'main', 'focus', 'centered', 'protagonist'],
            'style': ['style of', 'inspired by', 'aesthetic', 'artistic', 'rendered in', 
                     'drawn in', 'painted in', 'illustrated'],
            'scene': ['scene', 'setting', 'environment', 'background', 'landscape', 
                     'location', 'place', 'world'],
            'effect': ['glowing', 'pulsing', 'emanating', 'swirling', 'flowing', 
                      'shimmering', 'sparkling', 'radiating'],
            'composition': ['depth of field', 'composition', 'perspective', 'shot', 
                          'angle', 'view', 'framing', 'layout'],
            'quality': ['detailed', 'high quality', 'masterpiece', 'professional', 
                       'best quality', 'highly detailed'],
            'color': ['colorful', 'vibrant', 'dark', 'bright', 'saturated', 
                     'monochrome', 'palette'],
            'lighting': ['lighting', 'illuminated', 'backlit', 'sunlight', 'shadows', 
                        'dramatic lighting'],
            'emotion': ['peaceful', 'dramatic', 'serene', 'intense', 'calm', 
                       'energetic', 'mood']
        }
        
        # Model-specific token limits
        self.token_limits = {
            "sd1": 77,
            "sd2": 77,
            "sdxl": 77,
            "flux": 225  # Flux has a higher token limit
        }
        
        # Initialize tokenizers for different models
        try:
            self.sd1_tokenizer = AutoTokenizer.from_pretrained("openai/clip-vit-large-patch14")
            self.sd2_tokenizer = AutoTokenizer.from_pretrained("stabilityai/stable-diffusion-2")
            self.sdxl_tokenizer1 = AutoTokenizer.from_pretrained("openai/clip-vit-large-patch14")
            self.sdxl_tokenizer2 = AutoTokenizer.from_pretrained("laion/CLIP-ViT-bigG-14-laion2B-39B-b160k")
            self.flux_tokenizer = AutoTokenizer.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0")  # Flux uses SDXL tokenizer
        except Exception as e:
            print(f"Warning: Could not load tokenizers. Using fallback token estimation. Error: {e}")
            self.sd1_tokenizer = self.sd2_tokenizer = self.sdxl_tokenizer1 = self.sdxl_tokenizer2 = self.flux_tokenizer = None
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "target_tokens": ("INT", {
                    "default": 77,
                    "min": 1,
                    "max": 225,
                    "step": 1,
                    "display_text": "Target Token Count"
                }),
                "model_type": (["sd1", "sd2", "sdxl", "flux"], {
                    "default": "sd2",
                    "display_text": "Model Type"
                }),
                "preservation_mode": (["balanced", "subject_focus", "style_focus"], {
                    "default": "balanced",
                    "display_text": "Preservation Mode"
                })
            },
            "optional": {
                "prompt": ("STRING", {
                    "multiline": True,
                    "display_text": "Input Prompt",
                    "defaultinput": True,
                    "forceInput": True
                })
            }
        }
    
    RETURN_TYPES = ("STRING", "INT", "STRING")
    RETURN_NAMES = ("compressed_prompt", "token_count", "compression_info")
    FUNCTION = "compress_prompt"
    CATEGORY = "DP/text"
    
    def _count_tokens(self, text: str, model_type: str = "sd2") -> int:
        """Count tokens based on the specific model type."""
        if not text.strip():
            return 0
        
        try:
            if model_type == "flux":
                # Use the shared FluxTokenizer
                return FluxTokenizer.count_tokens(text)
            elif model_type == "sd1" and self.sd1_tokenizer:
                return len(self.sd1_tokenizer.encode(text))
            elif model_type == "sd2" and self.sd2_tokenizer:
                return len(self.sd2_tokenizer.encode(text))
            elif model_type == "sdxl" and self.sdxl_tokenizer1 and self.sdxl_tokenizer2:
                return max(
                    len(self.sdxl_tokenizer1.encode(text)),
                    len(self.sdxl_tokenizer2.encode(text))
                )
            else:
                # Fallback: rough estimation
                return len(text.split())
        except Exception as e:
            print(f"Warning: Token counting failed. Using fallback. Error: {e}")
            return len(text.split())
    
    def _split_into_phrases(self, prompt: str) -> List[str]:
        """Split the prompt into meaningful phrases."""
        # Split by commas but preserve special patterns
        phrases = [p.strip() for p in re.split(r',(?![^(]*\))', prompt)]
        return [p for p in phrases if p]
    
    def _score_phrase(self, phrase: str, mode: str) -> float:
        """Improved scoring with context awareness"""
        base_score = 0.0
        phrase_lower = phrase.lower()
        
        # Track matched categories for better context
        matched_categories = set()
        
        # Calculate importance score with category awareness
        for element_type, indicators in self.element_indicators.items():
            if any(indicator in phrase_lower for indicator in indicators):
                weight = self.importance_weights[element_type]
                matched_categories.add(element_type)
                
                # Adjust weights based on preservation mode
                if mode == "subject_focus" and element_type == "subject":
                    weight *= 1.5
                elif mode == "style_focus" and element_type == "style":
                    weight *= 1.5
                
                base_score = max(base_score, weight)
        
        # Context-based adjustments
        if len(matched_categories) > 1:
            # Bonus for phrases that combine multiple aspects
            base_score *= 1.1
        
        # Structural adjustments
        if '(' in phrase:  # Has weights/emphasis
            base_score *= 1.2
        if len(phrase.split()) <= 3:  # Shorter phrases often more core/essential
            base_score *= 1.1
        if any(x in phrase_lower for x in ['main', 'primary', 'key']):
            base_score *= 1.15
            
        return base_score
    
    def _compress_prompt(self, phrases: List[str], target_tokens: int, mode: str) -> Tuple[str, List[str]]:
        """Compress the prompt by selecting the most important phrases that fit within the token limit."""
        # Score all phrases
        scored_phrases = [(phrase, self._score_phrase(phrase, mode)) for phrase in phrases]
        scored_phrases.sort(key=lambda x: x[1], reverse=True)
        
        # Initialize result
        selected_phrases = []
        current_tokens = 0
        excluded_phrases = []
        
        # Try to fit highest-scoring phrases within token limit
        for phrase, score in scored_phrases:
            phrase_tokens = self._count_tokens(phrase + ", ")
            if current_tokens + phrase_tokens <= target_tokens:
                selected_phrases.append(phrase)
                current_tokens += phrase_tokens
            else:
                excluded_phrases.append(phrase)
        
        return ", ".join(selected_phrases), excluded_phrases
    
    def compress_prompt(self, target_tokens: int, model_type: str = "sd2", preservation_mode: str = "balanced", prompt: str = None):
        """Main function to compress the prompt while preserving important information."""
        # Return default values if no prompt is provided
        if prompt is None or not prompt.strip():
            return ("", 0, "No input prompt provided")

        # Validate target tokens against model limit
        model_limit = self.token_limits.get(model_type, 77)
        if target_tokens > model_limit:
            print(f"Warning: Target tokens ({target_tokens}) exceeds {model_type} limit of {model_limit}. Adjusting...")
            target_tokens = model_limit

        # Split prompt into phrases
        phrases = self._split_into_phrases(prompt)
        
        # Compress prompt
        compressed_prompt, excluded = self._compress_prompt(phrases, target_tokens, preservation_mode)
        
        # Count tokens using the specific model tokenizer
        original_tokens = self._count_tokens(prompt, model_type)
        final_tokens = self._count_tokens(compressed_prompt, model_type)
        
        # Generate compression info
        info = f"Model: {model_type.upper()}\n"
        info += f"Token limit: {model_limit}\n"
        info += f"Original tokens: {original_tokens}\n"
        info += f"Compressed tokens: {final_tokens}\n"
        info += f"Compression ratio: {final_tokens/original_tokens:.2%}\n"
        if excluded:
            info += f"\nExcluded phrases:\n" + "\n".join(f"- {p}" for p in excluded)
        
        return (compressed_prompt, final_tokens, info)
