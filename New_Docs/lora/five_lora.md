# DP Five Lora

## Description

The Five LoRA node enables loading up to five LoRA models simultaneously with precise strength control. It features a separate strength controller node for individual LoRA weight adjustments and includes memory optimizations for efficient processing.

## Inputs

### Required:
- **model**: (`MODEL`) - Base model to apply LoRAs to
- **clip**: (`CLIP`) - CLIP model for text encoding
- **loader_state**: (`COMBO`) - Enable/disable LoRA loading
  - "ON" - Process LoRAs
  - "OFF" - Bypass LoRA loading
- **Lora_01**: (`COMBO`) - First LoRA model selection

### Optional:
- **Lora_02** to **Lora_05**: (`COMBO`) - Additional LoRA model selections
- **strength_control**: (`LORA_STRENGTHS`) - Connection to DP_Lora_Strength_Controller

## Outputs

- **model**: (`MODEL`) - Model with applied LoRAs
- **clip**: (`CLIP`) - Updated CLIP model
- **lora_info**: (`STRING`) - Information about applied LoRAs and their strengths

## Strength Controller

The node requires a DP_Lora_Strength_Controller connection, which provides:

- Individual strength values (0.0-3.0) for each LoRA
- Fine control over model influence
- Independent adjustment for all five LoRA slots
- Precise 0.01 step increments

## Features

- **Optimization**:
  - Memory-efficient processing
  - GPU optimization
  - Batch LoRA loading
  - Weight caching
  - CUDA optimizations

- **Processing**:
  - Automatic weight preloading
  - Efficient batch operations
  - Memory management
  - Detailed strength reporting

## Example Usage

Basic Setup with Controller:
```python
# Main Node
loader_state: "ON"
Lora_01: "style_lora"
Lora_02: "detail_lora"

# Strength Controller
lora_01_strength: 1.0
lora_02_strength: 0.8
```

## Notes

- Requires DP_Lora_Strength_Controller
- Maximum 5 simultaneous LoRAs
- Automatic memory management
- GPU-accelerated processing
- Efficient batch operations
- Detailed strength reporting
- Automatic cache clearing
