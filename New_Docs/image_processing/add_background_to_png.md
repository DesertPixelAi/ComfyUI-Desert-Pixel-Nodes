# DP Add Background To PNG

<img src="https://github.com/user-attachments/assets/add_background_to_png.png" alt="DP_Add_Background_To_PNG" style="float: left; margin-right: 10px;"/>

## Description

The Add Background to PNG node allows you to add solid color backgrounds to images with transparency, with support for mask inversion and layer duplication for enhanced effects. This node is particularly useful for preparing images for formats or systems that don't support transparency.

## Inputs

### Required:
- **image**: (`IMAGE`) - Input image to process
- **mask**: (`MASK`) - Mask defining transparent areas
- **background_color**: (`COMBO`, default: "white") - Color for the background
  - Available colors: white, black, red, green, blue, yellow, purple, cyan, orange, pink, gray, brown, navy, lime, magenta
- **invert_mask**: (`COMBO`, default: "false") - Option to invert the mask
  - "false" - Use mask as is
  - "true" - Invert the mask
- **duplicate_layers**: (`INT`, default: 1, range: 1-5) - Number of times to stack the image layer
  - Higher values can create more complex blending effects

## Outputs

- **image**: (`IMAGE`) - Processed image with added background
- **mask**: (`MASK`) - Final mask after processing

## Features

- **Color Selection**: 15 predefined background colors
- **Mask Inversion**: Option to invert transparency areas
- **Layer Stacking**: Multiple layer support for complex effects
- **Smart Blending**: Progressive layer blending for smooth results
- **Alpha Channel Support**: Handles both RGB and RGBA inputs
- **Error Handling**: Graceful fallback to original image on errors

## Example Usage

Basic Background Addition:
```
background_color: "white"
invert_mask: "false"
duplicate_layers: 1
```

Complex Effect with Multiple Layers:
```
background_color: "cyan"
invert_mask: "true"
duplicate_layers: 3
```

## Notes

- Supports both RGB and RGBA input images
- Layer duplication can create interesting depth effects
- Mask inversion useful for negative space effects
- All colors use standard RGB values (0-1 range)
- Processing is done with GPU acceleration when available
- Maintains original image quality and dimensions 
