import torch
from nodes import EmptyLatentImage, VAEEncode
from typing import Dict, Any, Tuple, Optional, Union

class DP_Image_Empty_Latent_Switch_SDXL:
    _pinned_memory = {}  # Class level cache
    _empty_latent_cache = {}  # Class level cache

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Mode_Settings": (["Txt2Image", "Img2Img"], {"default": "Txt2Image"}),
                "IPadapter_Mode": (["IPadapter_OFF", "IPadapter_ON"], {"default": "IPadapter_OFF"}),
                "ControlNet_mode": (["Controlnet_OFF", "Controlnet_ON"], {"default": "Controlnet_OFF"}),
                "width": ("INT", {"default": 1024, "min": 64, "max": 8192}),
                "height": ("INT", {"default": 1024, "min": 64, "max": 8192}),
                "denoise_strength_img2img": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
            "optional": {
                "vae": ("VAE",),
                "Image_Input": ("IMAGE",),
                "Model": ("MODEL",),
                "Model_Ip_Adapter": ("MODEL",),
                "condition_positive": ("CONDITIONING",),
                "condition_negative": ("CONDITIONING",),
                "condition_positive_cn": ("CONDITIONING",),
                "condition_negative_cn": ("CONDITIONING",),
                "switch_settings": ("SWITCH_SETTINGS",),
            }
        }

    RETURN_TYPES = ("MODEL", "CONDITIONING", "CONDITIONING", "LATENT", "FLOAT")
    RETURN_NAMES = ("MODEL", "condition_positive", "condition_negative", "LATENT", "denoise")
    FUNCTION = "switch"
    CATEGORY = "DP/utils"

    def _get_empty_latent(self, width: int, height: int, batch_size: int = 1):
        """Get cached empty latent or create new one."""
        from nodes import EmptyLatentImage
        cache_key = f"{width}x{height}x{batch_size}"
        if cache_key not in self._empty_latent_cache:
            self._empty_latent_cache[cache_key] = EmptyLatentImage().generate(width, height, batch_size)[0]
        return self._empty_latent_cache[cache_key]

    def _encode_image(self, image, vae):
        """Encode image to latent."""
        try:
            if image.device.type == "cpu":
                batch_key = f"{image.shape}_{image.dtype}"
                if batch_key not in self._pinned_memory:
                    self._pinned_memory[batch_key] = torch.zeros_like(image, pin_memory=True)
                self._pinned_memory[batch_key].copy_(image)
                image = self._pinned_memory[batch_key].cuda(non_blocking=True)

            with torch.cuda.amp.autocast(enabled=True):
                latent = vae.encode(image[:, :, :, :3])
            return {"samples": latent}

        except Exception as e:
            print(f"Error during image encoding: {str(e)}")
            from nodes import VAEEncode
            return VAEEncode().encode(vae, image)[0]

    def switch(self, Mode_Settings, IPadapter_Mode, ControlNet_mode,
               width, height, denoise_strength_img2img, **kwargs):
        """Handle model selection and latent generation"""
        
        # Get settings from controller if available
        if "switch_settings" in kwargs:
            Mode_Settings, IPadapter_Mode, ControlNet_mode = kwargs["switch_settings"]
        
        # Convert mode_setting string to integer (keep this for internal logic)
        mode_map = {
            "Txt2Image": 0,
            "Img2Img": 1
        }
        mode_setting_int = mode_map[Mode_Settings]
        
        # Handle model selection based on IPadapter_Mode
        selected_model = kwargs.get("Model")
        if IPadapter_Mode == "IPadapter_ON":
            selected_model = kwargs.get("Model_Ip_Adapter", selected_model)
        
        if selected_model is None:
            raise ValueError("No valid model found. Please connect a model.")

        # Create empty latent
        empty_latent = self._get_empty_latent(width, height)

        # Get conditions based on ControlNet mode
        condition_positive = None
        condition_negative = None
        
        if ControlNet_mode == "Controlnet_ON":
            condition_positive = kwargs.get("condition_positive_cn")
            condition_negative = kwargs.get("condition_negative_cn")
        else:
            condition_positive = kwargs.get("condition_positive")
            condition_negative = kwargs.get("condition_negative")

        # Handle empty latent case (txt2img mode)
        if mode_setting_int == 0:
            return (selected_model,
                    condition_positive if condition_positive is not None else [],
                    condition_negative if condition_negative is not None else [],
                    empty_latent,
                    1.0)

        # Handle image input
        selected_image = kwargs.get("Image_Input")
        if selected_image is None:
            return (selected_model,
                    condition_positive if condition_positive is not None else [],
                    condition_negative if condition_negative is not None else [],
                    empty_latent,
                    0.0)

        vae = kwargs.get("vae")
        if vae is None:
            raise ValueError("VAE is required for image input")

        # Encode image
        latent = self._encode_image(selected_image, vae)
        if latent is None or 'samples' not in latent:
            return (selected_model,
                    condition_positive if condition_positive is not None else [],
                    condition_negative if condition_negative is not None else [],
                    empty_latent,
                    0.0)

        return (selected_model,
                condition_positive if condition_positive is not None else [],
                condition_negative if condition_negative is not None else [],
                latent,
                denoise_strength_img2img)

