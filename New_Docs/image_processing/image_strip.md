# DP Image Strip

## Description

The Image Strip node combines multiple images into a single strip, either horizontally or vertically. It automatically handles image resizing while maintaining aspect ratios and provides different arrangement options.

## Inputs

### Required:
- **images**: (`IMAGE`) - Batch of input images (up to 10 images)
- **mode**: (`COMBO`) - Strip arrangement mode:
  - "Horizontal_Right" - Images arranged left to right
  - "Horizontal_Left" - Images arranged right to left
  - "Vertical_Up" - Images arranged bottom to top
  - "Vertical_Down" - Images arranged top to bottom

## Outputs

- **image_strip**: (`IMAGE`) - Combined image strip

## Features

- **Automatic Sizing**:
  - Target height: 1024px for 1-5 images
  - Target height: 512px for 6-10 images
  - Width calculated to maintain aspect ratio

- **Smart Processing**:
  - Handles batches up to 10 images
  - Preserves image proportions
  - High-quality Lanczos resizing
  - Automatic batch limiting

- **Flexible Arrangement**:
  - Horizontal strips (left/right)
  - Vertical strips (up/down)
  - Reversible image order

## Example Usage

Horizontal Strip:
```python
mode: "Horizontal_Right"
# Results in images arranged from left to right
```

Vertical Strip:
```python
mode: "Vertical_Down"
# Results in images arranged from top to bottom
```

## Notes

- Maximum input: 10 images
- Maintains aspect ratios
- Uses Lanczos resampling
- Center-aligned resizing
- GPU-accelerated processing
- Memory-efficient operation
