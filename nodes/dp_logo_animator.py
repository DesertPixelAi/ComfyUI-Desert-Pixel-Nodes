import torch
import torch.nn.functional as F
import numpy as np

class DPLogoAnimator:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "frame_count": ("INT", {"default": 48, "min": 2, "max": 300, "step": 1}),
                "min_scale": ("FLOAT", {"default": 0.2, "min": 0.1, "max": 0.99, "step": 0.01}),
                "background": (["Auto", "Black", "White"],),
                "loop_count": ("INT", {"default": 1, "min": 1, "max": 5, "step": 1}),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "animate_logo"
    CATEGORY = "DP/utils"

    def create_scale_sequence(self, start_scale, end_scale, num_frames):
        """Create a smooth scale sequence that goes from start to end and back"""
        half_frames = num_frames // 2
        down = torch.linspace(start_scale, end_scale, half_frames)
        up = torch.linspace(end_scale, start_scale, num_frames - half_frames)
        return torch.cat([down, up])

    def detect_background_color(self, image):
        """Detect the background color using edge sampling similar to BackgroundColorThief"""
        print("\nStarting background color detection...")
        print(f"Input image value range: {image.min():.3f} to {image.max():.3f}")
        
        # Convert to numpy if it's a tensor
        if torch.is_tensor(image):
            if len(image.shape) == 4:
                image = image[0]
            image = image.cpu().numpy()
            print(f"Converted tensor to numpy array, shape: {image.shape}")
        
        print(f"Image shape: {image.shape}, dtype: {image.dtype}")
        print(f"Image min/max values: {image.min():.3f}/{image.max():.3f}")

        h, w = image.shape[:2]
        
        # Calculate sampling limits (10% of width/height)
        width_limit = int(w * 0.1)
        height_limit = int(h * 0.1)
        print(f"Sampling limits - width: {width_limit}, height: {height_limit}")
        
        pixels = []
        
        # Sample top edge
        top_edge = image[:height_limit, :].reshape(-1, 3)
        pixels.extend(top_edge)
        print(f"Top edge samples: {len(top_edge)}")
        
        # Sample bottom edge
        bottom_edge = image[-height_limit:, :].reshape(-1, 3)
        pixels.extend(bottom_edge)
        print(f"Bottom edge samples: {len(bottom_edge)}")
        
        # Sample left edge (excluding corners already sampled)
        left_edge = image[height_limit:-height_limit, :width_limit].reshape(-1, 3)
        pixels.extend(left_edge)
        print(f"Left edge samples: {len(left_edge)}")
        
        # Sample right edge (excluding corners already sampled)
        right_edge = image[height_limit:-height_limit, -width_limit:].reshape(-1, 3)
        pixels.extend(right_edge)
        print(f"Right edge samples: {len(right_edge)}")
        
        # Convert to numpy array
        pixels = np.array(pixels)
        print(f"Total pixel samples: {len(pixels)}")
        
        # Use median to get the most common color
        bg_color = np.median(pixels, axis=0)
        print(f"Detected background color RGB: R={bg_color[0]:.3f}, G={bg_color[1]:.3f}, B={bg_color[2]:.3f}")
        
        return bg_color

    def animate_logo(self, image, frame_count=48, min_scale=0.2, background="Black", loop_count=1):
        print(f"\nAnimating logo with {frame_count} frames")
        
        # Ensure input format
        if len(image.shape) == 4:
            image = image[0]
        
        # Convert image from HWC to CHW format if needed
        if image.shape[-1] == 3:  # If image is in HWC format
            image = image.permute(2, 0, 1)
        
        print(f"Image shape after format conversion: {image.shape}")
        print(f"Image min/max values: {image.min():.3f}/{image.max():.3f}")
        
        # Get original dimensions
        c, h, w = image.shape
        
        # Set background color
        if background == "Auto":
            print("\nUsing Auto background detection")
            # Convert to HWC for background detection
            temp_img = image.permute(1, 2, 0).cpu().numpy()
            print(f"Temp image shape for detection: {temp_img.shape}")
            
            bg_color = self.detect_background_color(temp_img)
            print(f"Background color after detection: {bg_color}")
            
            # Create a properly shaped background tensor without dividing by 255
            bg_value = torch.tensor(bg_color, device=image.device, dtype=torch.float32).view(3, 1, 1)
            print(f"Background tensor value: {bg_value.squeeze()}")
        else:
            bg_value = 1.0 if background == "White" else 0.0
            bg_value = torch.tensor([bg_value] * 3, device=image.device).view(3, 1, 1)

        # Generate scale sequence
        scales = self.create_scale_sequence(1.0, min_scale, frame_count)
        
        frames = []
        for scale in scales:
            # Calculate new dimensions while maintaining aspect ratio
            scale_factor = scale.item()
            new_h = max(int(h * scale_factor), 1)
            new_w = max(int(w * scale_factor), 1)
            
            # Create background frame
            background_frame = bg_value.expand(3, h, w)
            
            # Resize the original image
            resized = F.interpolate(
                image.unsqueeze(0),
                size=(new_h, new_w),
                mode='bilinear',
                align_corners=False
            )[0]
            
            # Calculate padding for centering
            pad_h = (h - new_h) // 2
            pad_w = (w - new_w) // 2
            
            # Create the frame
            frame = background_frame.clone()
            frame[:, pad_h:pad_h + new_h, pad_w:pad_w + new_w] = resized
            
            # Convert to HWC format
            frame = frame.permute(1, 2, 0)
            frames.append(frame)
        
        # Create the base animation
        base_frames = torch.stack(frames)
        
        # Create the requested number of loops
        if loop_count > 1:
            output = torch.cat([base_frames] * loop_count, dim=0)
        else:
            output = base_frames
        
        return (output,)

# Update the node mappings
NODE_CLASS_MAPPINGS = {
    "DPLogoAnimator": DPLogoAnimator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DPLogoAnimator": "DP Logo Animator"
}