# DP Strip Edge Masks

## Description

The Strip Edge Masks node combines multiple images into a strip while generating masks for the edges between images. It's specifically designed for inpainting workflows, creating masks that help blend transitions between images seamlessly. The masks can be used directly with inpainting nodes to smooth out joins between images.

## Inputs

### Required:
- **images**: (`IMAGE`) - Batch of input images (up to 10 images)
- **mode**: (`COMBO`) - Strip arrangement mode:
  - "Horizontal_Right" - Images arranged left to right
  - "Horizontal_Left" - Images arranged right to left
  - "Vertical_Up" - Images arranged bottom to top
  - "Vertical_Down" - Images arranged top to bottom
- **edge_width**: (`INT`, default: 64, range: 0-512) - Width of edge masks in pixels
- **feather**: (`INT`, default: 32, range: 0-256) - Feathering amount for mask edges
- **output_mode**: (`COMBO`) - Mask output format:
  - "separate_masks" - Individual mask for each edge for targeted inpainting
  - "combined_mask" - Single mask covering all edges for batch inpainting

## Outputs

- **combined_strip**: (`IMAGE`) - Combined image strip
- **edge_masks**: (`MASK`) - Inpainting masks for transitions between images

## Features

- **Inpainting-Optimized Masks**:
  - Smooth gradients for natural blending
  - Precise edge control
  - Feathered transitions
  - Multiple mask formats for different inpainting approaches

- **Automatic Sizing**:
  - Target height: 1024px for 1-5 images
  - Target height: 512px for 6-10 images
  - Width calculated to maintain aspect ratio

- **Layout Options**:
  - Horizontal arrangement
  - Vertical arrangement
  - Reversible order
  - Flexible spacing

## Example Usage

Horizontal Strip with Feathered Inpainting:
```python
mode: "Horizontal_Right"
edge_width: 64
feather: 32
output_mode: "separate_masks"
# Connect masks to inpainting node for seamless blending
```

Vertical Strip with Sharp Inpainting Areas:
```python
mode: "Vertical_Down"
edge_width: 48
feather: 0
output_mode: "combined_mask"
# Use with batch inpainting for efficiency
```

## Notes

- Maximum input: 10 images
- Maintains aspect ratios
- Uses Lanczos resampling
- GPU-accelerated processing
- Memory-efficient operation
- Automatic batch handling
- Optimized for inpainting workflows
- Smooth gradient generation for natural blending
