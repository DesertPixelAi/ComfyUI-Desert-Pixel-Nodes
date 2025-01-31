# DP Condition Switch

## Description

This node allows switching between different pairs of conditions (positive/negative), making it easy to manage and select between multiple conditioning pairs in your workflow.

## Inputs

### Required:
- **selected_pair**: (`COMBO`) - Select which pair to use:
  - "Conditions 01"
  - "Conditions 02"
  - "Conditions 03"
  - "Conditions 04"
  - "Conditions 05"

### Optional:
- **condition_positive_01**: (`CONDITIONING`) - First positive condition pair
- **condition_negative_01**: (`CONDITIONING`) - First negative condition pair
- **condition_positive_02**: (`CONDITIONING`) - Second positive condition pair
- **condition_negative_02**: (`CONDITIONING`) - Second negative condition pair
- **condition_positive_03**: (`CONDITIONING`) - Third positive condition pair
- **condition_negative_03**: (`CONDITIONING`) - Third negative condition pair
- **condition_positive_04**: (`CONDITIONING`) - Fourth positive condition pair
- **condition_negative_04**: (`CONDITIONING`) - Fourth negative condition pair
- **condition_positive_05**: (`CONDITIONING`) - Fifth positive condition pair
- **condition_negative_05**: (`CONDITIONING`) - Fifth negative condition pair

## Outputs

- **condition_positive**: (`CONDITIONING`) - Selected positive condition
- **condition_negative**: (`CONDITIONING`) - Selected negative condition

## Features

- **Condition Management**:
  - Multiple pair support
  - Easy switching
  - Optional connections
  - Pair validation

- **Processing**:
  - Automatic pair selection
  - Empty condition handling
  - Error reporting
  - Connection validation

## Example Usage

Basic Switching:
```python
selected_pair: "Conditions 01"
condition_positive_01: <conditioning_A>
condition_negative_01: <conditioning_B>
# Returns: conditioning_A, conditioning_B
```

Different Pair:
```python
selected_pair: "Conditions 03"
condition_positive_03: <conditioning_C>
condition_negative_03: <conditioning_D>
# Returns: conditioning_C, conditioning_D
```

## Notes

- Handles unconnected inputs
- Provides warning messages
- Returns empty conditions as fallback
- Memory-efficient processing
- Comprehensive error handling
- Easy pair selection
- Maintains conditioning types 
