# Load ControlNet Model With Name

## Description

This node is similar to ComfyUI's standard ControlNet loader but includes an additional output that provides information about the loaded model. It loads ControlNet models while maintaining compatibility with standard ComfyUI workflows.

## Inputs

### Required:
- **control_net_name**: (`COMBO`) - ControlNet model selection from the controlnet folder

## Outputs

- **control_net**: (`CONTROL_NET`) - The loaded ControlNet model
- **control_net_name**: (`STRING`) - Information about the loaded model
  - Format: "controlnet model: {model_name}"

## Features

- Standard ControlNet loading functionality
- Additional model info output
- Extension-stripped model name
- Compatible with all ComfyUI nodes
- Automatic path resolution

## Example Usage

Basic Loading:
```python
control_net_name: "canny.safetensors"
# Returns model and info string:
# "controlnet model: canny"
```

## Notes

- Functionally identical to ComfyUI's ControlNet loader
- Added model info output
- Uses ComfyUI's standard loading system
- Supports all ControlNet formats
- Automatic path resolution
- Memory-efficient loading
