# Load UNET With Info

## Description

This node is similar to ComfyUI's standard UNET loader but includes an additional output that provides information about the loaded model. It loads UNET models while maintaining compatibility with standard ComfyUI workflows.

## Inputs

### Required:
- **unet_name**: (`COMBO`) - UNET model selection from diffusion_models folder
- **weight_dtype**: (`COMBO`) - Model precision format:
  - "default" - Standard precision
  - "fp8_e4m3fn" - 8-bit precision (4 exponent, 3 mantissa)
  - "fp8_e4m3fn_fast" - 8-bit precision with optimizations
  - "fp8_e5m2" - 8-bit precision (5 exponent, 2 mantissa)

## Outputs

- **model**: (`MODEL`) - The loaded UNET model
- **model_info**: (`STRING`) - Information about the loaded model
  - Format: "unet name: {model_name}"

## Features

- Standard UNET loading functionality
- Additional model info output
- Extension-stripped model name
- Compatible with all ComfyUI nodes
- Multiple precision options
- Memory optimization settings

## Example Usage

Basic Loading:
```python
unet_name: "sd_xl_base_1.0.safetensors"
weight_dtype: "default"
# Returns model and info string:
# "unet name: sd_xl_base_1.0"
```

Memory-Optimized Loading:
```python
unet_name: "sd_xl_base_1.0.safetensors"
weight_dtype: "fp8_e4m3fn_fast"
# Loads model in 8-bit precision with optimizations
```

## Notes

- Functionally identical to ComfyUI's UNET loader
- Added model info output
- Uses ComfyUI's standard loading system
- Supports all UNET formats
- Multiple precision options
- Memory-efficient loading options
- Automatic path resolution 
