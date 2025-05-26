import torch
import logging

logger = logging.getLogger('DP_Nodes')

class DP_Extract_Mask:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("image", "mask")
    FUNCTION = "extract_mask"
    CATEGORY = "DP/image"

    def extract_mask(self, image):
        # Ensure image is in the correct format (batch, height, width, channels)
        if len(image.shape) == 3:
            image = image.unsqueeze(0)
        
        batch_size, height, width, channels = image.shape
        logger.info(f"Processing image with shape: {image.shape}, channels: {channels}")
        
        # If input is RGB, create a mask of zeros (fully opaque)
        if channels == 3:
            logger.info("RGB image detected - creating fully opaque mask (all zeros)")
            mask = torch.zeros((batch_size, height, width), device=image.device)
            return (image, mask)
        
        # For RGBA images
        if channels == 4:
            logger.info("RGBA image detected - extracting alpha channel as mask")
            # Extract alpha channel and convert it to mask
            # ComfyUI masks are inverted (0=keep, 1=discard)
            # So we need to invert the alpha channel (1-alpha)
            mask = 1.0 - image[..., 3]
            
            # Return the RGB image and the mask
            rgb_image = image[..., :3].clone()
            
            # Log mask statistics for debugging
            logger.info(f"Mask statistics - min: {mask.min().item():.3f}, max: {mask.max().item():.3f}, mean: {mask.mean().item():.3f}")
            
            return (rgb_image, mask)
        
        # Handle unexpected number of channels
        logger.warning(f"Unexpected number of channels: {channels}")
        mask = torch.zeros((batch_size, height, width), device=image.device)
        return (image[..., :3] if channels > 3 else image, mask) 