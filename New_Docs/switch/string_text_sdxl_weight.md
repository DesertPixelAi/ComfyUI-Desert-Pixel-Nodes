# String Text With SDXL Weight

## Description

This node takes a text input and applies an SDXL-style weight to it, formatting the output as "(text:weight)". It's useful for creating weighted prompts in SDXL workflows and supports both direct text input and list-to-string conversion.

## Inputs

### Required:
- **Widget_Input**: (`STRING`, multiline) - Input text to be weighted
- **weight**: (`FLOAT`, default: 1.0, range: -10.0 to 10.0, step: 0.1) - Weight value to apply to the text

## Outputs

- **TEXT**: (`STRING`) - Weighted text in SDXL format
  - Format: "(input_text:weight_value)"
  - Empty string if no input provided

## Features

- SDXL weight formatting
- List-to-string conversion
- Empty input handling
- Decimal precision
- Error reporting

## Example Usage

Basic Weighting:
```python
Widget_Input: "portrait photo"
weight: 1.2
# Returns: "(portrait photo:1.2)"
```

Empty Input:
```python
Widget_Input: ""
weight: 1.0
# Returns: ""
```

## Notes

- Automatically joins list inputs
- Trims whitespace
- Maintains SDXL syntax
- Error handling
- Memory-efficient
- Compatible with SDXL workflows
