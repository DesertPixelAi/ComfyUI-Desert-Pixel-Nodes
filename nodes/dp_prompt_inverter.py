import random
import re
import logging

logger = logging.getLogger('DP_Nodes')

# NLTK initialization with comprehensive error handling
try:
    import nltk
    from nltk.corpus import wordnet as wn
    NLTK_AVAILABLE = True
    logger.info("NLTK imported successfully")
    
    # Try to download required NLTK data
    required_nltk_data = ['punkt', 'averaged_perceptron_tagger', 'wordnet']
    missing_data = []
    
    for data in required_nltk_data:
        try:
            nltk.data.find(f'tokenizers/{data}' if data == 'punkt' else f'corpora/{data}')
        except LookupError:
            missing_data.append(data)
    
    if missing_data:
        logger.info(f"Downloading missing NLTK data: {', '.join(missing_data)}")
        try:
            for data in missing_data:
                nltk.download(data, quiet=True)
            logger.info("NLTK data downloaded successfully")
        except Exception as e:
            NLTK_AVAILABLE = False
            logger.warning(f"Failed to download NLTK data: {str(e)}")
    
except ImportError as e:
    NLTK_AVAILABLE = False
    logger.warning(f"NLTK import failed: {str(e)}")
except Exception as e:
    NLTK_AVAILABLE = False
    logger.warning(f"Unexpected error initializing NLTK: {str(e)}")

