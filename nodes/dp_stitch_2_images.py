import torch
import comfy.utils

class DP_Stitch_2_Images:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image1": ("IMAGE",),
                "image2": ("IMAGE",),
                "mode": (["Horizontal_Right", "Horizontal_Left", "Vertical_Up", "Vertical_Down"],),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image_strip",)
    FUNCTION = "stitch_images"
    CATEGORY = "DP/image"

    def stitch_images(self, image1, image2, mode):
        # Input validation
        if image1 is None or image2 is None:
            raise ValueError("Both images must be provided")
            
        # Get dimensions
        height1 = image1.shape[1]
        width1 = image1.shape[2]
        height2 = image2.shape[1]
        width2 = image2.shape[2]
        
        # Take first frame if multiple frames provided
        if len(image1.shape) == 4 and image1.shape[0] > 1:
            image1 = image1[0:1]
        if len(image2.shape) == 4 and image2.shape[0] > 1:
            image2 = image2[0:1]
        
        is_horizontal = mode.startswith("Horizontal")
        
        # Check dimensions match based on mode
        if is_horizontal and height1 != height2:
            raise ValueError(f"For horizontal stitching, both images must have the same height. Image 1 height: {height1}, Image 2 height: {height2}")
        if not is_horizontal and width1 != width2:
            raise ValueError(f"For vertical stitching, both images must have the same width. Image 1 width: {width1}, Image 2 width: {width2}")
        
        # Prepare images in correct order
        if mode in ["Horizontal_Right", "Vertical_Down"]:
            images = [image2, image1]
        else:
            images = [image1, image2]

        # Concatenate images based on mode
        if is_horizontal:
            # Concatenate horizontally
            return (torch.cat(images, dim=2),)  # Concatenate along width
        else:
            # Concatenate vertically
            return (torch.cat(images, dim=1),)  # Concatenate along height 