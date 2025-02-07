import torch
import torch.nn.functional as F
import numpy as np

class DP_Mask_Settings:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "expand": ("INT", {"default": 0, "min": -256, "max": 256, "step": 1}),
                "blur": ("INT", {"default": 0, "min": 0, "max": 256, "step": 1}),
            },
            "optional": {
                "mask": ("MASK",),
                "image_input": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("MASK", "IMAGE")
    RETURN_NAMES = ("mask", "image")
    FUNCTION = "process_mask"
    CATEGORY = "DP/mask"

    def image_to_mask(self, image):
        # Convert image to grayscale mask
        if image is None:
            return None
        # If image is RGB, convert to grayscale using luminance weights
        if len(image.shape) == 4 and image.shape[-1] == 3:
            mask = image[..., 0] * 0.299 + image[..., 1] * 0.587 + image[..., 2] * 0.114
        else:
            mask = image.squeeze(-1)
        return mask

    def mask_to_image(self, mask):
        if mask is None:
            return None
        # Convert mask to RGB image
        result = mask.reshape((-1, 1, mask.shape[-2], mask.shape[-1])).movedim(1, -1).expand(-1, -1, -1, 3)
        return result

    def process_mask(self, expand, blur, mask=None, image_input=None):
        # Handle input conversion
        if mask is None and image_input is not None:
            mask = self.image_to_mask(image_input)
        elif mask is None and image_input is None:
            raise ValueError("Either mask or image_input must be provided")

        # Ensure mask is the right shape
        if len(mask.shape) == 2:
            mask = mask.unsqueeze(0)  # Add batch dimension
        
        # Convert to float if needed
        mask = mask.float()
        
        if expand != 0:
            # Create kernel for dilation/erosion
            kernel_size = abs(expand) * 2 + 1
            kernel = torch.ones(1, 1, kernel_size, kernel_size)
            
            # Pad the mask for the convolution
            pad_size = kernel_size // 2
            padded_mask = F.pad(mask.unsqueeze(1), (pad_size, pad_size, pad_size, pad_size), mode='reflect')
            
            if expand > 0:
                # Dilation (expand outward)
                mask = F.max_pool2d(padded_mask, kernel_size, stride=1, padding=0)
            else:
                # Erosion (expand inward)
                mask = -F.max_pool2d(-padded_mask, kernel_size, stride=1, padding=0)
            
            mask = mask.squeeze(1)  # Remove channel dimension
            
        if blur > 0:
            # Apply Gaussian blur
            kernel_size = blur * 2 + 1
            sigma = blur / 3.0
            
            # Ensure kernel size is odd
            if kernel_size % 2 == 0:
                kernel_size += 1
            
            # Create Gaussian kernel
            x = torch.linspace(-sigma * 2, sigma * 2, kernel_size)
            kernel = torch.exp(-x.pow(2) / (2 * sigma ** 2))
            kernel = (kernel / kernel.sum()).to(mask.device)
            
            # Apply separable Gaussian blur
            padded = F.pad(mask.unsqueeze(1), (kernel_size//2, kernel_size//2, 0, 0), mode='reflect')
            blurred = F.conv2d(padded, kernel.view(1, 1, 1, -1), padding=0)
            padded = F.pad(blurred, (0, 0, kernel_size//2, kernel_size//2), mode='reflect')
            mask = F.conv2d(padded, kernel.view(1, 1, -1, 1), padding=0)
            mask = mask.squeeze(1)  # Remove channel dimension
        
        # Clamp values between 0 and 1
        mask = torch.clamp(mask, 0.0, 1.0)
        
        # Convert mask to image for second output
        image_output = self.mask_to_image(mask)
        
        return (mask, image_output)