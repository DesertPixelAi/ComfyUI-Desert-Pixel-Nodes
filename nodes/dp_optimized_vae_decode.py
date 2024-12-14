import torch
import math
from typing import Tuple, Dict, Any

class DP_VAE_Decode_Optimized:
    _pinned_memory = {}  # Cache for pinned memory buffers
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "samples": ("LATENT", {"tooltip": "The latent to be decoded."}),
                "vae": ("VAE", {"tooltip": "The VAE model used for decoding the latent."})
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "decode"
    CATEGORY = "DP/optimized"

    def _decode_tiled(self, vae: Any, samples: torch.Tensor, tile_size: int = 512) -> torch.Tensor:
        """Decode latents using tiling strategy."""
        output_device = samples["samples"].device
        bs, ch, h, w = samples["samples"].shape
        target_h, target_w = h * 8, w * 8
        
        num_tiles_h = math.ceil(target_h / tile_size)
        num_tiles_w = math.ceil(target_w / tile_size)
        
        output = torch.zeros((bs, 3, target_h, target_w), device=output_device)
        
        for h_idx in range(num_tiles_h):
            for w_idx in range(num_tiles_w):
                h_start = h_idx * (tile_size // 8)
                w_start = w_idx * (tile_size // 8)
                h_end = min((h_idx + 1) * (tile_size // 8), h)
                w_end = min((w_idx + 1) * (tile_size // 8), w)
                
                tile_latent = {
                    "samples": samples["samples"][:, :, h_start:h_end, w_start:w_end].clone()
                }
                
                with torch.cuda.amp.autocast(enabled=True):
                    tile_decoded = vae.decode(tile_latent["samples"])
                
                out_h_start = h_idx * tile_size
                out_w_start = w_idx * tile_size
                out_h_end = min((h_idx + 1) * tile_size, target_h)
                out_w_end = min((w_idx + 1) * tile_size, target_w)
                
                output[:, :, out_h_start:out_h_end, out_w_start:out_w_end] = \
                    tile_decoded[:, :, :(out_h_end - out_h_start), :(out_w_end - out_w_start)]
                
        torch.cuda.empty_cache()  # Clear cache before large operation
        
        if hasattr(vae, 'enable_gradient_checkpointing'):
            vae.enable_gradient_checkpointing()
        
        return output

    def decode(self, vae: Any, samples: Dict[str, torch.Tensor]) -> Tuple[torch.Tensor]:
        """Decode latents to images with optimizations."""
        try:
            # Only use pinned memory if input is on CPU
            if samples["samples"].device.type == "cpu":
                batch_key = f"{samples['samples'].shape}_{samples['samples'].dtype}"
                if batch_key not in self._pinned_memory:
                    self._pinned_memory[batch_key] = torch.zeros_like(
                        samples["samples"], 
                        pin_memory=True
                    )
                self._pinned_memory[batch_key].copy_(samples["samples"])
                samples = {"samples": self._pinned_memory[batch_key].cuda(non_blocking=True)}
            
            # Always apply optimizations
            if torch.cuda.is_available():
                torch.backends.cuda.matmul.allow_tf32 = True
                torch.backends.cudnn.allow_tf32 = True
                torch.backends.cudnn.benchmark = True
            
            # Use tiling for large images
            if max(samples["samples"].shape[-2:]) * 8 > 512:
                images = self._decode_tiled(vae, samples)
            else:
                with torch.cuda.amp.autocast(enabled=True):
                    images = vae.decode(samples["samples"])
            
            if len(images.shape) == 5:
                images = images.reshape(-1, images.shape[-3], images.shape[-2], images.shape[-1])
            
            return (images,)
            
        except Exception as e:
            print(f"Error during VAE decoding: {str(e)}")
            images = vae.decode(samples["samples"])
            if len(images.shape) == 5:
                images = images.reshape(-1, images.shape[-3], images.shape[-2], images.shape[-1])
            return (images,)