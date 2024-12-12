# DP Prompt Styler
<img src="https://github.com/user-attachments/assets/5a2eec5a-000d-4837-aaf5-f098273d1e2d" alt="DP_Prompt_Styler" style="float: left; margin-right: 10px;"/>

## Description

A versatile prompt styling node that combines your main prompt with various customizable style elements. Each style category is loaded from separate text files, making it easy to add or modify styles. The node automatically formats the combined prompt with proper spacing and commas.

## Inputs

**Text Inputs:**
- `Main_Prompt`: Your primary prompt text
- `extra_text`: Additional text to append at the end

**Style Selections** (all include "none" option):
- `DepthStyle`: Depth and perspective styles
- `cameraAngles`: Various camera viewing angles
- `colorTheme`: Color schemes and palettes
- `FaceMood`: Facial expressions and emotions
- `timeOfDay`: Time periods and lighting conditions
- `atmosphere`: Environmental and mood settings
- `lighting`: Lighting styles and effects
- `filter`: Post-processing and filter effects
- `CameraType`: Camera and lens specifications

## Outputs

- `Modified Prompt`: Combined and formatted prompt string with all selected styles

## Example Usage

Input:
```
Main_Prompt: "a portrait of a woman"
DepthStyle: "shallow depth of field"
cameraAngles: "close up"
colorTheme: "warm colors"
FaceMood: "smiling"
timeOfDay: "golden hour"
atmosphere: "dreamy"
lighting: "soft lighting"
filter: "film grain"
CameraType: "85mm lens"
extra_text: "highly detailed"
```

Output:
```
a portrait of a woman, shallow depth of field, close up, warm colors, smiling, golden hour, dreamy, soft lighting, film grain, 85mm lens, highly detailed
```

Note: Selections set to "none" are automatically excluded from the final prompt.
