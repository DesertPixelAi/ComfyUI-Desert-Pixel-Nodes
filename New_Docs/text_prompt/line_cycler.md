# Line Cycler

## Description

This node cycles through lines of text in various modes, allowing sequential, reverse, random, or fixed selection of lines from a multi-line input. It provides real-time UI updates and maintains state between executions.

## Inputs

### Required:
- **Text**: (`STRING`, multiline) - Multi-line text input to cycle through
- **Cycler_Mode**: (`COMBO`) - Operation mode:
  - "increment" - Move to next line
  - "decrement" - Move to previous line
  - "randomize" - Select random line
  - "fixed" - Use specified line index
- **Line_Index**: (`INT`, default: 0) - Line selection for fixed mode

## Outputs

- **TEXT**: (`STRING`) - Selected line of text

## Features

- **Operation Modes**:
  - Sequential cycling
  - Reverse cycling
  - Random selection
  - Fixed index selection

- **Text Processing**:
  - Empty line filtering
  - Line trimming
  - Index validation
  - State persistence

- **UI Integration**:
  - Real-time index updates
  - Visual feedback
  - Error reporting

## Example Usage

Sequential Cycling:
```python
Text: """line 1
line 2
line 3"""
Cycler_Mode: "increment"
# Cycles through lines sequentially
```

Fixed Selection:
```python
Text: """line 1
line 2
line 3"""
Cycler_Mode: "fixed"
Line_Index: 1
# Returns: "line 2"
```

## Notes

- Maintains cycling state
- Handles empty inputs
- Automatic index wrapping
- Memory-efficient processing
- Real-time UI updates
- Error handling
- WebSocket integration
