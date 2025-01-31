# DP Five Lora Random

## Description

The Five LoRA Random node enables loading up to five LoRA models with randomized strength values. It features a separate strength controller node for precise control over the randomization ranges. The node includes memory optimizations and efficient batch processing for improved performance.

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
- **strength_control**: (`LORA_RANDOM_STRENGTHS`) - Connection to DP_Lora_Random_Strength_Controller

## Outputs

- **model**: (`MODEL`) - Model with applied LoRAs
- **clip**: (`CLIP`) - Updated CLIP model
- **lora_info**: (`STRING`) - Information about applied LoRAs and their strengths

## Strength Controller

The node requires a DP_Lora_Random_Strength_Controller connection, which provides:

- Per-LoRA base strength (0.0-3.0)
- Minimum random multiplier (0.0-3.0)
- Maximum random multiplier (0.0-3.0)
- Independent control for all five LoRA slots

## Features

- **Randomization**:
  - Controllable random ranges
  - Per-LoRA strength settings
  - Min/max value validation
  - Automatic strength calculation

- **Optimization**:
  - Memory-efficient processing
  - GPU optimization
  - Batch LoRA loading
  - Weight caching
  - CUDA optimizations

## Example Usage

Basic Setup with Controller:
```python
# Main Node
loader_state: "ON"
Lora_01: "style_lora"
Lora_02: "detail_lora"

# Strength Controller
lora_01_strength: 1.0
lora_01_min: 0.5
lora_01_max: 1.0

lora_02_strength: 0.8
lora_02_min: 0.3
lora_02_max: 0.7
```

## Notes

- Requires DP_Lora_Random_Strength_Controller
- Maximum 5 simultaneous LoRAs
- Automatic memory management
- GPU-accelerated processing
- Efficient batch operations
- Detailed strength reporting
- Automatic cache clearing 
