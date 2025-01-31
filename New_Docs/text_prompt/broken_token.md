# Broken Token

## Description

This node analyzes and splits Flux prompts based on user-defined token counts. It's particularly useful for managing long prompts that need to be split into multiple parts while maintaining token limits, with a focus on Flux model compatibility.

## Inputs

### Required:
- **max_tokens_part_1**: (`INT`, default: 77, range: 0-2000) - Maximum token count for first part
- **max_tokens_part_2**: (`INT`, default: 0, range: 0-2000) - Maximum token count for second part

### Optional:
- **prompt**: (`STRING`, multiline) - Input text to be analyzed and split

## Outputs

- **total_tokens**: (`INT`) - Total number of tokens in the input prompt
- **info**: (`STRING`) - Detailed analysis information
- **Text part 1**: (`STRING`) - First part of split text
- **Text part 2**: (`STRING`) - Second part of split text
- **Text part 3**: (`STRING`) - Remaining text

## Features

- Token count analysis
- Multi-part text splitting
- Automatic text cleaning:
  - Comma spacing normalization
  - Trailing comma removal
  - Multiple space reduction
  - Whitespace trimming

## Example Usage

Basic Analysis:
```python
max_tokens_part_1: 77
max_tokens_part_2: 50
prompt: "A long prompt that needs to be split into multiple parts..."
# Returns:
# - Total token count
# - Analysis info
# - Three text parts based on token limits
```

Empty Input:
```python
prompt: None
# Returns: (0, "", "", "", "")
```

## Notes

- Flux model compatibility
- Intelligent text splitting
- Token count validation
- Clean text formatting
- Detailed analysis output
- Error handling
- Memory-efficient processing
