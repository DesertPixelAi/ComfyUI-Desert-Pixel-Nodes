import torch
import comfy.utils

class DP_Image_Strip:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "mode": (["Horizontal_Right", "Horizontal_Left", "Vertical_Up", "Vertical_Down"],),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image_strip",)
    FUNCTION = "create_strip"
    CATEGORY = "DP/image"

    def create_strip(self, images, mode):
        # Limit to 10 images if more are provided
        batch_size = min(len(images), 10)
        if batch_size == 0:
            raise ValueError("No images provided")
        
        # Determine target height based on number of images
        target_height = 1024 if batch_size <= 5 else 512
        
        # Process each image in the batch
        processed_images = []
        for i in range(batch_size):
            img = images[i:i+1]  # Take one image at a time
            
            # Calculate new width maintaining aspect ratio
            current_height = img.shape[1]
            current_width = img.shape[2]
            aspect_ratio = current_width / current_height
            new_width = int(target_height * aspect_ratio)
            
            # Resize image
            samples = img.movedim(-1, 1)
            resized = comfy.utils.common_upscale(samples, new_width, target_height, "lanczos", "center")
            processed = resized.movedim(1, -1)
            processed_images.append(processed)

        # Reverse the order if needed based on mode
        if mode in ["Horizontal_Right", "Vertical_Down"]:
            processed_images.reverse()

        # Concatenate images based on mode
        if mode.startswith("Horizontal"):
            # Concatenate horizontally
            return (torch.cat(processed_images, dim=2),)  # Concatenate along width
        else:
            # Concatenate vertically
            return (torch.cat(processed_images, dim=1),)  # Concatenate along height 