class DP_Prompt_Inverter:
    def __init__(self):
        self.nltk_available = NLTK_AVAILABLE
        if self.nltk_available:
            logger.info("DP_Prompt_Inverter initialized with NLTK support")
        else:
            logger.info("DP_Prompt_Inverter initialized without NLTK support")
            
        self.antonym_dict = {
            # Colors and Visual
            "transparent": "opaque",
            "soft": "bold",
            "pastel": "vivid",
            "light": "dark",
            "bright": "dim",
            "colorful": "monochrome",
            "vibrant": "dull",
            "sharp": "blurry",
            "clear": "hazy",
            "glowing": "dark",
            "shiny": "matte",
            "luminous": "dark",
            "iridescent": "dull",
            
            # Quality and State (enhanced)
            "chaotic": "orderly",
            "damaged": "restored",
            "simple": "intricate",
            "ancient": "futuristic",
            "stable": "unstable",
            "polished": "rough",
            "uniform": "varied",
            
            # Size and Scale (enhanced)
            "confined": "spacious",
            "miniature": "colossal",
            "shallow": "profound",
            "short": "elongated",
            "expansive": "confined",
            "monumental": "modest",
            
            # Emotions and Mood (enhanced)
            "harsh": "gentle",
            "miserable": "blissful",
            "discordant": "melodic",
            "hateful": "compassionate",
            "optimistic": "pessimistic",
            "content": "discontent",
            "hopeful": "despairing",
            "happy": "sad",
            "joyful": "miserable",
            "peaceful": "chaotic",
            "calm": "stormy",
            "serene": "turbulent",
            "gentle": "harsh",
            "friendly": "hostile",
            "loving": "hateful",
            "pleasant": "unpleasant",
            "harmonious": "discordant",
            
            # Physical Properties (enhanced)
            "liquid": "gaseous",
            "sparse": "dense",
            "flexible": "stiff",
            "fragile": "robust",
            "elastic": "rigid",
            "pliable": "brittle",
            "gritty": "smooth",
            
            # Temperature and Weather (enhanced)
            "arctic": "equatorial",
            "humid": "dry",
            "boiling": "chilled",
            "still": "breezy",
            "freezing": "boiling",
            "stormy": "calm",
            "windy": "still",
            "hot": "cold",
            "warm": "cool",
            "sunny": "cloudy",
            "dry": "wet",
            "arid": "humid",
            "tropical": "arctic",
            
            # Time and Age (enhanced)
            "ancient": "contemporary",
            "delayed": "instantaneous",
            "enduring": "momentary",
            "gradual": "instant",
            "immediate": "delayed",
            "premature": "late",
            "fleeting": "enduring",
            "fast": "slow",
            "quick": "slow",
            "rapid": "gradual",
            "young": "old",
            "fresh": "stale",
            "new": "old",
            "modern": "ancient",
            
            # Life and Nature
            "cultivated": "wild",
            "fertile": "barren",
            "flourishing": "withering",
            "alive": "dead",
            "living": "dead",
            "organic": "synthetic",
            "natural": "artificial",
            "wild": "tame",
            "raw": "processed",
            
            # Sound and Movement
            "echoing": "muffled",
            "rhythmic": "irregular",
            "swift": "sluggish",
            "loud": "quiet",
            "noisy": "silent",
            "active": "passive",
            "dynamic": "static",
            "moving": "still",
            "energetic": "lethargic",
            
            # Style and Artistic (enhanced)
            "realistic": "hyperrealistic",
            "ornate": "streamlined",
            "subtle": "theatrical",
            "casual": "extravagant",
            "minimalist": "ornate",
            "formal": "casual",
            "harmonic": "discordant",
            "realistic": "abstract",
            "detailed": "simple",
            "complex": "simple",
            "ornate": "plain",
            "fancy": "simple",
            "dramatic": "subtle",
            "bold": "subtle",
            
            # Digital and Tech (enhanced)
            "vintage": "cutting-edge",
            "analog": "digital-native",
            "fragmented": "integrated",
            "synthetic": "bio-inspired",
            "interactive": "static",
            "precise": "approximate",
            "seamless": "fragmented",
            "digital": "analog",
            "high-tech": "low-tech",
            "futuristic": "vintage",
            "cyber": "natural",
            "synthetic": "organic",
            
            # Fantasy and Reality (enhanced)
            "mundane": "extraordinary",
            "ordinary": "legendary",
            "earthly": "celestial",
            "natural": "paranormal",
            "enchanted": "mundane",
            "otherworldly": "terrestrial",
            "heroic": "ordinary",
            "magical": "mundane",
            "mystical": "ordinary",
            "fantasy": "reality",
            "ethereal": "earthly",
            "supernatural": "natural",
            "epic": "modest",
            
            # Intensity (enhanced)
            "mild": "ferocious",
            "moderate": "unrestrained",
            "minimum": "peak",
            "restrained": "uninhibited",
            "fierce": "gentle",
            "radiant": "dim",
            "exuberant": "restrained",
            "intense": "mild",
            "extreme": "moderate",
            "maximum": "minimum",
            "strong": "weak",
            "powerful": "weak",
            "bold": "subtle",
            
            # Art Mediums and Techniques
            "watercolor": "oil painting",
            "digital": "traditional",
            "painted": "photographed",
            "sketched": "rendered",
            "illustration": "photograph",
            "drawing": "painting",
            "abstract": "photorealistic",
            "stylized": "realistic",
            "cartoon": "hyperrealistic",
            "anime": "western",
            "manga": "realistic",
            "vector": "raster",
            "3d": "2d",
            
            # Photography Terms
            "overexposed": "underexposed",
            "blurred": "sharp",
            "focused": "unfocused",
            "shallow depth": "deep depth",
            "wide-angle": "telephoto",
            "macro": "wide shot",
            "close-up": "full shot",
            "portrait": "landscape",
            "backlit": "front-lit",
            
            # Lighting and Atmosphere
            "bright lighting": "dark lighting",
            "high key": "low key",
            "soft lighting": "harsh lighting",
            "natural lighting": "artificial lighting",
            "daylight": "nighttime",
            "sunlit": "moonlit",
            "direct light": "diffused light",
            "dramatic lighting": "flat lighting",
            "atmospheric": "clear",
            "foggy": "clear",
            "misty": "clear",
            "hazy": "crisp",
            
            # Composition and Framing
            "centered": "off-center",
            "symmetrical": "asymmetrical",
            "balanced": "unbalanced",
            "dynamic": "static",
            "wide shot": "close shot",
            "high angle": "low angle",
            "aerial view": "ground view",
            "front view": "back view",
            "profile": "frontal",
            
            # Art Styles and Periods
            "modern": "classical",
            "contemporary": "vintage",
            "minimalist": "maximalist",
            "baroque": "minimal",
            "gothic": "renaissance",
            "surreal": "realistic",
            "impressionist": "detailed",
            "expressionist": "naturalistic",
            "abstract": "figurative",
            
            # Render Quality and Detail
            "high quality": "low quality",
            "4k": "low-res",
            "8k": "low-res",
            "detailed": "simple",
            "intricate": "basic",
            "complex": "minimal",
            "refined": "rough",
            "polished": "raw",
            "professional": "amateur",
            "masterpiece": "sketch",
            
            # Material and Texture
            "glossy": "matte",
            "metallic": "organic",
            "reflective": "absorbing",
            "transparent": "solid",
            "textured": "smooth",
            "rough": "polished",
            "crystalline": "amorphous",
            "glass": "stone",
            "liquid": "solid",
            "chrome": "rust",
            
            # Color Properties
            "saturated": "desaturated",
            "vivid": "muted",
            "chromatic": "monochromatic",
            "multicolored": "single-colored",
            "iridescent": "flat",
            "neon": "pastel",
            "fluorescent": "subdued",
            "rainbow": "monochrome",
            "gradient": "solid",
            
            # Visual Effects
            "glowing": "dim",
            "sparkling": "dull",
            "shimmering": "static",
            "glittering": "matte",
            "radiating": "absorbing",
            "lens flare": "no flare",
            "bokeh": "sharp",
            "motion blur": "frozen",
            "distorted": "undistorted",
            
            # Artistic Elements
            "detailed background": "simple background",
            "ornate frame": "simple frame",
            "decorative": "plain",
            "patterned": "solid",
            "textured": "smooth",
            "layered": "flat",
            "geometric": "organic",
            "structured": "chaotic",
            
            # Common SD Modifiers
            "best quality": "worst quality",
            "highly detailed": "simple",
            "ultra detailed": "basic",
            "masterpiece": "amateur work",
            "perfect": "flawed",
            "award winning": "unremarkable",
            "trending": "outdated",
            "artstation": "amateur",
            "unreal engine": "basic render",
            "octane render": "simple render",
            "volumetric lighting": "flat lighting",
            "ray tracing": "basic lighting",
            "subsurface scattering": "flat surface",
            "studio quality": "amateur quality",
            "professional": "amateur",
            "cinematic": "casual",
            "commercial": "personal",
            "editorial": "candid",
            
            # New Photography Terms
            "telephoto": "fisheye",
            "crisp": "murky",
            "wide shot": "extreme close-up",
            "landscape": "macro",
            
            # Enhanced Lighting
            "diffused light": "focused light",
            "moonlit": "starlit",
            "flat lighting": "dynamic lighting",
            
            # Enhanced Composition
            "ground view": "sky view",
            "frontal": "angular",
            "unbalanced": "harmonized",
            
            # Enhanced Art Styles
            "renaissance": "deconstructive",
            "naturalistic": "symbolic",
            "classical": "postmodern",
            
            # Enhanced Materials
            "stone": "metallic",
            "amorphous": "crystalline",
            "processed": "raw",
            
            # Enhanced Color Properties
            "monochromatic": "kaleidoscopic",
            "subdued": "exuberant",
            "flat": "multi-dimensional",
            "solid": "gradient-rich",
            
            # Enhanced Visual Effects
            "frozen": "in-motion",
            "static": "animated",
            "no flare": "highlighted",
            
            # Enhanced Artistic Elements
            "plain": "ornamented",
            "chaotic": "harmonious",
            "flat": "layered",
            "organic": "architectural",
            
            # Enhanced SD Modifiers
            "basic lighting": "volumetric lighting",
            "outdated": "forward-thinking",
            "unremarkable": "iconic",
            "personal": "commercialized"
        }
        self.last_seed = 0

    def get_nltk_antonym(self, word):
        if not self.nltk_available:
            return None
            
        try:
            # Get synsets for the word
            synsets = wn.synsets(word)
            if not synsets:
                return None
                
            # Look for antonyms in all synsets
            for syn in synsets:
                for lemma in syn.lemmas():
                    if lemma.antonyms():
                        antonym = lemma.antonyms()[0].name()
                        logger.debug(f"NLTK found antonym for '{word}': '{antonym}'")
                        return antonym
            
            logger.debug(f"No NLTK antonym found for '{word}'")
            return None
            
        except Exception as e:
            logger.warning(f"Error getting NLTK antonym for '{word}': {str(e)}")
            return None

    def get_antonym(self, word, use_nltk=False):
        word_lower = word.lower()
        
        # First try our custom dictionary
        if word_lower in self.antonym_dict:
            antonym = self.antonym_dict[word_lower]
            logger.debug(f"Found custom antonym for '{word}': '{antonym}'")
            return antonym
            
        # Then try NLTK if enabled and available
        if use_nltk and self.nltk_available:
            nltk_antonym = self.get_nltk_antonym(word_lower)
            if nltk_antonym:
                return nltk_antonym
                
        # If no antonym found, return original word
        logger.debug(f"No antonym found for '{word}', keeping original")
        return word

    def invert_prompt(self, inversion_strength, generation_mode, use_nltk=False, input_prompt=None):
        try:
            # Return empty string if no input prompt
            if input_prompt is None or not input_prompt.strip():
                return ("",)

            if generation_mode == "randomize":
                seed = random.randint(0, 0xffffffffffffffff)
                self.last_seed = seed
            else:
                seed = self.last_seed

            rng = random.Random(seed)
            
            # Split into words while preserving punctuation
            words = re.findall(r'\b[\w\'-]+\b|[,.!?;]', input_prompt)
            
            inverted_words = []
            for word in words:
                # Skip punctuation and common words
                if word in ",.!?;" or word.lower() in {"a", "an", "the", "in", "on", "at", "to", "for", "of", "with", "by"}:
                    inverted_words.append(word)
                    continue
                    
                # Determine if we should invert this word based on inversion_strength
                if rng.random() < inversion_strength:
                    antonym = self.get_antonym(word, use_nltk)
                    inverted_words.append(antonym)
                else:
                    inverted_words.append(word)
            
            # Reconstruct the prompt
            inverted_prompt = ' '.join(inverted_words)
            
            # Clean up spacing around punctuation
            inverted_prompt = re.sub(r'\s+([,.!?;])', r'\1', inverted_prompt)
            
            logger.debug(f"Inverted prompt: '{input_prompt}' -> '{inverted_prompt}'")
            return (inverted_prompt,)
            
        except Exception as e:
            logger.error(f"Error inverting prompt: {str(e)}")
            return (input_prompt,)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "inversion_strength": ("FLOAT", {
                    "default": 0.8,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1
                }),
                "generation_mode": (["fixed", "randomize"], {"default": "randomize"}),
                "use_nltk": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "input_prompt": ("STRING", {"multiline": True, "forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "invert_prompt"
    CATEGORY = "DP/text"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

# Node registration
NODE_CLASS_MAPPINGS = {
    "DP_Prompt_Inverter": DP_Prompt_Inverter
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DP_Prompt_Inverter": "Prompt Inverter"
}
