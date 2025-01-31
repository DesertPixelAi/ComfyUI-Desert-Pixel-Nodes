# DP Clean Prompt Travel

## Description

The Clean Prompt Travel node is designed to clean and format text strings specifically for travel-related prompts. It removes special characters and formatting symbols that might interfere with prompt processing, making the text more suitable for use in travel-related image generation workflows.

## Inputs

### Required:
- **input_text**: (`STRING`, multiline) - The text to be cleaned and formatted

## Outputs
- **clean_text**: (`STRING`) - The cleaned and formatted text output

## Features

### Text Cleaning Operations
- Removes special characters: `( ) / \ | ^ * { } [ ]`
- Replaces underscores with spaces
- Preserves alphanumeric characters and basic punctuation

## Example Usage
```python
# Input text
input_text: "New_York_City (USA) / Manhattan [skyline] {sunset}"

# Output
clean_text: "New York City USA  Manhattan skyline sunset"
```

## Notes

- Maintains readability while removing problematic characters
- Ideal for cleaning location names and travel descriptions
- Preserves spaces between words
- Memory-efficient processing
- Compatible with any text input
- Useful for standardizing travel-related prompts 