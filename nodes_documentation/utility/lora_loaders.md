# DP Five LoRA Loaders

## Description

The DP Five LoRA Loaders package provides two specialized nodes for managing multiple LoRA models in ComfyUI:
1. A standard loader that applies up to five LoRA models with fixed strength values
2. A random loader that applies LoRA models with randomized strength values within specified ranges

## Standard Loader (DP_Five_Lora)
<img src="https://github.com/user-attachments/assets/7de97607-c5cc-4186-a9c0-250ee55548b4" alt="DP_Five_Lora" style="float: left; margin-right: 10px;"/>

### Inputs

**Required:**
- `model`: The base model to apply LoRAs to
- `clip`: The CLIP model
- `loader_state`: Toggle between "ON" and "OFF" to enable/disable LoRA application
- `Lora_01` to `Lora_05`: LoRA model selection (includes 'None' option) × 5
- `Lora_01_Strength` to `Lora_05_Strength`: Strength value for each LoRA (0.0 to 3.0) × 5

### Outputs

- `model`: The modified model with applied LoRAs
- `clip`: The modified CLIP model
- `lora_info`: A string containing information about applied LoRAs and their strengths

## Random Loader (DP_Five_Lora_Random)
<img src="https://github.com/user-attachments/assets/1a0fcc29-de16-4efc-bc96-f3d51e94352a" alt="DP_Five_Lora_Random" style="float: left; margin-right: 10px;"/>

### Inputs

**Required:**
- All standard loader required inputs
- `Lora_01` to `Lora_05`: LoRA model selection × 5
- `Lora_01_Strength` to `Lora_05_Strength`: Base strength values × 5
- `Random_Min` to `Random_Min_5`: Minimum strength values × 5
- `Random_Max` to `Random_Max_5`: Maximum strength values × 5

### Outputs

Same as standard loader, but strength values will be randomized within specified ranges each time the node runs.

## Notes

- Both nodes allow up to 5 simultaneous LoRA models
- Strength values range from 0.0 to 3.0
- Setting strength to 0.0 or selecting "None" will skip that LoRA
- The random loader generates new strength values within the specified ranges on each run
- Random strengths are rounded to 2 decimal places
