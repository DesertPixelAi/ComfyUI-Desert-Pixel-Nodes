# ComfyUI custom nodes by DreamProphet
# DP Image or Empty Latent Switch Node implementation

import torch
from nodes import EmptyLatentImage, VAEEncode
from typing import Dict, Any, Tuple, Optional, Union
from server import PromptServer


class DP_Image_Empty_Latent_Switch_Flux:
    _pinned_memory = {}  # Cache for pinned memory buffers
    _empty_latent_cache = {}  # Cache for empty latents
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Mode_Settings": (["Txt2Image", "Img2Img"], {"default": "Txt2Image"}),
                "IPadapter_Mode": (["IPadapter_OFF", "IPadapter_ON"], {"default": "IPadapter_OFF"}),
                "ControlNet_mode": (["Controlnet_OFF", "Controlnet_ON"], {"default": "Controlnet_OFF"}),
                "img2img_strength": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "width": ("INT", {"default": 1024, "min": 64, "max": 8192}),
                "height": ("INT", {"default": 1024, "min": 64, "max": 8192}),
            },
            "optional": {
                "vae": ("VAE",),
                "Image_Input": ("IMAGE",),
                "Model": ("MODEL",),
                "Model_Ip_Adapter": ("MODEL",),
                "controlnet_condition": ("ControlNetCondition",),
                "switch_settings": ("SWITCH_SETTINGS",),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID"
            }
        }

    RETURN_TYPES = ("MODEL", "LATENT", "FLOAT", "ControlNetCondition")
    RETURN_NAMES = ("MODEL", "LATENT", "img2img_strength", "CONTROLNET")
    FUNCTION = "switch"
    CATEGORY = "DP/utils"

    @staticmethod
    def _optimize_torch_settings():
        """Apply various PyTorch optimizations."""
        if torch.cuda.is_available():
            torch.backends.cuda.matmul.allow_tf32 = True
            torch.backends.cudnn.allow_tf32 = True
            torch.backends.cudnn.benchmark = True
            torch.backends.cudnn.deterministic = False

    def _get_empty_latent(self, width: int, height: int, batch_size: int = 1) -> Dict[str, torch.Tensor]:
        """Get cached empty latent or create new one."""
        cache_key = f"{width}x{height}x{batch_size}"
        if cache_key not in self._empty_latent_cache:
            latent = EmptyLatentImage().generate(width, height, batch_size)[0]
            self._empty_latent_cache[cache_key] = latent
        return self._empty_latent_cache[cache_key]

    def _encode_image(self, image: torch.Tensor, vae: Any) -> Dict[str, torch.Tensor]:
        """Encode image to latent with optimizations."""
        try:
            # Use pinned memory for CPU inputs
            if image.device.type == "cpu":
                batch_key = f"{image.shape}_{image.dtype}"
                if batch_key not in self._pinned_memory:
                    self._pinned_memory[batch_key] = torch.zeros_like(
                        image, 
                        pin_memory=True
                    )
                self._pinned_memory[batch_key].copy_(image)
                image = self._pinned_memory[batch_key].cuda(non_blocking=True)

            # Use mixed precision encoding
            with torch.cuda.amp.autocast(enabled=True):
                latent = vae.encode(image[:, :, :, :3])
            return {"samples": latent}

        except Exception as e:
            print(f"Error during image encoding: {str(e)}")
            return VAEEncode().encode(vae, image)[0]

    def switch(self, Mode_Settings, IPadapter_Mode, ControlNet_mode, img2img_strength,
               width, height, **kwargs):
        
        # Get settings from controller if available
        if "switch_settings" in kwargs:
            Mode_Settings, IPadapter_Mode, ControlNet_mode = kwargs["switch_settings"]
        
        self._optimize_torch_settings()

        # Convert Mode_Settings string to integer (keep this for internal logic)
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

        # Handle ControlNet mode
        controlnet_output = None if ControlNet_mode == "Controlnet_OFF" else kwargs.get("controlnet_condition")

        # Create empty latent
        empty_latent = self._get_empty_latent(width, height)

        # Handle empty latent case
        if mode_setting_int == 0:
            return (selected_model, empty_latent, 0.0, controlnet_output)

        # Handle image input
        selected_image = kwargs.get("Image_Input")
        if selected_image is None:
            return (selected_model, empty_latent, 0.0, controlnet_output)

        vae = kwargs.get("vae")
        if vae is None:
            raise ValueError("VAE is required for image input")

        # Encode image
        latent = self._encode_image(selected_image, vae)
        if latent is None or 'samples' not in latent:
            return (selected_model, empty_latent, 0.0, controlnet_output)

        return (selected_model, latent, img2img_strength, controlnet_output)

    @classmethod
    def cleanup_cache(cls):
        """Clear all caches to free memory."""
        cls._pinned_memory.clear()
        cls._empty_latent_cache.clear()

