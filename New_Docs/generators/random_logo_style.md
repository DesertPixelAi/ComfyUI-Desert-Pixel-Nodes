# DP Random Logo Style Generator

<img src="https://github.com/user-attachments/assets/random_logo_style.png" alt="DP_Random_Logo_Style" style="float: left; margin-right: 10px;"/>

## Description

The Random Logo Style Generator creates detailed style prompts for logo generation by combining various design elements including textures, color palettes, lighting effects, and artistic styles. It features both random and fixed generation modes with adjustable complexity levels.

## Inputs

### Required:
- **style_complexity**: (`INT`, default: 3, range: 1-5)
  - Controls the number of combined styles:
    - Level 1: 2 styles
    - Level 2: 3 styles
    - Level 3: 4 styles
    - Level 4: 6 styles
    - Level 5: 8 styles

- **generation_mode**: (`COMBO`, ["fixed", "randomize"])
  - "fixed" - Maintains consistent selections between runs
  - "randomize" - Creates new combinations each time

## Outputs

- **STRING**: Complete style prompt combining all elements

## Generated Prompt Structure

The output prompt combines elements from multiple categories:
1. **Texture**: Surface and material qualities
2. **Color Palette**: Color scheme and combinations
3. **Lighting**: Illumination and shadow effects
4. **Additional Elements**: Extra design features
5. **Base Rendering**: Professional 3D and octane render settings
6. **Style Combinations**: Multiple artistic styles based on complexity level

## Example Output
```
with metallic surface, neon cyberpunk colors, dramatic rim lighting, geometric patterns, ultra detailed, professional 3D rendering, octane render, in the style of minimalist, tech-art, futuristic
```

## Features

- **Persistent Selections**: Fixed mode maintains choices between executions
- **Complexity Control**: Adjustable style density through complexity levels
- **Smart Randomization**: Avoids duplicate style combinations
- **Professional Rendering**: Includes high-quality render settings
- **Curated Elements**: All components selected from carefully curated lists:
  - Texture options from texture.txt
  - Color schemes from color_palette.txt
  - Lighting effects from lighting.txt
  - Additional elements from additional_elements.txt
  - Artistic styles from styles.txt

## Notes

- Higher complexity levels create more diverse and detailed prompts
- Fixed mode is perfect for batch processing with consistent styles
- Randomize mode generates unique combinations each time
- All elements are optimized for logo generation
- Compatible with most image generation systems 
