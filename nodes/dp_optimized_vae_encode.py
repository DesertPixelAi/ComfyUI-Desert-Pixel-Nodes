import torch
import math
from typing import Tuple, Dict, Any

class DP_VAE_Encode_Optimized:
    _pinned_memory = {}  # Cache for pinned memory buffers
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "pixels": ("IMAGE", {"tooltip": "The image to be encoded."}),
                "vae": ("VAE", {"tooltip": "The VAE model used for encoding."})
            }
        }
    
    RETURN_TYPES = ("LATENT",)
    FUNCTION = "encode"
    CATEGORY = "DP/optimized"

    def _encode_tiled(self, vae: Any, pixels: torch.Tensor, tile_size: int = 512) -> torch.Tensor:
        """Encode pixels using tiling strategy for large images."""
        output_device = pixels.device
        bs, h, w, c = pixels.shape
        
        num_tiles_h = math.ceil(h / tile_size)
        num_tiles_w = math.ceil(w / tile_size)
        
        latent_h, latent_w = h // 8, w // 8
        output = torch.zeros((bs, 4, latent_h, latent_w), device=output_device)
        
        for h_idx in range(num_tiles_h):
            for w_idx in range(num_tiles_w):
                h_start = h_idx * tile_size
                w_start = w_idx * tile_size
                h_end = min((h_idx + 1) * tile_size, h)
                w_end = min((w_idx + 1) * tile_size, w)
                
                tile_pixels = pixels[:, h_start:h_end, w_start:w_end, :3].clone()
                
                with torch.cuda.amp.autocast(enabled=True):
                    tile_encoded = vae.encode(tile_pixels)
                
                out_h_start = h_start // 8
                out_w_start = w_start // 8
                out_h_end = math.ceil(h_end / 8)
                out_w_end = math.ceil(w_end / 8)
                
                output[:, :, out_h_start:out_h_end, out_w_start:out_w_end] = tile_encoded
                
        torch.cuda.empty_cache()
        return output

    def encode(self, vae: Any, pixels: torch.Tensor) -> Tuple[Dict[str, torch.Tensor]]:
        """Encode pixels to latents with optimizations."""
        try:
            # Only use pinned memory if input is on CPU
            if pixels.device.type == "cpu":
                batch_key = f"{pixels.shape}_{pixels.dtype}"
                if batch_key not in self._pinned_memory:
                    self._pinned_memory[batch_key] = torch.zeros_like(
                        pixels, 
                        pin_memory=True
                    )
                self._pinned_memory[batch_key].copy_(pixels)
                pixels = self._pinned_memory[batch_key].cuda(non_blocking=True)
            
            # Always apply optimizations
            if torch.cuda.is_available():
                torch.backends.cuda.matmul.allow_tf32 = True
                torch.backends.cudnn.allow_tf32 = True
                torch.backends.cudnn.benchmark = True
            
            # Use tiling for large images
            if max(pixels.shape[1:3]) > 512:
                latents = self._encode_tiled(vae, pixels)
            else:
                with torch.cuda.amp.autocast(enabled=True):
                    latents = vae.encode(pixels[:, :, :, :3])
            
            return ({"samples": latents},)
            
        except Exception as e:
            print(f"Error during VAE encoding: {str(e)}")
            # Fallback to basic encoding
            latents = vae.encode(pixels[:, :, :, :3])
            return ({"samples": latents},) 