import torch
import torch.nn.functional as F
import numpy as np

class DP_Logo_Animator_Advanced:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "full_loop_size": ("INT", {"default": 100, "min": 4, "max": 300, "step": 1}),
                "start_point_percent": ("INT", {"default": 0, "min": 0, "max": 100, "step": 1}),
                "end_point_percent": ("INT", {"default": 100, "min": 0, "max": 100, "step": 1}),
                "min_scale": ("FLOAT", {"default": 0.2, "min": 0.1, "max": 0.99, "step": 0.01}),
                "background": (["Auto", "Black", "White"],),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "animate_logo"
    CATEGORY = "DP/animation"

    def create_scale_sequence(self, start_scale, end_scale, num_frames):
        """Create a smooth scale sequence that goes from start to end and back"""
        half_frames = num_frames // 2
        down = torch.linspace(start_scale, end_scale, half_frames)
        up = torch.linspace(end_scale, start_scale, num_frames - half_frames)
        return torch.cat([down, up])

    def detect_background_color(self, image):
        """Detect the background color using edge sampling similar to BackgroundColorThief"""
        if torch.is_tensor(image):
            if len(image.shape) == 4:
                image = image[0]
            image = image.cpu().numpy()
        
        h, w = image.shape[:2]
        width_limit = int(w * 0.1)
        height_limit = int(h * 0.1)
        
        # Collect edge pixels
        pixels = []
        # Top edge
        pixels.extend(image[:height_limit, :].reshape(-1, image.shape[-1]))
        # Bottom edge
        pixels.extend(image[-height_limit:, :].reshape(-1, image.shape[-1]))
        # Left edge (excluding corners)
        pixels.extend(image[height_limit:-height_limit, :width_limit].reshape(-1, image.shape[-1]))
        # Right edge (excluding corners)
        pixels.extend(image[height_limit:-height_limit, -width_limit:].reshape(-1, image.shape[-1]))
        
        pixels = np.array(pixels)
        bg_color = np.median(pixels, axis=0)
        
        return bg_color

    def animate_logo(self, image, full_loop_size=100, start_point_percent=0, end_point_percent=100, min_scale=0.2, background="Black"):
        # Handle batched input - take only the first image if multiple are provided
        if len(image.shape) == 4:
            image = image[0]  # Take first image from batch
        
        # Convert image from HWC to CHW format if needed
        if image.shape[-1] in [3, 4]:  # Handle both RGB and RGBA
            image = image.permute(2, 0, 1)
            if image.shape[0] == 4:  # If RGBA, convert to RGB
                rgb = image[:3]
                alpha = image[3:]
                # Composite over white background
                image = rgb * alpha + (1 - alpha)
        
        c, h, w = image.shape
        
        # Set background color
        if background == "Auto":
            temp_img = image.permute(1, 2, 0).cpu().numpy()
            bg_color = self.detect_background_color(temp_img)
            bg_value = torch.tensor(bg_color, device=image.device, dtype=torch.float32)
        else:
            bg_value = 1.0 if background == "White" else 0.0
            bg_value = torch.full((3,), bg_value, device=image.device, dtype=torch.float32)
        
        # Reshape background value for broadcasting
        bg_value = bg_value.view(3, 1, 1)

        # Generate scale sequence
        scales = self.create_scale_sequence(1.0, min_scale, full_loop_size)
        
        # Calculate frame indices to keep based on start_point_percent and end_point_percent
        start_frame = int((start_point_percent / 100) * full_loop_size)
        end_frame = int((end_point_percent / 100) * full_loop_size)
        
        # Select only the frames within the specified range
        selected_scales = scales[start_frame:end_frame]
        
        frames = []
        for scale in selected_scales:
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
        
        # Stack all frames into a single tensor
        output = torch.stack(frames)
        
        return (output,)

# Update the node mappings
NODE_CLASS_MAPPINGS = {
    "DP_Logo_Animator_Advanced": DP_Logo_Animator_Advanced
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DP_Logo_Animator_Advanced": "DP Logo Animator Advanced"
} 