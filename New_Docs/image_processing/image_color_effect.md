# DP Image Color Effect

<img src="https://github.com/user-attachments/assets/image_color_effect.png" alt="DP_Image_Color_Effect" style="float: left; margin-right: 10px;"/>

## Description

The Image Color Effect node applies color overlays to images using various blend modes. It features both single-color effects and a multi-color retro effect generator. The node supports multiple blend modes and adjustable strength settings for precise control over the final look.

## Inputs

### Required:
- **image**: (`IMAGE`) - Input image to process
- **color**: (`COMBO`) - Color for single effect overlay
  - Available colors: purple, yellow, pink, blue, red, orange, magenta, green, violet, cyan
- **blend_mode**: (`COMBO`) - Blending method for color overlay
  - Available modes: Normal, Add, Multiply, Screen, Overlay, Soft Light, Hard Light, Color Dodge, Color Burn, Difference
- **strength**: (`FLOAT`, default: 0.5, range: 0.0-1.0) - Intensity of the color effect

## Outputs

- **single_effect**: (`IMAGE`) - Image with selected color effect applied
- **all_colors_batch**: (`IMAGE`) - Batch of 20 images with different color variations

## Features

- **Single Color Effects**:
  - 10 predefined colors
  - Precise hex color values
  - Adjustable blend strength
  - Multiple blend modes

- **Retro Effect Generator**:
  - 20 unique color variations
  - Randomized color sequence
  - Smart color transitions
  - Batch processing

- **Blend Modes**:
  - Normal blending
  - Additive blending
  - Multiplicative effects
  - Screen and overlay options
  - Light blend variations
  - Color dodge and burn
  - Difference blending

- **Color Palette**:
  - Deep Purple (#24137C)
  - Purple (#7415A8)
  - Yellow (#FFE229)
  - Pink (#FF1AE0)
  - Light Green (#9BFF70)
  - Blue (#339CFF)
  - Red (#DF1111)
  - Orange (#FF950A)
  - Magenta (#A7167E)
  - Cyan (#29FBFF)
  - And more...

## Example Usage

Basic Color Effect:
```
color: "blue"
blend_mode: "Overlay"
strength: 0.5
```

Retro Color Effect:
```
blend_mode: "Screen"
strength: 0.7
// Automatically generates 20 color variations
```

## Notes

- Supports both RGB and RGBA input images
- GPU-accelerated processing
- Random seed generation for unique variations
- Automatic batch processing for retro effects
- Error handling with graceful fallback
- Real-time blend mode preview
