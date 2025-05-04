import torch
import numpy as np
import comfy.utils

class DP_Resize_Image_And_Mask:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "width": ("INT", {"default": 512, "min": 64, "max": 8192, "step": 8}),
                "height": ("INT", {"default": 512, "min": 64, "max": 8192, "step": 8}),
                "keep_proportions": ("BOOLEAN", {"default": False}),
                "upscale_method": (["nearest-exact", "bilinear", "area", "bicubic", "lanczos"],),
                "crop": (["disabled", "center"],),
                "export_image_with_alpha": ("BOOLEAN", {"default": False, "label_on": "Yes", "label_off": "No"}),
                "force_rgb_output": ("BOOLEAN", {"default": False, "label_on": "Yes", "label_off": "No", "tooltip": "Convert RGBA to RGB for compatibility with nodes like RMBG"}),
            },
            "optional": {
                "mask_opt": ("MASK",),
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("image", "mask")
    FUNCTION = "resize_image_and_mask"
    CATEGORY = "DP/image"

    def resize_image_and_mask(self, image, width, height, keep_proportions, upscale_method, crop, export_image_with_alpha=False, force_rgb_output=False, mask_opt=None):
        # Store original image dimensions
        orig_batch, orig_height, orig_width, orig_channels = image.shape
        
        # Process width and height based on keep_proportions setting
        if keep_proportions:
            # Calculate aspect ratio
            aspect_ratio = orig_width / orig_height
            
            # If only width or height is specified, calculate the other dimension
            if width > 0 and height == 0:
                height = max(64, int(width / aspect_ratio))
            elif height > 0 and width == 0:
                width = max(64, int(height * aspect_ratio))
            else:
                # Both width and height specified - maintain aspect ratio by using the smaller scale
                width_scale = width / orig_width
                height_scale = height / orig_height
                
                if width_scale < height_scale:
                    height = max(64, int(width / aspect_ratio))
                else:
                    width = max(64, int(height * aspect_ratio))
        
        # Ensure minimum dimensions
        width = max(64, width)
        height = max(64, height)
        
        # Resize image
        image_resized = self.resize_tensor(image, width, height, upscale_method, crop)
        
        # Resize mask if provided
        if mask_opt is not None:
            # Ensure mask dimensions match the original image
            if mask_opt.shape[1] != orig_height or mask_opt.shape[2] != orig_width:
                print(f"Warning: Mask dimensions ({mask_opt.shape[1]}x{mask_opt.shape[2]}) don't match image dimensions ({orig_height}x{orig_width}). Resizing mask to match image first.")
                # Resize mask to match original image dimensions first
                mask_opt = self.resize_mask(mask_opt, orig_width, orig_height, upscale_method, crop)
            
            # Now resize to target dimensions
            mask_resized = self.resize_mask(mask_opt, width, height, upscale_method, crop)
        else:
            # Create an empty mask with the target dimensions
            mask_resized = torch.zeros((orig_batch, height, width), dtype=torch.float32)
        
        # Apply mask as alpha channel if requested
        if export_image_with_alpha and mask_resized is not None:
            # Get dimensions
            batch_size, resized_height, resized_width, channels = image_resized.shape
            
            # Check if image already has an alpha channel
            if channels == 3:
                # Convert the mask to inverted alpha (1.0 = fully visible, 0.0 = fully transparent)
                # ComfyUI masks are inverted (0=keep, 1=discard), so we need to invert them for alpha
                alpha = 1.0 - mask_resized
                
                # Reshape mask to match image dimensions for concatenation
                alpha_reshaped = alpha.view(batch_size, resized_height, resized_width, 1)
                
                # Create a new tensor with RGBA
                rgba_image = torch.cat((image_resized, alpha_reshaped), dim=3)
                image_resized = rgba_image
            elif channels == 4:
                # Image already has alpha, but we'll replace it with our mask
                # Keep RGB channels and add the new alpha
                rgb_channels = image_resized[:, :, :, :3]
                
                # Convert the mask to inverted alpha (1.0 = fully visible, 0.0 = fully transparent)
                alpha = 1.0 - mask_resized
                
                # Reshape mask to match image dimensions for concatenation
                alpha_reshaped = alpha.view(batch_size, resized_height, resized_width, 1)
                
                # Create a new tensor with RGBA
                rgba_image = torch.cat((rgb_channels, alpha_reshaped), dim=3)
                image_resized = rgba_image
        
        # Force RGB output if requested (especially for compatibility with nodes like RMBG)
        if force_rgb_output and image_resized.shape[3] == 4:
            # Keep only the RGB channels, discard alpha
            image_resized = image_resized[:, :, :, :3]
        
        return (image_resized, mask_resized)
    
    def resize_tensor(self, tensor, width, height, method, crop_mode):
        # Move channels from last dimension to 2nd dimension (batch, height, width, channels) -> (batch, channels, height, width)
        samples = tensor.movedim(-1, 1)
        
        # Use comfy.utils.common_upscale for the actual resize operation
        resized = comfy.utils.common_upscale(samples, width, height, method, crop_mode)
        
        # Move channels back to last dimension (batch, channels, height, width) -> (batch, height, width, channels)
        result = resized.movedim(1, -1)
        
        return result
    
    def resize_mask(self, mask, width, height, method, crop_mode):
        # Add a channel dimension to mask for processing
        mask_expanded = mask.unsqueeze(1)  # (batch, height, width) -> (batch, 1, height, width)
        
        # Use comfy.utils.common_upscale for the actual resize operation
        resized = comfy.utils.common_upscale(mask_expanded, width, height, method, crop_mode)
        
        # Remove the channel dimension
        result = resized.squeeze(1)  # (batch, 1, height, width) -> (batch, height, width)
        
        return result 