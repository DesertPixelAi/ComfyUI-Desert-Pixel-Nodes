import torch
import numpy as np
from PIL import Image
import torch.nn.functional as F

class DP_FastSlowMotion:
    def __init__(self):
        self.type = "DP_FastSlowMotion"
        self.input_dir = "input"
        self.output_dir = "output"
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "frames": ("IMAGE",),  # Batch of input frames as tensor
                "start_frame": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 10000,
                    "step": 1,
                    "display": "number"
                }),
                "end_frame": ("INT", {
                    "default": 10,
                    "min": 0,
                    "max": 10000,
                    "step": 1,
                    "display": "number"
                }),
                "speed": ("FLOAT", {
                    "default": 0.0,
                    "min": -4.0,
                    "max": 4.0,
                    "step": 0.1,
                    "display": "slider"
                })
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_speed_effect"
    CATEGORY = "DP/animation"

    def ensure_tensor_format(self, image):
        """Ensure the image tensor is in the correct format (BCHW)"""
        if not isinstance(image, torch.Tensor):
            image = torch.tensor(image)
        
        # Handle different input dimensions
        if len(image.shape) == 2:  # HW format
            image = image.unsqueeze(0).unsqueeze(0)  # Add batch and channel dims
        elif len(image.shape) == 3:  # CHW or HWC format
            if image.shape[-1] in [1, 3, 4]:  # HWC format
                image = image.permute(2, 0, 1)  # HWC to CHW
            image = image.unsqueeze(0)  # Add batch dim
        elif len(image.shape) == 4:  # Already in BCHW format
            pass
        else:
            raise ValueError(f"Unsupported image shape: {image.shape}")
            
        return image

    def apply_speed_effect(self, frames, start_frame, end_frame, speed):
        try:
            # Ensure frames are in the correct format
            if isinstance(frames, list):
                frames = torch.cat([self.ensure_tensor_format(f) for f in frames], dim=0)
            else:
                frames = self.ensure_tensor_format(frames)
            
            # Validate frame indices
            start_frame = max(0, min(start_frame, frames.shape[0]-1))
            end_frame = max(start_frame, min(end_frame, frames.shape[0]-1))
            
            # Calculate the number of frames in the effect
            original_duration = end_frame - start_frame + 1
            
            if speed == 0:
                return (frames,)
            
            # Calculate new duration based on speed
            if speed > 0:
                # Fast motion: reduce frames
                new_duration = int(original_duration / (1 + abs(speed)))
            else:
                # Slow motion: increase frames
                new_duration = int(original_duration * (1 + abs(speed)))
            
            # Generate frame indices for sampling
            if speed > 0:  # Fast motion
                # Create indices with linear interpolation
                indices = torch.linspace(start_frame, end_frame, new_duration)
                indices = indices.round().long()
            else:  # Slow motion
                # Duplicate frames for slow motion
                indices = []
                for i in range(start_frame, end_frame + 1):
                    repeats = int(1 + abs(speed))
                    indices.extend([i] * repeats)
                indices = torch.tensor(indices[:new_duration])
            
            # Create result tensor
            result_frames = []
            
            # Add frames before effect
            if start_frame > 0:
                result_frames.append(frames[:start_frame])
            
            # Apply effect (pure frame selection/duplication, no blending)
            effect_frames = frames[indices]
            result_frames.append(effect_frames)
            
            # Add remaining frames after the effect
            if end_frame < frames.shape[0] - 1:
                result_frames.append(frames[end_frame + 1:])
            
            # Concatenate all parts
            result = torch.cat(result_frames, dim=0)
            
            return (result,)
            
        except Exception as e:
            print(f"Error in apply_speed_effect: {str(e)}")
            raise e

