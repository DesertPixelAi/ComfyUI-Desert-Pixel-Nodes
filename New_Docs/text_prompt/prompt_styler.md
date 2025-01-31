# Prompt Styler

## Description

This node provides comprehensive prompt styling capabilities by combining various artistic and photographic elements. It loads style options from predefined categories and allows for both manual selection and randomization of styles.

## Inputs

### Required:
- **mode**: (`COMBO`) - Operation mode:
  - "Styler_ON" - Apply selected styles
  - "ByPass_All" - Skip style application
  - "Randomize_All" - Randomly select from all categories
- **DepthStyle**: (`COMBO`) - Depth and perspective styles
- **cameraAngles**: (`COMBO`) - Camera angle options
- **colorTheme**: (`COMBO`) - Color themes and palettes
- **FaceMood**: (`COMBO`) - Facial expressions and moods
- **timeOfDay**: (`COMBO`) - Time of day settings
- **atmosphere**: (`COMBO`) - Atmospheric conditions
- **lighting**: (`COMBO`) - Lighting setups
- **filter_effect**: (`COMBO`) - Post-processing filters
- **CameraType**: (`COMBO`) - Camera and lens types

### Optional:
- **pre_text**: (`STRING`) - Text to prepend
- **pre_text_B**: (`STRING`) - Additional prepended text
- **Main_Prompt**: (`STRING`) - Primary prompt text
- **extra_text**: (`STRING`) - Text to append
- **extra_text_B**: (`STRING`) - Additional appended text

## Outputs

- **Modified Prompt**: (`STRING`) - Final styled prompt

## Style Categories

Each category includes:
- "none" - Skip this category
- "randomize" - Random selection from category
- [Category-specific options loaded from data files]

## Features

- **Style Management**:
  - Multiple style categories
  - Individual category control
  - Randomization options
  - Style bypassing
  - Custom style loading

- **Text Processing**:
  - Multi-component assembly
  - Proper spacing
  - Comma separation
  - Empty component filtering

## Example Usage

Basic Styling:
```python
mode: "Styler_ON"
Main_Prompt: "portrait of a person"
lighting: "cinematic lighting"
atmosphere: "foggy"
# Returns: "portrait of a person, cinematic lighting, foggy"
```

Randomization:
```python
mode: "Styler_ON"
Main_Prompt: "landscape"
lighting: "randomize"
timeOfDay: "randomize"
# Returns random selections from lighting and time categories
```

Full Randomization:
```python
mode: "Randomize_All"
Main_Prompt: "cityscape"
# Returns prompt with random selections from all categories
```

## Notes

- Loads styles from external files
- Maintains consistent ordering
- Handles missing style files
- Supports dynamic updates
- Memory-efficient processing
- Automatic style file loading
- Comprehensive error handling
