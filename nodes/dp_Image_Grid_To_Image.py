import torch
import numpy as np

class DP_Image_Grid_To_Image:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "slices": ("IMAGE",),
                "rows": ("INT", {"default": 2}),
                "columns": ("INT", {"default": 2}),
                "overlap": ("INT", {"default": 64}),
                "feather": ("INT", {"default": 32, "min": 0, "max": 256}),
            },
            "optional": {
                "stroke_size": ("INT", {"default": 0, "min": 0, "max": 100}),
                "stroke_color": (["black", "white", "red", "green", "blue", "cyan", "magenta", "yellow"], {"default": "white"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "stitch_image"
    CATEGORY = "image/processing"

    def get_stroke_color(self, color_name):
        colors = {
            "black": [0, 0, 0],
            "white": [1, 1, 1],
            "red": [1, 0, 0],
            "green": [0, 1, 0],
            "blue": [0, 0, 1],
            "cyan": [0, 1, 1],
            "magenta": [1, 0, 1],
            "yellow": [1, 1, 0]
        }
        return colors[color_name]

    def create_feather_mask(self, size, feather):
        # Create linear gradients for feathering
        mask = torch.ones(size)
        for i in range(feather):
            # Linear fade from 0 to 1
            mask[i] = i / feather
            # Linear fade from 1 to 0
            mask[-i-1] = i / feather
        return mask

    def stitch_image(self, slices, rows, columns, overlap, feather, stroke_size=0, stroke_color="white"):
        slice_list = torch.split(slices, 1, dim=0)
        _, slice_height, slice_width, channels = slice_list[0].shape
        
        output_height = (slice_height - overlap) * rows + overlap
        output_width = (slice_width - overlap) * columns + overlap
        
        # Initialize output and weight accumulator
        result = torch.zeros((1, output_height, output_width, channels), 
                           device=slices.device, dtype=slices.dtype)
        weights = torch.zeros((1, output_height, output_width, 1), 
                            device=slices.device, dtype=slices.dtype)
        
        # Create feather masks
        vertical_mask = self.create_feather_mask(slice_height, feather)
        horizontal_mask = self.create_feather_mask(slice_width, feather)
        
        # Convert to 2D masks
        vertical_mask = vertical_mask.view(-1, 1).expand(-1, slice_width)
        horizontal_mask = horizontal_mask.view(1, -1).expand(slice_height, -1)
        
        # Combine masks
        blend_mask = (vertical_mask * horizontal_mask).unsqueeze(0).unsqueeze(-1)
        blend_mask = blend_mask.to(device=slices.device, dtype=slices.dtype)

        for idx, slice_img in enumerate(slice_list):
            i = idx // columns
            j = idx % columns
            
            y_start = i * (slice_height - overlap)
            x_start = j * (slice_width - overlap)
            y_end = y_start + slice_height
            x_end = x_start + slice_width
            
            # Apply stroke if size > 0
            if stroke_size > 0:
                color = torch.tensor(self.get_stroke_color(stroke_color), 
                                  device=slice_img.device, dtype=slice_img.dtype)
                
                # Create stroke mask
                stroke_mask = torch.ones_like(slice_img)
                stroke_mask[:, stroke_size:-stroke_size, stroke_size:-stroke_size, :] = 0
                
                # Apply stroke color
                slice_img = slice_img * (1 - stroke_mask) + color.view(1, 1, 1, 3) * stroke_mask
            
            # Apply blending mask to slice
            masked_slice = slice_img * blend_mask
            
            # Add to result with blending
            result[:, y_start:y_end, x_start:x_end, :] += masked_slice
            weights[:, y_start:y_end, x_start:x_end, :] += blend_mask

        # Normalize by weights to get final image
        result = result / (weights + 1e-8)  # Add small epsilon to avoid division by zero
        
        return (result,) 