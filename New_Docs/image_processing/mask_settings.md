# DP Mask Settings

## Description

The Mask Settings node provides advanced mask manipulation tools, including expansion/erosion and blur effects. It can process both mask inputs and convert images to masks, offering precise control over mask modifications.

## Inputs

### Required:
- **expand**: (`INT`, default: 0, range: -256 to 256) - Expands or erodes the mask
  - Positive values: Dilate mask outward
  - Negative values: Erode mask inward
  - Zero: No expansion/erosion
- **blur**: (`INT`, default: 0, range: 0-256) - Gaussian blur strength
  - 0: No blur
  - Higher values: Stronger blur effect

### Optional:
- **mask**: (`MASK`) - Input mask to process
- **image_input**: (`IMAGE`) - Alternative input as image (automatically converted to mask)

## Outputs

- **mask**: (`MASK`) - Processed mask
- **image**: (`IMAGE`) - Mask converted to RGB image format

## Features

- **Mask Processing**:
  - Expansion/Erosion with adjustable strength
  - Gaussian blur with variable radius
  - Automatic value clamping (0-1)
  - Reflection padding for edge handling

- **Input Flexibility**:
  - Accepts both mask and image inputs
  - Automatic grayscale conversion
  - RGB to luminance weighting
  - Batch processing support

- **Quality Controls**:
  - High-quality Gaussian kernel
  - Separable blur for efficiency
  - Precise edge handling
  - Maintains mask integrity

## Example Usage

Basic Mask Expansion:
```python
expand: 10  # Dilate mask by 10 pixels
blur: 0     # No blur
```

Soft Mask Edges:
```python
expand: 0   # No expansion
blur: 5     # Soft blur effect
```

## Notes

- At least one input (mask or image) required
- Processes in floating-point precision
- Uses reflection padding for better edge results
- GPU-accelerated operations
- Memory-efficient processing
- Maintains batch dimensions 
