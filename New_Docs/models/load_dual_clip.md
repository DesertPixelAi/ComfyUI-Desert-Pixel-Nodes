# Load Dual CLIP With Info

## Description

This node is similar to ComfyUI's standard Dual CLIP loader but includes an additional output that provides information about the loaded models. It loads two CLIP models for various model architectures while maintaining compatibility with standard ComfyUI workflows.

## Inputs

### Required:
- **clip_name1**: (`COMBO`) - First CLIP model selection from text_encoders folder
- **clip_name2**: (`COMBO`) - Second CLIP model selection from text_encoders folder
- **type**: (`COMBO`) - Model architecture type:
  - "sdxl" - Stable Diffusion XL
  - "sd3" - Stable Diffusion 3
  - "flux" - Flux architecture
  - "hunyuan_video" - Hunyuan Video model

### Optional:
- **device**: (`COMBO`, advanced) - Model loading device
  - "default" - Use default device
  - "cpu" - Force CPU loading

## Outputs

- **clip**: (`CLIP`) - The loaded dual CLIP model
- **model_info**: (`STRING`) - Information about the loaded models
  - Format:
    ```
    clip1: {clip1_name}
    clip2: {clip2_name}
    ```

## Features

- Standard dual CLIP loading functionality
- Additional model info output
- Extension-stripped model names
- Compatible with all ComfyUI nodes
- Embedding directory support

## Model Combinations

The node supports these CLIP combinations:
- SDXL: clip-l + clip-g
- SD3: clip-l + clip-g / clip-l + t5 / clip-g + t5
- Flux: clip-l + t5
- Hunyuan Video: custom combination

## Example Usage

SDXL Loading:
```python
clip_name1: "sd_xl_base_1.0_clip_l.safetensors"
clip_name2: "sd_xl_base_1.0_clip_g.safetensors"
type: "sdxl"
# Returns model and info string with both CLIP names
```

## Notes

- Functionally identical to ComfyUI's dual CLIP loader
- Added model info output
- Uses ComfyUI's standard loading system
- Supports all CLIP model formats
- Automatic path resolution
- Memory-efficient loading
- Optional CPU offloading 
