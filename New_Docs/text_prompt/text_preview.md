# Text Preview

## Description

This node provides real-time text preview capabilities with automatic value formatting and display updates. It's particularly useful for monitoring node outputs, displaying model names, and previewing text transformations in your workflow.

## Inputs

### Optional:
- **any_input**: (`*`) - Accepts any input type for preview
- **display_text**: (`STRING`, multiline) - Custom text to display when no input is provided

### Hidden:
- **text**: (`STRING`) - Direct text input
- **unique_id**: Node identifier
- **extra_pnginfo**: Additional PNG metadata

## Outputs

- **STRING**: Formatted display text

## Features

- **Value Formatting**:
  - Numbers to strings
  - Boolean conversion
  - File path simplification
  - List handling
  - Model name extraction
  - Null value handling

- **Display Processing**:
  - Multi-line support
  - Automatic type conversion
  - Smart concatenation
  - Real-time updates

## Example Usage

Basic Text Display:
```python
any_input: "Hello World"
# Displays: "Hello World"
```

Model Name Display:
```python
any_input: <model_object>
# Displays: "model_name"
```

File Path Display:
```python
any_input: "path/to/model.safetensors"
# Displays: "model"
```

## Notes

- Real-time UI updates
- Multiple input types
- Automatic formatting
- Memory-efficient
- Error handling
- WebSocket integration
- Dynamic widget updates 
