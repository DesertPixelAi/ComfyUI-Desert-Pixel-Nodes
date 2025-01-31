# DP Random Min/Max

## Description

This node generates random numbers within a specified range, providing both float and integer outputs with configurable step sizes. It generates two random float values and two random integer values in each execution.

## Inputs

### Required:
- **min**: (`FLOAT`, default: 0.0, range: -10000.0-10000.0) - Minimum value
- **max**: (`FLOAT`, default: 1.0, range: -10000.0-10000.0) - Maximum value
- **step**: (`COMBO`) - Step size options:
  - "int_1" - Integer steps of 1
  - "float_0.1" - Float steps of 0.1
  - "float_0.01" - Float steps of 0.01
  - "float_0.001" - Float steps of 0.001

## Outputs

- **random_float_1**: (`FLOAT`) - First random float value
- **random_float_2**: (`FLOAT`) - Second random float value
- **random_int_1**: (`INT`) - First random integer value
- **random_int_2**: (`INT`) - Second random integer value

## Features

- **Range Control**:
  - Wide value range
  - Multiple step sizes
  - Integer/float outputs
  - Dual value generation

- **Processing**:
  - Step-size enforcement
  - Range validation
  - Automatic rounding
  - Value clamping

## Example Usage

Decimal Values:
```python
min: 0.5
max: 1.5
step: "float_0.01"
# Outputs: 0.72, 1.13, 1, 1
```

Integer Range:
```python
min: 1
max: 10
step: "int_1"
# Outputs: 4.0, 7.0, 4, 7
```

Fine Control:
```python
min: 0.001
max: 0.01
step: "float_0.001"
# Outputs: 0.004, 0.007, 0, 0
```

## Notes

- Generates new values each execution
- Maintains step size accuracy
- Handles edge cases
- Memory-efficient processing
- Comprehensive error handling
- Range enforcement
- Step size validation
