import torch
import torch.nn.functional as F
import numpy as np

class DP_Mask_Settings:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask": ("MASK",),
                "expand": ("INT", {"default": 0, "min": -256, "max": 256, "step": 1}),
                "blur": ("INT", {"default": 0, "min": 0, "max": 256, "step": 1}),
            }
        }

    RETURN_TYPES = ("MASK",)
    FUNCTION = "process_mask"
    CATEGORY = "DP/mask"

    def process_mask(self, mask, expand, blur):
        # Ensure mask is the right shape and on CPU
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
        
        return (mask,)