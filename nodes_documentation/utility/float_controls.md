# DP Float Controls (0-1)
<img src="https://github.com/user-attachments/assets/64a249c6-4c48-4dcf-a4ba-ddcb6e70736c" alt="DP_Float_0_1" style="float: left; margin-right: 10px;"/>

## Description

A set of utility nodes providing easy-to-use float value controls. Each node can be customized through text files to modify min/max values, default settings, step size, and slider appearance. Available in single, double, and triple float variants.

## Single Float (DP Float 0-1)

### Inputs
- `float_value`: Single float input with customizable range and appearance

### Outputs
- `float_value`: The input value passed through

## Double Float (DP 2 Floats 0-1)

### Inputs
- `float_value1`: First float input
- `float_value2`: Second float input

### Outputs
- `float_value1`: First float value
- `float_value2`: Second float value

## Triple Float (DP 3 Floats 0-1)

### Inputs
- `float_value1`: First float input
- `float_value2`: Second float input
- `float_value3`: Third float input

### Outputs
- `float_value1`: First float value
- `float_value2`: Second float value
- `float_value3`: Third float value

## Customization

Each node reads settings from a text file in the `data/zero_floats/` directory:
```
min=0.00
max=1.00
default=1.00
step=0.01
slider=false
```

- `min`: Minimum value (default: 0.00)
- `max`: Maximum value (default: 1.00)
- `default`: Default value (default: 1.00)
- `step`: Step size for value changes (default: 0.01)
- `slider`: Display as slider (true) or number input (false)

Configuration files:
- Single Float: `float_min_max_1_input.txt`
- Double Float: `float_min_max_2_input.txt`
- Triple Float: `float_min_max_3_input.txt`
