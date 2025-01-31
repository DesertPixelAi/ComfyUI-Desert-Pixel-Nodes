# Prompt Token Compressor

## Description

This node intelligently compresses prompts to fit within token limits while preserving the most important semantic information. It uses a sophisticated scoring system to prioritize different prompt elements and supports multiple model tokenizers.

## Inputs

### Required:
- **target_tokens**: (`INT`, default: 77, range: 1-225) - Desired token count
- **model_type**: (`COMBO`) - Model-specific tokenization:
  - "sd1" - Stable Diffusion 1.x (77 tokens)
  - "sd2" - Stable Diffusion 2.x (77 tokens)
  - "sdxl" - Stable Diffusion XL (77 tokens)
  - "flux" - Flux model (225 tokens)
- **preservation_mode**: (`COMBO`) - Compression strategy:
  - "balanced" - Equal weight to all elements
  - "subject_focus" - Prioritize subject descriptions
  - "style_focus" - Prioritize style elements

### Optional:
- **prompt**: (`STRING`, multiline) - Input text to compress

## Outputs

- **compressed_prompt**: (`STRING`) - Compressed version of input
- **token_count**: (`INT`) - Final token count
- **compression_info**: (`STRING`) - Detailed compression statistics

## Features

- **Element Prioritization**:
  - Subject matter (1.0)
  - Artistic style (0.9)
  - Scene description (0.8)
  - Visual effects (0.7)
  - Composition (0.6)
  - Quality terms (0.9)
  - Color terms (0.8)
  - Lighting (0.8)
  - Emotion (0.85)

- **Smart Processing**:
  - Context-aware scoring
  - Weight preservation
  - Multi-model support
  - Phrase-level analysis
  - Token count validation

## Example Usage

Basic Compression:
```python
target_tokens: 77
model_type: "sd2"
prompt: "A detailed portrait of a person, cinematic lighting, dramatic atmosphere, high quality render"
# Returns compressed version within token limit
```

Focused Compression:
```python
target_tokens: 77
model_type: "sdxl"
preservation_mode: "subject_focus"
prompt: "A detailed cyberpunk cityscape with neon lights, flying cars, dramatic atmosphere, cinematic composition"
# Returns subject-focused compression
```

## Notes

- Multiple tokenizer support
- Intelligent phrase scoring
- Preserves weighted terms
- Model-specific limits
- Detailed compression info
- Fallback token estimation
- Comprehensive error handling
