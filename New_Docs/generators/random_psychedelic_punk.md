# DP Random Psychedelic Punk Generator

<img src="https://github.com/user-attachments/assets/random_psychedelic_punk.png" alt="DP_Random_Psychedelic_Punk" style="float: left; margin-right: 10px;"/>

## Description

The Random Psychedelic Punk Generator creates unique and detailed prompts combining psychedelic art with futuristic punk elements. It features a sophisticated prompt structure that includes character descriptions, settings, lighting, and various artistic styles, with options for both random and fixed generation modes.

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

- **STRING**: Complete prompt combining all elements

## Generated Prompt Structure

The output prompt combines elements from multiple categories:
1. **Primary Style**: Base psychedelic futuristic style
2. **Subject**: Character description with gender
3. **Camera Angle**: Viewpoint and perspective
4. **Setting**: Environment and atmosphere
5. **Lighting**: Illumination effects
6. **Color Palette**: Color scheme
7. **Additional Elements**: Extra details and effects
8. **Style Combinations**: Multiple artistic styles based on complexity
9. **Final Touch**: Finishing quality elements

## Example Output
```
psychedelic art futuristic hyper realistic illustration of a female cyberpunk shaman, dutch angle shot, in a neon-lit underground laboratory, underground punk hipster cyborg atmosphere, volumetric fog lighting, iridescent rainbow colors, surrounded by holographic fractals, in the style of psychedelic art, synthwave, cyberpunk, high quality, high detail, sharp focus, ultra detailed render
```

## Features

- **Gender Integration**: Automatically includes gender in character descriptions
- **Camera Angle System**: Adds cinematic perspectives to scenes
- **Smart Prompt Cleaning**: Removes redundant spaces and fixes punctuation
- **Style Complexity Control**: Adjustable number of combined styles
- **Persistent Selections**: Fixed mode maintains choices between runs
- **Curated Elements**: Components selected from specialized lists:
  - subject.txt: Character descriptions
  - setting.txt: Environments and locations
  - style.txt: Artistic styles
  - color_palette.txt: Color schemes
  - lighting.txt: Lighting effects
  - additional_elements.txt: Extra details
  - final_touch.txt: Quality enhancements
  - camera_angles.txt: Perspective options

## Notes

- All prompts include psychedelic and futuristic elements as base styles
- Higher complexity levels create more diverse style combinations
- Fixed mode perfect for consistent batch generation
- Randomize mode creates unique combinations each time
- Prompt structure optimized for AI image generation
- Automatic prompt cleaning ensures proper formatting
