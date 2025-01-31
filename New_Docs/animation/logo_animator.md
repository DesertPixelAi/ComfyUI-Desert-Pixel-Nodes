# DP Logo Animator

<img src="https://github.com/user-attachments/assets/d56d6536-ea7a-4819-98b6-cc5c4b19f5f3" alt="DP_Logo_Animator" style="float: left; margin-right: 10px;"/>

## Description

The DP Logo Animator node creates dynamic animations for logos using scale transformations. It supports various animation patterns and batch processing, making it ideal for creating logo animations for video content. The node features automatic background detection and multiple animation styles, with the ability to process both single images and batches.

## Inputs

### Required:
- **images**: (`IMAGE`) - Input logo image(s) to be animated
- **frame_count**: (`INT`, default: 48, range: 2-300) - Number of frames in the animation sequence
- **min_scale**: (`FLOAT`, default: 0.2, range: 0.1-0.99) - Minimum scale size during animation
- **background**: (`COMBO`, ["Auto", "Black", "White"]) - Background color selection
- **animation_pattern**: (`COMBO`) - Animation style selection:
  - "Big>Small>Big" - Full cycle from large to small and back
  - "Small>Big>Small" - Full cycle from small to large and back
  - "Big>Small" - Single direction scaling down
  - "Small>Big" - Single direction scaling up
  - "batch_flow_big>small" - Batch processing with continuous downscaling
  - "batch_flow_small>big" - Batch processing with continuous upscaling
  - "batch_alternate_big>small" - Alternating scale patterns in batch
  - "batch_alternate_small>big" - Alternating scale patterns in batch

## Outputs

- **IMAGE**: Animated sequence of frames

## Usage Examples

### Basic Logo Animation
# Single logo animation
images: single logo image
frame_count: 48
min_scale: 0.2
background: "Auto"
animation_pattern: "Big>Small>Big"
Result: Smooth scaling animation with 48 frames

### Batch Processing
# Multiple logos with alternating patterns
images: batch of logos (up to 10)
frame_count: 24
animation_pattern: "batch_alternate_big>small"
Result: Each logo alternates between scaling patterns

## Notes

- **Background Detection**:
  - Auto mode samples edges to determine background color
  - Manual selection available for black or white backgrounds
  - Works with both RGB and RGBA images

- **Batch Processing**:
  - Supports up to 10 images in a batch
  - Different animation patterns for batch processing
  - Each image in batch can have unique animation timing

- **Animation Patterns**:
  - Single patterns work on individual images
  - Batch patterns create coordinated animations across multiple images
  - Flow patterns create continuous transitions
  - Alternate patterns create varied effects across the batch

- **Performance**:
  - Automatically handles image format conversion
  - Maintains aspect ratio during scaling
  - Efficiently processes batches with tensor operations
  - Memory usage scales with frame count and batch size
