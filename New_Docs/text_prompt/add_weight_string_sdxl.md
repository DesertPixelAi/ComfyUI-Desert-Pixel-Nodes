# Add Weight To String SDXL

## Description

This node adds a weight value to a text string using SDXL prompt syntax. It formats the output as "(text:weight)" and handles empty inputs gracefully. This is particularly useful for creating weighted prompts in SDXL workflows.

## Inputs

### Required:
- **weight**: (`FLOAT`, default: 1.0, range: 0.0 to 10.0, step: 0.1) - Weight value to apply to the text

### Optional:
- **text**: (`STRING`, multiline) - Input text to be weighted

## Outputs

- **STRING**: The weighted text in SDXL format
  - Format: "(text:weight)"
  - Returns empty string if no text provided
  - Returns unmodified text if weight is 1.0

## Features

- SDXL-compatible weight formatting
- Empty input handling
- Default weight bypass
- Decimal precision
- Error handling

## Example Usage

Basic Weighting:
```python
text: "portrait photo"
weight: 1.2
# Returns: "(portrait photo:1.2)"
```

Default Weight:
```python
text: "portrait photo"
weight: 1.0
# Returns: "portrait photo"
```

Empty Input:
```python
text: ""
weight: 1.5
# Returns: ""
```

## Notes

- Preserves original text when weight is 1.0
- Two decimal place precision
- Memory-efficient processing
- Compatible with SDXL workflows
- Automatic input validation
