# DP Big Letters

<img src="https://github.com/user-attachments/assets/c40205d0-6327-47f3-b9f0-29fb3d048ef8" alt="DP_Big_Letters" style="float: left; margin-right: 10px;"/>

## Description

The DP Big Letters node splits text into individual letters and creates images for each letter. It features both batch and cycler modes, with customizable dimensions, padding, fonts, and colors. Perfect for creating animated text effects or stylized letter graphics.

## Inputs

### Required:
- **mode**: (`COMBO`, ["Batch_Mode", "Cycler_Mode"]) - Operation mode selection
  - "Batch_Mode" - Processes all letters at once
  - "Cycler_Mode" - Processes one letter at a time (default)

- **text**: (`STRING`, default: "DESERT PIXEL") - Text to be processed

- **cycle_mode**: (`COMBO`, ["increment", "decrement", "fixed"]) - Letter cycling method
  - Only active in Cycler_Mode

- **index**: (`INT`, default: 0) - Fixed position for letter selection
  - Used when cycle_mode is "fixed"

- **image_width**: (`INT`, default: 1024, range: 64-2048) - Width of output images

- **image_height**: (`INT`, default: 1024, range: 64-2048) - Height of output images

- **padding**: (All `INT`, range: 0-500)
  - **padding_top**: (default: 20)
  - **padding_bottom**: (default: 20)
  - **padding_left**: (default: 20)
  - **padding_right**: (default: 20)

- **font_name**: (`COMBO`) - Available system fonts
- **font_weight**: (`COMBO`) - Available font weights
- **font_color**: (`COMBO`, ["white", "black", "red", "green", "blue", "yellow"])
- **background_color**: (`COMBO`, ["black", "white", "red", "green", "blue", "yellow"])

## Outputs

- **image**: (`IMAGE`) - Generated letter image
- **letter_name**: (`STRING`) - Description of the current letter

## Features

- **Dual Operation Modes**:
  - Batch processing for all letters
  - Cycler mode for sequential letter processing
- **Smart Font Sizing**: Automatically calculates optimal font size
- **Special Character Support**: Handles letters, numbers, and special symbols
- **WebSocket Integration**: Real-time updates for UI elements
- **Flexible Cycling**: Increment, decrement, or fixed position options
- **Error Handling**: Graceful fallback to system fonts

## Example Usage

For Batch Processing:
```
mode: "Batch_Mode"
text: "HELLO"
font_color: "white"
background_color: "black"
```

For Animated Cycling:
```
mode: "Cycler_Mode"
text: "ANIMATION"
cycle_mode: "increment"
font_color: "yellow"
background_color: "blue"
```

## Notes

- Supports both RGB and RGBA image formats
- Automatically skips whitespace characters
- Maintains aspect ratio while fitting letters
- Uses system fonts if specified font is unavailable
- Perfect for creating animated text sequences
- Real-time UI updates in cycler mode
