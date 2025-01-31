# Clean Prompt

## Description

This node provides comprehensive text cleaning for prompts, handling various formatting issues and standardizing punctuation. It's particularly useful for cleaning and normalizing prompt text while preserving special notation like weights.

## Inputs

### Required:
- **input_text**: (`STRING`, multiline) - Text to be cleaned

## Outputs

- **clean_text**: (`STRING`) - Cleaned and normalized text

## Features

- **Text Normalization**:
  - Preserves escaped parentheses \( \)
  - Standardizes newlines
  - Converts underscores to spaces
  - Normalizes punctuation

- **Weight Notation Handling**:
  - Preserves weight formats like (1.5) or (2,)
  - Protects weight notation during cleaning
  - Fixes spacing around weights

- **Punctuation Processing**:
  - Converts dots to commas
  - Removes multiple commas
  - Standardizes comma spacing
  - Removes single quotes
  - Fixes accidentally joined words

## Example Usage

Basic Cleaning:
```python
input_text: "photo.of_a.person..with weight(1.5),next_part"
# Returns: "photo, of a person, with weight(1.5), next part"
```

Weight Preservation:
```python
input_text: "subject(1.5), another_subject(2,)"
# Returns: "subject(1.5), another subject(2,)"
```

## Notes

- Preserves weight notations
- Maintains word boundaries
- Removes redundant spacing
- Fixes accidental word joins
- Standardizes comma usage
- Handles escaped characters
- Memory-efficient processing
