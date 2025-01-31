# DP Advanced Sampler

## Description

The Advanced Sampler node provides enhanced control over the sampling process with additional parameters and scheduling options. It extends the basic sampler functionality with features like dynamic scheduling, custom step patterns, advanced noise control, latent upscaling, and latent splitting capabilities.

## Inputs

### Required:
- **model**: (`MODEL`) - The model to use for sampling
- **vae**: (`VAE`) - VAE model for encoding/decoding images
- **seed**: (`INT`, default: 0, range: 0-18446744073709551615) - Random seed for generation
- **steps**: (`INT`, default: 20, range: 1-10000) - Number of sampling steps
- **cfg**: (`FLOAT`, default: 8.0, range: 0.0-100.0) - Classifier-free guidance scale
- **sampler_name**: (`COMBO`) - Sampling algorithm selection:
  - "euler"
  - "euler_ancestral"
  - "heun"
  - "dpm_2"
  - "dpm_2_ancestral"
  - "lms"
  - "dpm_fast"
  - "dpm_adaptive"
  - "dpmpp_2s_ancestral"
  - "dpmpp_sde"
  - "dpmpp_2m"
  - "ddim"
  - "uni_pc"
  - "uni_pc_bh2"
- **scheduler**: (`COMBO`) - Scheduler type:
  - "normal" - Standard scheduling
  - "karras" - Karras noise scheduling
  - "exponential" - Exponential scheduling
  - "sgm_uniform" - SGM uniform scheduling
  - "simple" - Simple linear scheduling
- **positive**: (`CONDITIONING`) - Positive conditioning
- **negative**: (`CONDITIONING`) - Negative conditioning
- **latent_image**: (`LATENT`) - Input latent image
- **denoise**: (`FLOAT`, default: 1.0, range: 0.0-1.0) - Denoising strength
- **enable_upscale**: (`BOOLEAN`, default: False) - Enable latent upscaling
- **two_step_upscale**: (`BOOLEAN`, default: False) - Use two-step upscaling process
- **scale_by**: (`FLOAT`, default: 1.5, range: 0.01-8.0) - Upscale factor
- **upscale_steps**: (`INT`, default: 10, range: 1-10000) - Steps for upscale sampling
- **upscale_cfg**: (`FLOAT`, default: 7.0, range: 0.0-100.0) - CFG for upscale sampling
- **upscale_sampler_name**: (`COMBO`) - Sampler for upscaling (same options as sampler_name)
- **upscale_scheduler**: (`COMBO`) - Scheduler for upscaling (same options as scheduler)
- **upscale_denoise**: (`FLOAT`, default: 0.5, range: 0.0-1.0) - Denoise strength for upscaling
- **enable_split**: (`BOOLEAN`, default: False) - Enable latent splitting
- **split_rows**: (`INT`, default: 2, range: 1-8) - Number of rows for splitting
- **split_columns**: (`INT`, default: 4, range: 1-8) - Number of columns for splitting
- **overlap_pixels**: (`INT`, default: 0, range: 0-128, step: 8) - Overlap between split sections

## Outputs
- **sampled_latent**: (`LATENT`) - The output latent from initial sampling
- **sampled_image**: (`IMAGE`) - The decoded image from initial sampling
- **upscaled_latent**: (`LATENT`) - The upscaled latent (if upscaling enabled)
- **upscaled_image**: (`IMAGE`) - The decoded upscaled image (if upscaling enabled)
- **sampler_info**: (`STRING`) - Detailed information about the sampling process

## Features

### Basic Sampling
- Configurable sampling parameters
- Multiple scheduler options
- Adjustable denoising strength

### Latent Upscaling
- Single-step or two-step upscaling process
- Configurable scale factor
- Independent sampling parameters for upscaling
- Uses bicubic interpolation for initial scaling

### Two-Step Upscaling
- Geometric progression scaling (sqrt of final scale per step)
- Slightly increased denoise in second pass (+0.05)
- Independent seed for each pass (seed+1, seed+2)
- Refined detail preservation

### Latent Splitting
- Grid-based splitting before upscaling
- Configurable overlap between sections
- Maintains consistent seed across splits
- Automatic reassembly after processing

## Example Usage
```python
# Basic sampling with upscaling
seed: 123456789
steps: 30
cfg: 7.5
sampler_name: "euler_ancestral"
scheduler: "karras"
denoise: 0.8
enable_upscale: True
scale_by: 2.0
upscale_denoise: 0.5

# With splitting enabled
enable_split: True
split_rows: 2
split_columns: 2
overlap_pixels: 64
```

## Notes

- Two-step upscaling provides better detail preservation
- Splitting is useful for processing large images
- Overlap helps prevent seams in split processing
- Memory usage increases with split count and upscale factor
- Processing time scales with upscale steps and split count 