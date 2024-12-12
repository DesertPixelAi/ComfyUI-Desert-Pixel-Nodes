# DP Random Min/Max
<img src="https://github.com/user-attachments/assets/99bb875f-3d9b-462c-b781-0c179077af6c" alt="DP_Random_MinMax" style="float: left; margin-right: 10px;"/>

## Description

A utility node for generating random numbers within a specified range. Provides both float and integer outputs with configurable step sizes. Generates two random float values and two random integer values in each execution.

## Inputs

- `min`: Minimum value (-10000.0 to 10000.0)
- `max`: Maximum value (-10000.0 to 10000.0)
- `step`: Step size options:
  - `int_1`: Integer steps of 1
  - `float_0.1`: Float steps of 0.1
  - `float_0.01`: Float steps of 0.01
  - `float_0.001`: Float steps of 0.001

## Outputs

- `random_float_1`: First random float value
- `random_float_2`: Second random float value
- `random_int_1`: First random integer value
- `random_int_2`: Second random integer value

## Example Usage

For Decimal Values:
```
min: 0.5
max: 1.5
step: float_0.01
→ Outputs numbers like: 0.72, 1.13, 1, 1
```

For Integer Range:
```
min: 1
max: 10
step: int_1
→ Outputs numbers like: 4.0, 7.0, 4, 7
```

For Fine Control:
```
min: 0.001
max: 0.01
step: float_0.001
→ Outputs numbers like: 0.004, 0.007, 0, 0
```

Note: Node regenerates new random values on every execution.
