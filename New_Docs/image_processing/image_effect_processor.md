# DP Image Effect Processor

<img src="https://github.com/user-attachments/assets/image_effect_processor.png" alt="DP_Image_Effect_Processor" style="float: left; margin-right: 10px;"/>

## Description

The Image Effect Processor node provides a comprehensive suite of image processing effects with adjustable parameters. It can process up to 4 images simultaneously, applying different effects to each one. The node includes basic transformations, artistic filters, and advanced image processing techniques.

## Inputs

### Required:
- **effect_strength**: (`FLOAT`, default: 1.0, range: 0.0-1.0) - Global strength for effects
- **image_01_effect** to **image_04_effect**: (`COMBO`) - Effect selection for each image
- **resize_image**: (`BOOLEAN`, default: False) - Option to resize output
- **width**: (`INT`, default: 1024, range: 64-2048) - Output width if resizing
- **height**: (`INT`, default: 1024, range: 64-2048) - Output height if resizing

### Optional:
- **image_input_01** to **image_input_04**: (`IMAGE`) - Input images to process

## Available Effects

### Basic Effects (No Parameters):
- Original
- Grayscale
- Flip Horizontal/Vertical
- Rotate (90°, 180°, 270° CCW)
- Edge Detection
- Edge Gradient
- Lineart Anime
- Desaturate

### Strength-Based Effects:
- **Posterize**: (2-8 levels)
- **Sharpen**: (0.0-2.0)
- **Sepia**: (0.0-1.0)
- **Blur**: (0.0-10.0)
- **Emboss**: (0.0-2.0)
- **Palette**: (2-32 colors)
- **Solarize**: (0.0-1.0)
- **Denoise**: (1-5 strength)
- **Vignette**: (0.0-1.0)
- **Glow Edges**: (0.0-1.0)
- **Threshold**: (0.0-1.0)
- **Contrast**: (0.5-2.0)
- **Equalize**: (0.0-1.0)
- **Enhance**: (0.0-2.0)

## Outputs

- **image_output_01** to **image_output_04**: (`IMAGE`) - Processed images

## Features

- **Multi-Image Processing**: Handle up to 4 images simultaneously
- **Flexible Resizing**: Optional output size adjustment
- **Advanced Effects**: Professional-grade image processing
- **Batch Processing**: Efficient handling of multiple images
- **Smart Parameter Mapping**: Intuitive strength controls
- **Error Handling**: Graceful processing of invalid inputs

## Example Usage

Basic Image Enhancement:
```
effect_strength: 0.8
image_01_effect: "enhance"
image_02_effect: "sharpen"
```

Artistic Effect Chain:
```
effect_strength: 1.0
image_01_effect: "edge_detect"
image_02_effect: "glow_edges"
image_03_effect: "vignette"
```

## Notes

- Supports both RGB and RGBA images
- GPU-accelerated processing
- Automatic batch handling
- Preserves image quality
- Memory-efficient operations
- Real-time preview support
