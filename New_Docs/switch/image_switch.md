# 3/5/10 Images Switch Or Batch

## Description

These nodes allow switching between multiple images or combining them into a batch. Available in three variants for 3, 5, or 10 images, they provide flexible image selection and batch processing capabilities.

## Inputs

### Required:
- **mode**: (`COMBO`) - Operation mode:
  - "Switch_Mode" - Select single image
  - "Batch_Mode" - Combine into batch
- **index**: (`INT`, default: 1) - Selected image in Switch Mode
  - 3 Images: range 1-3
  - 5 Images: range 1-5
  - 10 Images: range 1-10

### Optional:
- **Image_01** to **Image_XX**: (`IMAGE`) - Input images (XX depends on variant)

## Outputs

- **IMAGE**: (`IMAGE`) - Selected/combined images
- **CURRENT_INDEX**: (`INT`) - Current selection index or batch size

## Features

- **Operation Modes**:
  - Single image selection
  - Batch combination
  - Automatic resizing

- **Image Processing**:
  - Batch handling
  - Size normalization
  - Channel order correction
  - Memory optimization

## Example Usage

Switch Mode:
```python
mode: "Switch_Mode"
index: 2
Image_02: [input_image]
# Returns selected image
```

Batch Mode:
```python
mode: "Batch_Mode"
# Returns all connected images as batch
# Automatically resizes to match first image
```

## Notes

- Automatic size matching
- Lanczos resampling
- Memory-efficient processing
- Batch size reporting
- Channel order handling
- Connection validation
- Error reporting
