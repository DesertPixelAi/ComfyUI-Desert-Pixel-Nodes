# DP Random Vehicle Generator

<img src="https://github.com/user-attachments/assets/random_vehicle.png" alt="DP_Random_Vehicle" style="float: left; margin-right: 10px;"/>

## Description

The Random Vehicle Generator creates detailed prompts for vehicle concept art by combining various design elements including body types, tires, camera angles, color themes, and scene descriptions. It features both random and fixed generation modes with adjustable style complexity.

## Inputs

### Required:
- **style_complexity**: (`INT`, default: 3, range: 1-5)
  - Controls the number of combined styles:
    - Level 1: 1 style
    - Level 2: 3 styles
    - Level 3: 5 styles
    - Level 4: 7 styles
    - Level 5: 10 styles

- **generation_mode**: (`COMBO`, ["fixed", "randomize"])
  - "fixed" - Maintains consistent selections between runs
  - "randomize" - Creates new combinations each time

## Outputs

- **STRING**: Complete vehicle prompt combining all elements

## Generated Prompt Structure

The output prompt combines elements from multiple categories:
1. **Base Format**: Epic vehicle photography with cinematic concept focus
2. **Camera View**: Angle and filter settings
3. **Vehicle Design**: Body type and tire descriptions
4. **Color Theme**: Color scheme and finish
5. **Scene Setting**: Environment and atmosphere
6. **Style Elements**: Multiple artistic styles based on complexity

## Example Output
```
epic vehicle photography, big cinematic concept vehicle in the center of the frame, dramatic low angle shot with golden hour lighting, the vehicle designed with sleek aerodynamic body with gull-wing doors, and massive off-road tires with chrome rims, metallic midnight blue with carbon fiber accents, parked in a futuristic cityscape with neon reflections, vehicle concept photo, highly detailed, sharp focus, in the style of concept art, automotive photography, digital painting
```

## Features

- **Comprehensive Vehicle Details**: Body types and tire configurations
- **Dynamic Scene Creation**: Various environments and lighting conditions
- **Camera Angle System**: Different viewpoints and filters
- **Color Theme Integration**: Detailed color schemes and finishes
- **Style Complexity Control**: Adjustable number of artistic styles
- **Curated Elements**: Components selected from specialized lists:
  - body_type.txt: Vehicle body designs
  - tires_description.txt: Wheel and tire configurations
  - vehicle_camera_angle_and_filter.txt: Photography angles and effects
  - vehicle_color_theme.txt: Color schemes and finishes
  - vehicle_scene_description.txt: Environmental settings
  - vehicle_art_styles.txt: Artistic rendering styles

## Notes

- Generates complete vehicle concepts with consistent details
- Fixed mode perfect for series of related vehicles
- Randomize mode creates unique designs each time
- Automatic prompt cleaning ensures proper formatting
- Compatible with most image generation systems
- Extensive customization through multiple element categories 
