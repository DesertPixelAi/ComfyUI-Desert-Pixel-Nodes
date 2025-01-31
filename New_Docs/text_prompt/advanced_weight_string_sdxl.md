# Advanced Weight String SDXL

## Description

This node provides advanced weight control for SDXL prompts with multiple syntax options. It can format weights either numerically "(text:1.2)" or using plus/minus symbols "(text)++", making it versatile for different SDXL prompt styles.

## Inputs

### Required:
- **mode**: (`COMBO`) - Weight format style:
  - "NUMERIC" - Uses decimal format (text:1.2)
  - "PLUS/MINUS" - Uses symbols (text)++ or (text)--
- **weight**: (`FLOAT`, default: 1.0, range: 0.0 to 2.0, step: 0.1) - Weight value to apply
- **symbol_count**: (`INT`, default: 1, range: 1-3, step: 1) - Number of +/- symbols to use in PLUS/MINUS mode

### Optional:
- **text**: (`STRING`, multiline) - Input text to be weighted

## Outputs

- **STRING**: The weighted text in selected format
  - NUMERIC format: "(text:weight)"
  - PLUS/MINUS format: "(text)++" or "(text)--"
  - Returns empty string if no text provided
  - Returns unmodified text if weight is 1.0

## Features

- Multiple weight syntax options
- Configurable symbol count
- Empty input handling
- Default weight bypass
- Decimal precision
- Error handling

## Example Usage

Numeric Mode:
```python
mode: "NUMERIC"
text: "portrait photo"
weight: 1.2
# Returns: "(portrait photo:1.2)"
```

Plus/Minus Mode:
```python
mode: "PLUS/MINUS"
text: "portrait photo"
weight: 1.5
symbol_count: 2
# Returns: "(portrait photo)++"
```

Default Weight:
```python
text: "portrait photo"
weight: 1.0
# Returns: "portrait photo"
```

## Notes

- Preserves original text when weight is 1.0
- Two decimal place precision in numeric mode
- Supports up to triple +/- symbols
- Memory-efficient processing
- Compatible with all SDXL workflows
- Automatic input validation
