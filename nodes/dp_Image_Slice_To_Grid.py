import torch
import numpy as np
import os

class DP_Image_Slice_To_Grid:
    def __init__(self):
        self.output_dir = "ComfyUI/temp"
        pass
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "grid_size": ("INT", {"default": 2, "min": 1, "max": 10}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "slice_to_grid"
    CATEGORY = "DP/Image"

    def slice_to_grid(self, image, grid_size):
        # Convert from tensor format
        if isinstance(image, torch.Tensor):
            image = image.cpu().numpy()
        
        # Get image dimensions
        height, width = image.shape[1:3]
        
        # Calculate slice dimensions
        slice_height = height // grid_size
        slice_width = width // grid_size
        
        # Prepare list for slices
        slices = []
        
        # Create slices with overlap
        for i in range(grid_size):
            for j in range(grid_size):
                # Calculate boundaries with overlap
                y_start = max(0, i * slice_height - 0)
                y_end = min(height, (i + 1) * slice_height + 0)
                x_start = max(0, j * slice_width - 0)
                x_end = min(width, (j + 1) * slice_width + 0)
                
                # Extract slice
                slice_img = image[:, y_start:y_end, x_start:x_end, :]
                slices.append(torch.from_numpy(slice_img))
        
        # Stack all slices vertically
        result = torch.cat(slices, dim=0)
        
        return (result,)
