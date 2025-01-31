# Prompt Inverter

## Description

This node inverts prompts by replacing words with their antonyms, using both a comprehensive custom dictionary and optional NLTK support. It's particularly useful for generating contrasting or opposite prompts while preserving prompt structure and special terms.

## Inputs

### Required:
- **inversion_strength**: (`FLOAT`, default: 0.8, range: 0.0-1.0) - Probability of inverting each word
- **generation_mode**: (`COMBO`) - Operation mode:
  - "fixed" - Use consistent inversions
  - "randomize" - Randomize inversions each time
- **use_nltk**: (`BOOLEAN`, default: false) - Enable NLTK antonym lookup

### Optional:
- **input_prompt**: (`STRING`, multiline) - Prompt text to invert

## Outputs

- **STRING**: Inverted prompt text

## Features

- **Antonym Categories**:
  - Colors and Visual Properties
  - Quality and State
  - Size and Scale
  - Emotions and Mood
  - Physical Properties
  - Temperature and Weather
  - Time and Age
  - Life and Nature
  - Sound and Movement
  - Photography Terms
  - Art Styles and Periods
  - Render Quality
  - Materials and Textures
  - Visual Effects
  - Common SD Modifiers

- **Text Processing**:
  - Preserves punctuation
  - Maintains common words
  - Handles multi-word terms
  - Supports NLTK integration

## Example Usage

Basic Inversion:
```python
input_prompt: "A bright, warm sunset with soft clouds"
inversion_strength: 1.0
# Might return: "A dim, cool sunrise with bold clouds"
```

Partial Inversion:
```python
input_prompt: "high quality detailed portrait"
inversion_strength: 0.5
# Might return: "high quality simple portrait"
```

## Notes

- Extensive antonym dictionary
- Preserves prompt structure
- Handles SD-specific terms
- Optional NLTK support
- Consistent seed handling
- Memory-efficient processing
- Detailed logging support
