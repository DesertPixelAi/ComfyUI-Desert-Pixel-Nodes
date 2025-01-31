# 3/5/10 String Switch Or Connect

## Description

These nodes allow switching between multiple strings or combining them in various ways. Available in three variants for 3, 5, or 10 strings, they provide flexible text selection and combination capabilities.

## Inputs

### Required:
- **mode**: (`COMBO`) - Operation mode:
  - "Switch" - Select single string
  - "Connected" - Join with spaces
  - "Connected with comma" - Join with commas
  - "Connected with line break" - Join with \n
  - "Connected with line break+" - Join with \n\n
- **index**: (`INT`, default: 1) - Selected string in Switch mode
  - 3 Strings: range 1-3
  - 5 Strings: range 1-5
  - 10 Strings: range 1-10

### Optional:
- **String_01** to **String_XX**: (`STRING`, multiline) - Input strings (XX depends on variant)

## Outputs

- **TEXT**: (`STRING`) - Selected/combined text
- **CURRENT_INDEX**: (`INT`) - Current selection index

## Features

- **Operation Modes**:
  - Single string selection
  - Space-separated joining
  - Comma-separated joining
  - Line break joining
  - Double line break joining

- **Text Processing**:
  - Empty string filtering
  - List conversion
  - Whitespace trimming
  - Order preservation

## Example Usage

Switch Mode:
```python
mode: "Switch"
index: 2
String_02: "Selected text"
# Returns: "Selected text"
```

Connected Mode:
```python
mode: "Connected with comma"
String_01: "First"
String_02: "Second"
# Returns: "First, Second"
```

## Notes

- Handles empty strings
- Preserves input order
- Automatic list joining
- Multiple joining options
- Connection validation
- Error reporting
- Memory-efficient processing
