# Load Checkpoint With Info

## Description

This node is similar to ComfyUI's standard checkpoint loader but includes an additional output that provides information about the loaded model. It loads Stable Diffusion checkpoints and extracts their components while maintaining compatibility with standard ComfyUI workflows.

## Inputs

### Required:
- **ckpt_name**: (`COMBO`) - Checkpoint file selection from the checkpoints folder
  - Tooltip: "The name of the checkpoint (model) to load."

## Outputs

- **model**: (`MODEL`) - The loaded Stable Diffusion model
- **clip**: (`CLIP`) - CLIP text encoder
- **vae**: (`VAE`) - VAE for image encoding/decoding
- **model_info**: (`STRING`) - Information about the loaded checkpoint
  - Format: "checkpoint name: {model_name}"

## Features

- Standard checkpoint loading functionality
- Automatic config detection
- Embedding directory support
- Additional model info output
- Extension-stripped model name
- Compatible with all ComfyUI nodes

## Example Usage

Basic Loading:
```python
ckpt_name: "v1-5-pruned.ckpt"
# Returns model components and info string:
# "checkpoint name: v1-5-pruned"
```

## Notes

- Functionally identical to ComfyUI's checkpoint loader
- Added model info output
- Uses ComfyUI's standard loading system
- Supports all checkpoint formats
- Automatic VAE extraction
- Automatic CLIP extraction
- Embedding directory integration 
