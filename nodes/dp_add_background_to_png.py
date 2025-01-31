import torch

class DP_Add_Background_To_Png:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "mask": ("MASK",),
                "background_color": ([
                    "white", "black", "red", "green", "blue",
                    "yellow", "purple", "cyan", "orange", "pink",
                    "gray", "brown", "navy", "lime", "magenta"
                ], {"default": "white"}),
                "invert_mask": (["false", "true"], {"default": "false"}),
                "duplicate_layers": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 5,
                    "step": 1
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("image", "mask")
    FUNCTION = "process"
    CATEGORY = "DP/image"

    def get_color_value(self, color_name):
        # RGB values as floats (0-1)
        colors = {
            "white": (1.0, 1.0, 1.0),
            "black": (0.0, 0.0, 0.0),
            "red": (1.0, 0.0, 0.0),
            "green": (0.0, 1.0, 0.0),
            "blue": (0.0, 0.0, 1.0),
            "yellow": (1.0, 1.0, 0.0),
            "purple": (0.5, 0.0, 0.5),
            "cyan": (0.0, 1.0, 1.0),
            "orange": (1.0, 0.65, 0.0),
            "pink": (1.0, 0.75, 0.8),
            "gray": (0.5, 0.5, 0.5),
            "brown": (0.65, 0.16, 0.16),
            "navy": (0.0, 0.0, 0.5),
            "lime": (0.0, 1.0, 0.0),
            "magenta": (1.0, 0.0, 1.0)
        }
        return colors.get(color_name, (1.0, 1.0, 1.0))

    def process(self, image, mask, background_color, invert_mask, duplicate_layers):
        try:
            # Ensure image is in the correct format
            if len(image.shape) == 3:
                image = image.unsqueeze(0)
            
            # Ensure mask is in the correct format
            if len(mask.shape) == 2:
                mask = mask.unsqueeze(0)
            
            batch_size, height, width, channels = image.shape
            
            # Get RGB values for selected color
            r, g, b = self.get_color_value(background_color)
            
            # Create background with selected color
            background = torch.zeros((batch_size, height, width, 3), device=image.device)
            background[..., 0] = r  # Red channel
            background[..., 1] = g  # Green channel
            background[..., 2] = b  # Blue channel
            
            # Handle mask inversion
            if invert_mask == "true":
                mask = 1.0 - mask
            
            # Expand mask dimensions for broadcasting
            mask = mask.unsqueeze(-1)
            
            # Use the provided mask for blending
            if channels == 4:
                # Use RGB channels only from input
                rgb = image[..., :3]
            else:
                rgb = image
            
            # Initialize result with background
            result = background.clone()
            
            # Stack layers multiple times
            for _ in range(duplicate_layers):
                # Calculate alpha for this layer
                layer_alpha = mask * (1 - (result - background).abs().mean(dim=-1, keepdim=True))
                # Blend this layer
                result = rgb * layer_alpha + result * (1 - layer_alpha)
            
            # Return both the composited image and the final mask
            return (result, mask.squeeze(-1))
            
        except Exception as e:
            print(f"Error in DP_Add_Background_To_Png: {str(e)}")
            return (image, mask) 