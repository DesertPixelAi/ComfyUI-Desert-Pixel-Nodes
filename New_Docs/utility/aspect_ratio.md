# Aspect Ratio Nodes

## Description

These nodes work together to manage image dimensions. The Aspect Ratio Picker provides predefined aspect ratios loaded from a configuration file, while the Custom Aspect Ratio node allows manual dimension settings.

## DP Aspect Ratio Picker

### Inputs

#### Required:
- **aspect_ratio**: (`COMBO`) - Predefined aspect ratio selections loaded from file

#### Optional:
- **custom_settings**: (`CUSTOM_SETTINGS`) - Connection from Custom Aspect Ratio node

### Outputs

- **width**: (`INT`) - Selected width dimension
- **height**: (`INT`) - Selected height dimension

## DP Custom Aspect Ratio

### Inputs

#### Required:
- **width**: (`INT`, default: 1024, range: 256-2048, step: 8) - Custom width setting
- **height**: (`INT`, default: 1024, range: 256-2048, step: 8) - Custom height setting

### Outputs

- **custom_settings**: (`CUSTOM_SETTINGS`) - Dimensions for Aspect Ratio Picker

### Important Note
When the Custom Aspect Ratio node is connected to an Aspect Ratio Picker, it will override the Picker's predefined ratio settings. This allows for dynamic control of dimensions through node connections rather than preset selections.

## Features

- **Ratio Management**:
  - File-based configuration
  - Custom dimension support
  - Dynamic overrides
  - Cached ratio loading

- **Dimension Processing**:
  - Validation checks
  - Error handling
  - Default fallbacks
  - Step-size enforcement

## Example Usage

Predefined Ratio:
```python
aspect_ratio: "16:9 (1920x1080)"
# Returns: width=1920, height=1080
```

Custom Dimensions:
```python
# Custom Aspect Ratio Node
width: 1280
height: 720
# When connected to Aspect Ratio Picker, overrides preset selection
```

## Notes

- Loads ratios from file
- Maintains ratio cache
- Handles missing files
- Memory-efficient
- Input validation
- Comprehensive error handling
- Dynamic override support
