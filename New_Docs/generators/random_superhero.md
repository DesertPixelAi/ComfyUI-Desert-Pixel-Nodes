# DP Random Superhero Generator

<img src="https://github.com/user-attachments/assets/random_superhero.png" alt="DP_Random_Superhero" style="float: left; margin-right: 10px;"/>

## Description

The Random Superhero Generator creates detailed prompts for superhero character generation, combining various elements including powers, costumes, settings, and visual effects. It features both random and fixed generation modes with adjustable style complexity.

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

- **STRING**: Complete superhero prompt combining all elements

## Generated Prompt Structure

The output prompt combines elements from multiple categories:
1. **Hero Identity**: Name and base character type
2. **Physical Attributes**: Gender and ethnicity
3. **Costume Elements**: Materials, design, and color scheme
4. **Powers**: Source and visual effects
5. **Scene Components**: Setting and action pose
6. **Visual Effects**: Lighting and atmosphere
7. **Style Elements**: Multiple artistic styles based on complexity

## Example Output
```
comic art style of an epic generic-superhero female, in cinematic powerful concept photo, frontal view, UltraPhoenix-X157 - cosmic guardian, heroic stance, wearing high-tech mask, quantum energy infused, wearing a nano-fiber advanced armor design in neon-chrome color scheme with a glowing geometric emblem, energy manipulation effects, futuristic cityscape background, dramatic rim lighting, epic atmosphere, Asian ethnicity, inspired by comics art and psychedelic hyper realistic digital illustration, cool and crazy and funny generic-superhero cinematic solo scene, comic book art, digital painting, concept art
```

## Features

- **Dynamic Name Generation**: Creates unique superhero names
- **Comprehensive Character Details**: Including ethnicity and gender
- **Costume System**: Detailed costume descriptions with materials and designs
- **Power Generation**: Various power sources and visual effects
- **Scene Creation**: Dynamic settings and poses
- **Style Integration**: Multiple artistic style combinations
- **Curated Elements**: Components selected from specialized lists:
  - hero_names.txt: Character names
  - hero_base.txt: Character archetypes
  - power_source.txt: Origin of powers
  - costume_material.txt: Suit materials
  - costume_design.txt: Costume styles
  - powers_visual.txt: Power effects
  - scene_setting.txt: Environments
  - action_pose.txt: Character poses
  - lighting_effects.txt: Scene lighting
  - atmosphere.txt: Mood and atmosphere
  - styles.txt: Artistic styles
  - color_schemes.txt: Costume colors
  - hero_logos.txt: Emblem designs
  - face_masks.txt: Mask types
  - ethnicities.txt: Character ethnicities

## Notes

- Generates complete character concepts with consistent details
- Fixed mode perfect for series of related characters
- Randomize mode creates unique heroes each time
- Automatic prompt cleaning ensures proper formatting
- Compatible with most image generation systems
- Extensive customization through multiple element categories
