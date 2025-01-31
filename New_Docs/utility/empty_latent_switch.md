# DP Image Empty Latent Switch System

## Description

This system consists of three interconnected nodes that manage latent switching and mode control for both SDXL and Flux models:
- **DP Switch Controller**: Central control node
- **DP Image Empty Latent Switch SDXL**: SDXL-specific latent switcher
- **DP Image Empty Latent Switch Flux**: Flux model latent switcher

When the Switch Controller is connected to either latent switch node, it overrides their individual input settings.

## DP Switch Controller

### Inputs

#### Required:
- **Mode_Settings**: (`COMBO`) - Primary operation mode:
  - "Txt2Image" - Generate from text
  - "Img2Img" - Generate from image
- **IPadapter_Mode**: (`COMBO`) - IP-Adapter control:
  - "IPadapter_OFF" - Standard model
  - "IPadapter_ON" - Use IP-Adapter model
- **ControlNet_mode**: (`COMBO`) - ControlNet integration:
  - "Controlnet_OFF" - No ControlNet
  - "Controlnet_ON" - Enable ControlNet

### Outputs
- **settings**: (`SWITCH_SETTINGS`) - Combined settings for latent switch nodes

## DP Image Empty Latent Switch SDXL/Flux

### Inputs

#### Required:
- **Mode_Settings**: (`COMBO`) - Same as controller (ignored if controller connected)
- **IPadapter_Mode**: (`COMBO`) - Same as controller (ignored if controller connected)
- **ControlNet_mode**: (`COMBO`) - Same as controller (ignored if controller connected)
- **width**: (`INT`, default: 1024, range: 64-8192) - Output width
- **height**: (`INT`, default: 1024, range: 64-8192) - Output height
- **denoise_strength_img2img**: (`FLOAT`, default: 1.0, range: 0.0-1.0) - Image strength for img2img

#### Optional:
- **vae**: (`VAE`) - VAE model
- **Image_Input**: (`IMAGE`) - Input image for img2img
- **Model**: (`MODEL`) - Base model
- **Model_Ip_Adapter**: (`MODEL`) - IP-Adapter model
- **switch_settings**: (`SWITCH_SETTINGS`) - Connection from controller

### Outputs
- **MODEL**: Selected model based on mode
- **LATENT**: Generated latent
- **denoise**: Denoising strength
- **CONTROLNET**: ControlNet condition (if enabled)

## Features

- **Mode Management**:
  - Centralized control
  - Multiple model support
  - Dynamic switching
  - Automatic override

- **Processing**:
  - Memory optimization
  - Cached latents
  - Pinned memory
  - Error handling

## Example Usage

Basic Controller Setup:
```python
# DP Switch Controller
Mode_Settings: "Txt2Image"
IPadapter_Mode: "IPadapter_OFF"
ControlNet_mode: "Controlnet_OFF"
# Connect output to latent switch nodes
```

SDXL Latent Switch:
```python
# Connect controller to override these settings
width: 1024
height: 1024
denoise_strength_img2img: 0.75
# Other connections as needed
```

## Notes

- Controller overrides node inputs when connected
- Maintains separate caches for efficiency
- Handles model selection automatically
- Comprehensive error handling
- Memory-efficient processing
- Automatic cache management
- Supports both SDXL and Flux models
