# ComfyUI custom nodes by DreamProphet
# DP Image or Empty Latent Switch Node implementation

import torch
from nodes import EmptyLatentImage, VAEEncode
from typing import Dict, Any, Tuple, Optional, Union

class DP_Image_Empty_Latent_Switch:
    _pinned_memory = {}  # Cache for pinned memory buffers
    _empty_latent_cache = {}  # Cache for empty latents
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "switch": (["empty_latent_image", "image_input_1", "image_input_2", "image_input_3", "image_input_4", "image_input_5"], 
                          {"default": "empty_latent_image"}),
                "img2img_strength": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "width": ("INT", {"default": 1024, "min": 64, "max": 8192}),
                "height": ("INT", {"default": 1024, "min": 64, "max": 8192}),
            },
            "optional": {
                "Image_Input_01": ("IMAGE",),
                "Image_Input_02": ("IMAGE",),
                "Image_Input_03": ("IMAGE",),
                "Image_Input_04": ("IMAGE",),
                "Image_Input_05": ("IMAGE",),
                "vae": ("VAE",),
            }
        }

    RETURN_TYPES = ("LATENT", "FLOAT", "FLOAT", "INT")
    RETURN_NAMES = ("LATENT", "img2img_strength", "denoise", "selected_switch")
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

    def switch(self, switch: str, img2img_strength: float, denoise: float, 
               width: int, height: int, 
               Image_Input_01: Optional[torch.Tensor] = None,
               Image_Input_02: Optional[torch.Tensor] = None,
               Image_Input_03: Optional[torch.Tensor] = None,
               Image_Input_04: Optional[torch.Tensor] = None,
               Image_Input_05: Optional[torch.Tensor] = None,
               vae: Optional[Any] = None) -> Tuple[Dict[str, torch.Tensor], float, float, int]:
        """Switch between empty latent and image inputs with optimizations."""
        
        # Apply optimizations
        self._optimize_torch_settings()

        # Direct mapping for switch values
        switch_number = {
            "empty_latent_image": 1,
            "image_input_1": 2,
            "image_input_2": 3,
            "image_input_3": 4,
            "image_input_4": 5,
            "image_input_5": 6
        }[switch]

        # Handle empty latent case
        if switch == "empty_latent_image":
            return (self._get_empty_latent(width, height), 0.0, denoise, switch_number)

        # Map inputs to their switch positions
        input_map = {
            "image_input_1": Image_Input_01,
            "image_input_2": Image_Input_02,
            "image_input_3": Image_Input_03,
            "image_input_4": Image_Input_04,
            "image_input_5": Image_Input_05
        }

        selected_image = input_map[switch]
        if selected_image is None:
            return (self._get_empty_latent(width, height), 0.0, denoise, switch_number)

        if vae is None:
            raise ValueError(f"VAE is required for image input {switch}")

        return (self._encode_image(selected_image, vae), img2img_strength, denoise, switch_number)

    @classmethod
    def cleanup_cache(cls):
        """Clear all caches to free memory."""
        cls._pinned_memory.clear()
        cls._empty_latent_cache.clear()

NODE_CLASS_MAPPINGS = {
    "DP_Image_Empty_Latent_Switch": DP_Image_Empty_Latent_Switch
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DP_Image_Empty_Latent_Switch": "DP Image Empty Latent Switch"
}