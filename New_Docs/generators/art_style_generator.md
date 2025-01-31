# DP Art Style Generator

## Description

The Art Style Generator node provides access to a curated collection of art styles with associated positive and negative prompts. It features various control modes for style selection and weight adjustment, making it ideal for consistent style application or style exploration in image generation.

## Inputs

### Required:
- **style_name**: (`COMBO`) - Select from available art styles or "None"
  - Includes styles like "Classic Oil Painting", "Contemporary Abstract Expressionism", "Professional Studio Photography", etc.
  - "None" returns empty prompts
- **style_index_control**: (`COMBO`) - Control method for style selection:
  - "fixed" - Uses selected style
  - "randomize" - Randomly selects a new style
  - "increment" - Moves to next style
  - "decrement" - Moves to previous style
- **index**: (`INT`, default: 0, range: 0-9999) - Manual index control
- **positive_weight**: (`FLOAT`, default: 1.0, range: 0.0-10.0) - Weight multiplier for positive prompt

## Outputs

- **style_name**: (`STRING`) - Name of selected style
- **positive_prompt**: (`STRING`) - Style's positive prompt text (with weight if applicable)
- **negative_prompt**: (`STRING`) - Style's negative prompt text

## Style Categories Examples

### Traditional Art
- **Classic Oil Painting**
  - Rich impasto texture, classical composition, traditional medium
- **Traditional Japanese Woodblock**
  - Ukiyo-e style, flat color areas, strong outlines

### Digital & Modern
- **Professional 3D Rendering**
  - Octane render, volumetric rendering, ray tracing
- **Professional Studio Photography**
  - Studio lighting, perfect exposure, commercial quality

### Contemporary & Abstract
- **Contemporary Abstract Expressionism**
  - Bold brushstrokes, emotional color use, dynamic composition
- **Ethereal Watercolor Art**
  - Delicate technique, flowing pigments, translucent layers

### Specialized Styles
- **DP Neural Baroque**
  - Neural networks in baroque style, AI patterns with classical decoration
- **DP Quantum Calligraphy**
  - Physics equations in flowing brushstrokes, artistic typography
- **DP Chrono-Cubism**
  - Temporal mechanics through cubist fragmentation

## Notes

- Style weights can be adjusted using positive_weight parameter
- Weighted prompts are formatted as (prompt:weight)
- Style selection persists between node executions
- Random selection avoids repeating current style
- Styles are loaded from art_styles_v01.json
- UI updates automatically reflect style changes
- Compatible with any prompt-based image generation
- Extensive style library with detailed positive/negative prompts
- Each style optimized for specific artistic characteristics
