# DP Image Empty Latent Switch
<img src="https://github.com/user-attachments/assets/04c21510-a1d2-41d6-901c-ad70dd4f8ec6" alt="DP_Image_Empty_Latent_Switch" style="float: left; margin-right: 10px;"/>

## Description

A utility node that switches between empty latent (for txt2img) and up to 5 input images (for img2img). When in empty latent mode, it automatically sets img2img_strength to 0 and denoise to 1, ensuring proper settings for text-to-image generation.

## Inputs

**Required:**
- `switch`: Selection between empty_latent_image or image_input_1 through image_input_5
- `img2img_strength`: Image-to-image strength (0.0 to 1.0)
- `denoise`: Denoising strength (0.0 to 1.0)
- `width`: Width of the output latent (64 to 8192)
- `height`: Height of the output latent (64 to 8192)

**Optional:**
- `Image_Input_01` to `Image_Input_05`: Image inputs × 5
- `vae`: VAE model for encoding images

## Outputs

- `LATENT`: Output latent for generation
- `img2img_strength`: Modified strength value (forced to 0 in empty latent mode)
- `denoise`: Modified denoise value (forced to 1 in empty latent mode)
- `selected_switch`: Numerical value indicating selected mode (1-6)

## Notes

- When `switch` is set to "empty_latent_image":
  - `img2img_strength` output is forced to 0
  - `denoise` output is forced to 1
  - Creates empty latent of specified width/height
- When `switch` is set to any image input:
  - Uses provided img2img_strength and denoise values
  - Requires VAE for image encoding
  - Falls back to empty latent if image/VAE missing
