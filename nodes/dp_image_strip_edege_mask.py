import torch
import torch.nn.functional as F
import comfy.utils

class DP_Strip_Edge_Masks:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "mode": (["Horizontal_Right", "Horizontal_Left", "Vertical_Up", "Vertical_Down"],),
                "edge_width": ("INT", {"default": 64, "min": 0, "max": 512, "step": 1}),
                "feather": ("INT", {"default": 32, "min": 0, "max": 256, "step": 1}),
                "output_mode": (["separate_masks", "combined_mask"], {"default": "separate_masks"}),
            }
        }
    RETURN_TYPES = ("IMAGE", "MASK",)
    RETURN_NAMES = ("combined_strip", "edge_masks",)
    FUNCTION = "create_edge_masks"
    CATEGORY = "DP/image"

    def create_edge_masks(self, images, mode, edge_width, feather, output_mode):
        # Limit to 10 images if more are provided
        batch_size = min(len(images), 10)
        if batch_size == 0:
            raise ValueError("No images provided")
        
        # Determine target height based on number of images
        target_height = 1024 if batch_size <= 5 else 512
        
        # Process each image in the batch
        processed_images = []
        for i in range(batch_size):
            img = images[i:i+1]
            
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

        # Create edge masks
        edge_masks = []
        is_horizontal = mode.startswith("Horizontal")

        # Calculate total dimensions for the combined image
        if is_horizontal:
            total_width = sum([img.shape[2] for img in processed_images])
            total_height = target_height
        else:
            total_width = processed_images[0].shape[2]
            total_height = sum([img.shape[1] for img in processed_images])

        # Create blank mask for the full size
        full_mask = torch.zeros((1, total_height, total_width))
        current_pos = 0

        for i in range(len(processed_images) - 1):  # We need one less mask than images
            if is_horizontal:
                # Calculate the center position between current and next image
                current_image_width = processed_images[i].shape[2]
                current_pos += current_image_width  # Move to the end of current image
                
                # Create mask centered on the join
                mask_width = edge_width * 2
                mask_height = target_height  # Define mask_height for horizontal case
                mask_start = current_pos - edge_width  # Center the mask on the join
                
                # Create and feather the mask
                mask = torch.ones((1, mask_height, mask_width))
                if feather > 0:
                    # Create feathering gradients
                    x = torch.linspace(0, 1, feather)
                    left_feather = x.view(1, 1, -1).repeat(1, mask_height, 1)
                    right_feather = torch.flip(left_feather, [2])
                    
                    # Apply feathering only to the edges
                    center_width = mask_width - (2 * feather)
                    if center_width > 0:
                        mask[:, :, :feather] *= left_feather
                        mask[:, :, -feather:] *= right_feather
                    else:
                        # If feather is too large, blend in the middle
                        mask[:, :, :mask_width//2] *= left_feather[:, :, :mask_width//2]
                        mask[:, :, mask_width//2:] *= right_feather[:, :, -mask_width//2:]

                # Add to full mask at the centered position
                full_mask[:, :, mask_start:mask_start + mask_width] = mask
                
                # Also store individual mask
                if output_mode == "separate_masks":
                    edge_masks.append(mask)

            else:  # Vertical
                # Similar updates for vertical stacking
                current_image_height = processed_images[i].shape[1]
                current_pos += current_image_height
                
                mask_height = edge_width * 2
                mask_width = processed_images[i].shape[2]  # Define mask_width for vertical case
                mask_start = current_pos - edge_width
                
                # Create and feather the mask
                mask = torch.ones((1, mask_height, mask_width))
                if feather > 0:
                    y = torch.linspace(0, 1, feather)
                    top_feather = y.view(1, -1, 1).repeat(1, 1, mask_width)
                    bottom_feather = torch.flip(top_feather, [1])
                    
                    # Apply feathering
                    center_height = mask_height - (2 * feather)
                    if center_height > 0:
                        mask[:, :feather, :] *= top_feather
                        mask[:, -feather:, :] *= bottom_feather
                    else:
                        mask[:, :mask_height//2, :] *= top_feather[:, :mask_height//2, :]
                        mask[:, mask_height//2:, :] *= bottom_feather[:, -mask_height//2:, :]

                # Add to full mask
                full_mask[:, mask_start:mask_start + mask_height, :] = mask
                
                # Also store individual mask
                if output_mode == "separate_masks":
                    edge_masks.append(mask)

        # Concatenate images
        if is_horizontal:
            combined_image = torch.cat(processed_images, dim=2)
        else:
            combined_image = torch.cat(processed_images, dim=1)

        if output_mode == "separate_masks":
            # Stack individual masks
            edge_masks = torch.cat(edge_masks, dim=0)
        else:
            # Use the full combined mask
            edge_masks = full_mask

        return (combined_image, edge_masks)