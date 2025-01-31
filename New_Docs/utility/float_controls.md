# DP Draggable Floats System

## Description

A set of utility nodes providing easy-to-use float value controls. Each node can be customized through text files to modify min/max values, default settings, step size, and slider appearance. Available in single, double, and triple float variants.

## DP Draggable Floats 1

### Inputs
- **float_value**: (`FLOAT`) - Single float input with customizable range and appearance

### Outputs
- **float_value**: (`FLOAT`) - The input value passed through

## DP Draggable Floats 2

### Inputs
- **float_value1**: (`FLOAT`) - First float input
- **float_value2**: (`FLOAT`) - Second float input

### Outputs
- **float_value1**: (`FLOAT`) - First float value
- **float_value2**: (`FLOAT`) - Second float value

## DP Draggable Floats 3

### Inputs
- **float_value1**: (`FLOAT`) - First float input
- **float_value2**: (`FLOAT`) - Second float input
- **float_value3**: (`FLOAT`) - Third float input

### Outputs
- **float_value1**: (`FLOAT`) - First float value
- **float_value2**: (`FLOAT`) - Second float value
- **float_value3**: (`FLOAT`) - Third float value

## Customization

Each node reads settings from a text file in the `data/draggable_floats/` directory:
```python
min=0.00
max=1.00
default=1.00
step=0.01
slider=false
```

Settings:
- **min**: Minimum value (default: 0.00)
- **max**: Maximum value (default: 1.00)
- **default**: Default value (default: 1.00)
- **step**: Step size for value changes (default: 0.01)
- **slider**: Display as slider (true) or number input (false)

Configuration files:
- Single Float: `float_min_max_1_input.txt`
- Double Float: `float_min_max_2_input.txt`
- Triple Float: `float_min_max_3_input.txt`

## Features

- **Value Control**:
  - Customizable ranges
  - Adjustable step sizes
  - Default presets
  - Slider/number toggle

- **Processing**:
  - File-based configuration
  - Error handling
  - Default fallbacks
  - Memory-efficient

## Example Usage

Basic Float:
```python
# DP Draggable Floats 1
float_value: 0.5
# Returns: 0.5
```

Double Float:
```python
# DP Draggable Floats 2
float_value1: 0.3
float_value2: 0.7
# Returns: 0.3, 0.7
```

## Notes

- Reads settings from file
- Handles missing files
- Provides default values
- Memory-efficient
- Input validation
- Error handling
- Multiple display modes 
