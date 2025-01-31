# Image Loaders

The DP Image Loaders are a collection of nodes designed to load and process images with varying levels of complexity. Each loader offers different features to suit various workflow needs.

## DP Load Image Effects

The full-featured image loader with comprehensive effect processing.

### Inputs
- **image**: (`IMAGE_UPLOAD`) - Image file to load
- **effect_strength**: (`FLOAT`, default: 1.0, range: 0.0-1.0) - Global strength for effects
- **effect_A** to **effect_D**: (`COMBO`) - Effect selection for each output
- **resize_image**: (`BOOLEAN`, default: True) - Option to resize output
- **width**: (`INT`, default: 1024, range: 64-2048) - Output width if resizing
- **height**: (`INT`, default: 1024, range: 64-2048) - Output height if resizing

### Outputs
- **image_A** to **image_D**: (`IMAGE`) - Processed images
- **filename**: (`STRING`) - Original filename
- **dp_prompt**: (`STRING`) - Embedded prompt text
- **dp_negative_or_other**: (`STRING`) - Embedded negative prompt/metadata

## DP Load Image Effects Small

A streamlined version with two effect outputs.

### Inputs
- **image**: (`IMAGE_UPLOAD`) - Image file to load
- **effect_strength**: (`FLOAT`, default: 1.0, range: 0.0-1.0) - Global strength for effects
- **effect_A**, **effect_B**: (`COMBO`) - Effect selection for outputs
- **resize_image**: (`BOOLEAN`, default: True) - Option to resize output
- **width**: (`INT`, default: 1024, range: 64-2048) - Output width if resizing
- **height**: (`INT`, default: 1024, range: 64-2048) - Output height if resizing

### Outputs
- **image_A**, **image_B**: (`IMAGE`) - Processed images
- **filename**: (`STRING`) - Original filename
- **dp_prompt**: (`STRING`) - Embedded prompt text
- **dp_negative_or_other**: (`STRING`) - Embedded negative prompt/metadata

## DP Load Image Minimal

The simplest version for basic image loading.

### Inputs
- **image**: (`IMAGE_UPLOAD`) - Image file to load
- **resize_image**: (`BOOLEAN`, default: True) - Option to resize output
- **width**: (`INT`, default: 1024, range: 64-2048) - Output width if resizing
- **height**: (`INT`, default: 1024, range: 64-2048) - Output height if resizing

### Outputs
- **image**: (`IMAGE`) - Loaded image

## Available Effects

### Basic Effects
- Original
- Grayscale
- Flip Horizontal/Vertical
- Rotate (90°, 180°, 270° CCW)
- Edge Detection
- Edge Gradient
- Lineart Anime
- Desaturate

### Strength-Based Effects
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

## Features

- Supports PNG, JPG, JPEG, and WebP formats
- GPU-accelerated processing
- EXIF orientation handling
- Automatic color space conversion
- Memory-efficient batch processing
- Error handling with graceful fallback
- Embedded metadata extraction
