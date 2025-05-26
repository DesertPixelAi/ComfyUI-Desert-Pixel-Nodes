import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image

class DP_Image_To_Pixelgrid:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "grid_size": ("INT", {"default": 64, "min": 8, "max": 256, "step": 1}),
                "quantize_colors": ("BOOLEAN", {"default": True}),
                "color_count": ("INT", {"default": 32, "min": 2, "max": 256, "step": 1}),
                "grid_lines": ("BOOLEAN", {"default": False}),
                "grid_line_color": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "grid_line_width": ("INT", {"default": 1, "min": 1, "max": 5, "step": 1}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "convert_to_pixel_art"
    CATEGORY = "image/processing"

    def convert_to_pixel_art(self, image, grid_size=64, quantize_colors=True, color_count=32, 
                           grid_lines=False, grid_line_color=0.0, grid_line_width=1):
        # Convert from ComfyUI image format (B,H,W,C) to (B,C,H,W) for processing
        img = image.permute(0, 3, 1, 2)
        batch_size, channels, height, width = img.shape
        
        # Step 1: Downsample to grid_size using area interpolation (average pooling)
        # This gets the average color for each cell
        small = F.interpolate(img, size=(grid_size, grid_size), mode='area')
        
        # Step 2: Optional color quantization
        if quantize_colors:
            # Convert to numpy for color processing
            small_np = small.permute(0, 2, 3, 1).cpu().numpy()
            
            for b in range(batch_size):
                # Convert to PIL for color quantization
                img_pil = Image.fromarray((small_np[b] * 255).astype(np.uint8))
                # Use adaptive palette for better results
                img_pil = img_pil.convert('P', palette=Image.ADAPTIVE, colors=color_count)
                # Convert back to RGB
                small_np[b] = np.array(img_pil.convert('RGB')) / 255.0
            
            # Back to torch tensor
            small = torch.from_numpy(small_np).permute(0, 3, 1, 2).to(image.device)
        
        # Step 3: Calculate cell size for the final image
        # Use float division to get more accurate cell sizes
        cell_height_float = height / grid_size
        cell_width_float = width / grid_size
        
        # Create a new empty image with the original dimensions
        result = torch.zeros_like(img)
        
        # Step 4: Fill each cell with solid color
        for i in range(grid_size):
            for j in range(grid_size):
                # Get the color for this cell
                cell_color = small[:, :, i, j].unsqueeze(2).unsqueeze(3)
                
                # Calculate pixel positions for this cell more precisely
                y_start = int(i * cell_height_float)
                y_end = int((i + 1) * cell_height_float) if i < grid_size - 1 else height
                x_start = int(j * cell_width_float)
                x_end = int((j + 1) * cell_width_float) if j < grid_size - 1 else width
                
                # Fill the cell with the solid color
                result[:, :, y_start:y_end, x_start:x_end] = cell_color
        
        # Step 5: Optional grid lines
        if grid_lines:
            for i in range(1, grid_size):
                # Horizontal lines with precise positioning
                y_pos = int(i * cell_height_float)
                if y_pos < height:
                    line_height = min(grid_line_width, height - y_pos)  # Prevent overflow
                    result[:, :, y_pos:y_pos+line_height, :] = grid_line_color
                
                # Vertical lines with precise positioning
                x_pos = int(i * cell_width_float)
                if x_pos < width:
                    line_width = min(grid_line_width, width - x_pos)  # Prevent overflow
                    result[:, :, :, x_pos:x_pos+line_width] = grid_line_color
        
        # Convert back to ComfyUI format (B,H,W,C)
        result = result.permute(0, 2, 3, 1)
        return (result,)

NODE_CLASS_MAPPINGS = {
    "DP_Image_To_Pixelgrid": DP_Image_To_Pixelgrid
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DP_Image_To_Pixelgrid": "DP Image To Pixelgrid"
}