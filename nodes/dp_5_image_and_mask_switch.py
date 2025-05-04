import torch
import numpy as np

class DP_5_Image_And_Mask_Switch:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "select": ("INT", {"default": 1, "min": 1, "max": 5, "step": 1}),
                "export_with_mask_alpha": ("BOOLEAN", {"default": False, "label_on": "Yes", "label_off": "No"}),
                "force_rgb_output": ("BOOLEAN", {"default": False, "label_on": "Yes", "label_off": "No", "tooltip": "Convert RGBA to RGB for compatibility with nodes like RMBG"}),
            },
            "optional": {
                "images1": ("IMAGE",),
                "mask1_opt": ("MASK",),
                "images2_opt": ("IMAGE",),
                "mask2_opt": ("MASK",),
                "images3_opt": ("IMAGE",),
                "mask3_opt": ("MASK",),
                "images4_opt": ("IMAGE",),
                "mask4_opt": ("MASK",),
                "images5_opt": ("IMAGE",),
                "mask5_opt": ("MASK",),
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("image", "mask")
    FUNCTION = "switch_images_and_masks"
    CATEGORY = "DP/image"

    def switch_images_and_masks(self, select, export_with_mask_alpha=False, force_rgb_output=False, images1=None, mask1_opt=None, 
                             images2_opt=None, mask2_opt=None, 
                             images3_opt=None, mask3_opt=None, 
                             images4_opt=None, mask4_opt=None, 
                             images5_opt=None, mask5_opt=None):
        
        # Map selection to image and mask pairs
        image_options = [images1, images2_opt, images3_opt, images4_opt, images5_opt]
        mask_options = [mask1_opt, mask2_opt, mask3_opt, mask4_opt, mask5_opt]
        
        # Adjust for 1-based indexing in UI
        idx = select - 1
        
        # Check if the selected index is valid
        if idx < 0 or idx >= len(image_options):
            raise ValueError(f"Invalid selection: {select}. Must be between 1 and 5.")
        
        # Get the selected image and mask
        selected_image = image_options[idx]
        selected_mask = mask_options[idx]
        
        # If image is None, create an empty tensor (black image)
        if selected_image is None:
            selected_image = torch.zeros((1, 64, 64, 3), dtype=torch.float32)
            
        # If mask is None, create an empty mask
        if selected_mask is None:
            # Create mask matching the height and width of the selected image
            h = selected_image.shape[1]
            w = selected_image.shape[2]
            selected_mask = torch.zeros((1, h, w), dtype=torch.float32)
        
        # Apply mask as alpha channel if requested
        if export_with_mask_alpha and selected_image is not None and selected_mask is not None:
            # Get dimensions
            batch_size, height, width, channels = selected_image.shape
            
            # Check if image already has an alpha channel
            if channels == 3:
                # Convert the mask to inverted alpha (1.0 = fully visible, 0.0 = fully transparent)
                # ComfyUI masks are inverted (0=keep, 1=discard), so we need to invert them for alpha
                alpha = 1.0 - selected_mask
                
                # Reshape mask to match image dimensions for concatenation
                alpha_reshaped = alpha.view(batch_size, height, width, 1)
                
                # Create a new tensor with RGBA
                rgba_image = torch.cat((selected_image, alpha_reshaped), dim=3)
                selected_image = rgba_image
            elif channels == 4:
                # Image already has alpha, but we'll replace it with our mask
                # Keep RGB channels and add the new alpha
                rgb_channels = selected_image[:, :, :, :3]
                
                # Convert the mask to inverted alpha (1.0 = fully visible, 0.0 = fully transparent)
                alpha = 1.0 - selected_mask
                
                # Reshape mask to match image dimensions for concatenation
                alpha_reshaped = alpha.view(batch_size, height, width, 1)
                
                # Create a new tensor with RGBA
                rgba_image = torch.cat((rgb_channels, alpha_reshaped), dim=3)
                selected_image = rgba_image
        
        # Force RGB output if requested (especially for compatibility with nodes like RMBG)
        if force_rgb_output and selected_image.shape[3] == 4:
            # Keep only the RGB channels, discard alpha
            selected_image = selected_image[:, :, :, :3]
            
        return (selected_image, selected_mask)
