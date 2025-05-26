import torch
import numpy as np

class DP_Place_Image:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 8}),
                "height": ("INT", {"default": 1024, "min": 64, "max": 8192, "step": 8}),
                "x_position": ("INT", {"default": 0, "min": -8192, "max": 8192, "step": 1}),
                "y_position": ("INT", {"default": 0, "min": -8192, "max": 8192, "step": 1}),
            },
            "optional": {
                "mask": ("MASK",),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "place_image"
    CATEGORY = "DP/image"

    def place_image(self, image, width, height, x_position, y_position, mask=None):
        # Ensure image is in the correct format (batch, height, width, channels)
        if len(image.shape) == 3:
            image = image.unsqueeze(0)
        
        batch_size, img_height, img_width, channels = image.shape
        
        # Create empty RGBA canvas (fully transparent)
        canvas = torch.zeros((batch_size, height, width, 4), device=image.device)
        
        # Convert input image to RGBA if it's RGB
        if channels == 3:
            # Add alpha channel (fully opaque)
            alpha = torch.ones((batch_size, img_height, img_width, 1), device=image.device)
            image = torch.cat([image, alpha], dim=-1)
        
        # Calculate valid placement coordinates
        x_start = max(0, x_position)
        y_start = max(0, y_position)
        x_end = min(width, x_position + img_width)
        y_end = min(height, y_position + img_height)
        
        # Calculate source image coordinates
        src_x_start = max(0, -x_position)
        src_y_start = max(0, -y_position)
        src_x_end = src_x_start + (x_end - x_start)
        src_y_end = src_y_start + (y_end - y_start)
        
        # Only proceed if there's a valid overlap
        if x_end > x_start and y_end > y_start and src_x_end > src_x_start and src_y_end > src_y_start:
            # Get the source image region
            source = image[:, src_y_start:src_y_end, src_x_start:src_x_end, :]
            
            # If mask is provided, apply it to the alpha channel
            if mask is not None:
                if len(mask.shape) == 2:
                    mask = mask.unsqueeze(0)
                # Get the corresponding mask region
                mask_region = mask[:, src_y_start:src_y_end, src_x_start:src_x_end]
                # Apply mask to alpha channel (invert mask as ComfyUI masks are inverted)
                source[..., 3] = source[..., 3] * (1.0 - mask_region)
            
            # Place the image on the canvas using alpha compositing
            source_alpha = source[..., 3:4]
            canvas_region = canvas[:, y_start:y_end, x_start:x_end, :]
            
            # Alpha compositing formula
            canvas[:, y_start:y_end, x_start:x_end, :3] = (
                source[..., :3] * source_alpha +
                canvas_region[..., :3] * (1 - source_alpha)
            )
            canvas[:, y_start:y_end, x_start:x_end, 3:] = (
                source_alpha + canvas_region[..., 3:4] * (1 - source_alpha)
            )
        
        return (canvas,) 