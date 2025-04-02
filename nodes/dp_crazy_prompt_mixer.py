import random
import re


class DP_Crazy_Prompt_Mixer:
    def __init__(self):
        self.last_seed = 0

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "chunk_size": (
                    "INT",
                    {"default": 3, "min": 1, "max": 10, "step": 1, "display": "number"},
                ),
                "generation_mode": (["fixed", "randomize"], {"default": "randomize"}),
                "mixing_mode": (
                    ["chunks", "full_random", "split_by_commas"],
                    {"default": "split_by_commas"},
                ),
            },
            "optional": {
                "input_prompt": ("STRING", {"multiline": True, "forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "mix_prompt"
    CATEGORY = "DP/text"

    def split_into_chunks(self, words, chunk_size):
        """Split list of words into chunks of specified size, keeping some phrases together."""
        chunks = []
        i = 0
        while i < len(words):
            # Check for common phrases that should stay together
            if i + 1 < len(words):
                next_pair = f"{words[i]} {words[i + 1]}"
                if any(
                    phrase in next_pair.lower()
                    for phrase in [
                        "ultra detailed",
                        "highly detailed",
                        "high quality",
                        "cinematic lighting",
                        "dramatic lighting",
                        "professional photo",
                        "digital art",
                        "concept art",
                        "character design",
                        "ultra realistic",
                        "hyper realistic",
                    ]
                ):
                    chunks.append([words[i], words[i + 1]])
                    i += 2
                    continue

            # Regular chunking
            end = min(i + chunk_size, len(words))
            chunk = words[i:end]
            chunks.append(chunk)
            i += chunk_size
        return chunks

    def mix_words_randomly(self, words, rng):
        """Completely randomize all words while preserving punctuation."""
        # Separate words and punctuation
        text_words = []
        punctuation = []
        for word in words:
            if word in ",.!?;":
                punctuation.append((len(text_words), word))
            else:
                text_words.append(word)

        # Shuffle only the text words
        rng.shuffle(text_words)

        # Reinsert punctuation at their relative positions
        result = []
        text_word_idx = 0
        for pos, punct in sorted(punctuation):
            # Calculate relative position
            current_pos = int((pos / len(text_words)) * len(text_words))
            # Add words up to this position
            while text_word_idx < current_pos and text_word_idx < len(text_words):
                result.append(text_words[text_word_idx])
                text_word_idx += 1
            result.append(punct)

        # Add any remaining words
        while text_word_idx < len(text_words):
            result.append(text_words[text_word_idx])
            text_word_idx += 1

        return result

    def split_into_sentences(self, text):
        """Split text into sentences, preserving punctuation."""
        # Split by common sentence endings and commas, but keep the separators
        sentences = re.split(r"([,.!?;])", text)

        # Recombine separators with their sentences and clean
        cleaned_sentences = []
        current_sentence = ""

        for i, part in enumerate(sentences):
            if part.strip():
                if re.match(r"[,.!?;]", part):
                    current_sentence += part
                    if current_sentence.strip():
                        cleaned_sentences.append(current_sentence.strip())
                    current_sentence = ""
                else:
                    current_sentence += part

        # Add last sentence if it exists
        if current_sentence.strip():
            cleaned_sentences.append(current_sentence.strip())

        return cleaned_sentences

    def mix_prompt(
        self, chunk_size, generation_mode, mixing_mode="chunks", input_prompt=None
    ):
        try:
            # Return empty string if no input prompt
            if input_prompt is None or not input_prompt.strip():
                return ("",)

            if generation_mode == "randomize":
                seed = random.randint(0, 0xFFFFFFFFFFFFFFFF)
                self.last_seed = seed
            else:
                seed = self.last_seed

            rng = random.Random(seed)

            if mixing_mode == "split_by_commas":
                # Split into sentences and shuffle
                sentences = self.split_into_sentences(input_prompt)
                rng.shuffle(sentences)
                return (" ".join(sentences),)

            # Split the prompt into words while preserving some punctuation
            words = re.findall(r"\b[\w\']+\b|[,.!?;]", input_prompt)

            if mixing_mode == "full_random":
                # Full random mode - shuffle all words
                mixed_words = self.mix_words_randomly(words, rng)
            else:
                # Chunk mode - original behavior
                chunks = self.split_into_chunks(words, chunk_size)
                rng.shuffle(chunks)
                mixed_words = [word for chunk in chunks for word in chunk]

            # Reconstruct the prompt with proper spacing around punctuation
            mixed_prompt = ""
            for i, word in enumerate(mixed_words):
                if word in ",.!?;":
                    mixed_prompt = mixed_prompt.rstrip() + word + " "
                else:
                    mixed_prompt += word + " "

            # Clean up the mixed prompt
            mixed_prompt = mixed_prompt.strip()
            # Remove leading punctuation/spaces
            while mixed_prompt and mixed_prompt[0] in ",.!?; ":
                mixed_prompt = mixed_prompt[1:].strip()
            # Remove multiple consecutive punctuation marks
            mixed_prompt = re.sub(r"([,.!?;])\s*([,.!?;])+", r"\1", mixed_prompt)

            return (mixed_prompt.strip(),)

        except Exception as e:
            print(f"Error mixing prompt: {str(e)}")
            return ("",)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")


# Node registration
NODE_CLASS_MAPPINGS = {"DP_Crazy_Prompt_Mixer": DP_Crazy_Prompt_Mixer}

NODE_DISPLAY_NAME_MAPPINGS = {"DP_Crazy_Prompt_Mixer": "Crazy Prompt Mixer"}
