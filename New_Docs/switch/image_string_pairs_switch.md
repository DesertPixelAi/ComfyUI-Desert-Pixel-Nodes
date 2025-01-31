# Image And String Pairs Switch

## Description

This node allows switching between up to five image-text pairs, with options for fixed selection or automatic cycling. Each pair consists of an image and an associated string, making it useful for workflows that need synchronized image and text switching.

## Inputs

### Required:
- **cycle_mode**: (`COMBO`) - Selection mode:
  - "fixed" - Use specified index
  - "increment" - Cycle forward through pairs
  - "decrement" - Cycle backward through pairs
- **index**: (`INT`, default: 1, range: 1-5) - Selected pair index in fixed mode

### Optional:
- **Image_01** to **Image_05**: (`IMAGE`) - Input images
- **String_01** to **String_05**: (`STRING`, multiline) - Associated text for each image

## Outputs

- **IMAGE**: (`IMAGE`) - Selected image
- **TEXT**: (`STRING`) - Selected text string
- **INDEX**: (`INT`) - Current pair index

## Features

- **Selection Modes**:
  - Fixed index selection
  - Forward cycling
  - Backward cycling
  - Automatic validation

- **Pair Management**:
  - Up to 5 image-text pairs
  - Dynamic connection detection
  - Synchronized switching
  - Missing input handling

- **UI Integration**:
  - Real-time index updates
  - Visual feedback
  - Error reporting

## Example Usage

Fixed Selection:
```python
cycle_mode: "fixed"
index: 2
Image_02: [input_image]
String_02: "Description text"
```

Auto Cycling:
```python
cycle_mode: "increment"
# Will cycle through all connected pairs
```

## Notes

- Validates connected inputs
- Maintains synchronization
- Reports errors clearly
- Memory-efficient processing
- Automatic batch handling
- UI state persistence
- Flexible connection options
