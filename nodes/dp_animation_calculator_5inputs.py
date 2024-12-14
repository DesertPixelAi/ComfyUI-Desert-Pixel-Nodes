# Standard library imports
import logging
from typing import Dict, Any, Tuple, Optional

# Third-party imports
import torch
import numpy as np
from .dp_video_transition import DP_Video_Transition

class DP_Animation_Calculator_5Inputs:
    def __init__(self):
        # Initialize logging
        self.logger = logging.getLogger(__name__)
        
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Total_Frames": ("INT", {"default": 96, "min": 16, "max": 2000, "step": 1, "display": "number"}),
                "Image_01_startPoint": ("INT", {
                    "default": 0,
                    "min": 0, "max": 0, "step": 1, "display": "number"
                }),
                **{f"Image_{i:02d}_startPoint": ("INT", {
                    "default": {2: 24, 3: 48, 4: 72, 5: 96}[i],
                    "min": 0, "max": 1000, "step": 1, "display": "number"
                }) for i in range(2, 6)},
                **{f"Prompt_Image_{i:02d}": ("STRING", {"default": f"prompt {i:02d}", "multiline": False}) for i in range(1, 6)},
                "Transition_Frames": ("INT", {"default": 8, "min": 0, "max": 32, "step": 4, "display": "number"}),
                "fade_mask_01_Min": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.1}),
                "fade_mask_01_Max": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.1}),
                "fade_mask_02_Min": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.1}),
                "fade_mask_02_Max": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.1}),
                "fade_mask_03_Min": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.1}),
                "fade_mask_03_Max": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.1})
            },
            "optional": {
                **{f"Image_{i:02d}_Input": ("IMAGE",) for i in range(1, 6)}
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING", "STRING", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("Image_Batch_Output", "Text_Prompt_Timing", "fade_mask_01_timing", "fade_mask_02_timing", "fade_mask_03_timing", "Check_Log",)
    FUNCTION = "calc"
    CATEGORY = "DP/animation"

    def validate_timing_string(self, timing_string: str) -> str:
        """
        Validate the timing string format and order.
        
        Args:
            timing_string: String containing frame timings
            
        Returns:
            str: Error message if validation fails, empty string if successful
        """
        if not timing_string.strip():
            return "Error: Empty timing string"
        
        try:
            frames = []
            for line in timing_string.split('\n'):
                if not line.strip():
                    continue
                if ':' not in line:
                    return f"Error: Invalid format in line '{line}'"
                if line.startswith('"'):
                    frame = int(line.split(':')[0].strip('"'))
                else:
                    frame = int(line.split(':')[0])
                frames.append(frame)
            
            for i in range(len(frames)-1):
                if frames[i] >= frames[i+1]:
                    return f"Error: Frame {frames[i]} is followed by frame {frames[i+1]}, frames must be in ascending order"
            
            return ""
        except ValueError as e:
            return f"Error: Invalid frame number format - {str(e)}"

    def validate_transition_sizes(self, transition_size, pre_size, post_size):
        if pre_size + post_size > transition_size:
            raise ValueError(
                f"Pre ({pre_size}) + Post ({post_size}) transition sizes cannot exceed "
                f"total Transition size ({transition_size})"
            )

    def calc(self, **kwargs: Dict[str, Any]) -> Tuple[Optional[torch.Tensor], str, str, str, str, str]:
        try:
            total_frames = kwargs['Total_Frames']
            Image_Start_KeyFrames = [kwargs[f'Image_{i:02d}_startPoint'] for i in range(1, 6)]
            images = [kwargs.get(f'Image_{i:02d}_Input') for i in range(1, 6)]
            
            # Automatically calculate transition sizes
            transition_frames = kwargs['Transition_Frames']
            if transition_frames == 0:
                kwargs['Transition_Size'] = 0
                kwargs['Pre_Transition_Size'] = 0
                kwargs['Post_Transition_Size'] = 0
            else:
                kwargs['Transition_Size'] = transition_frames
                kwargs['Pre_Transition_Size'] = transition_frames // 2
                kwargs['Post_Transition_Size'] = transition_frames - (transition_frames // 2)
            
            # Create a dictionary to handle duplicate frames, keeping only the first occurrence
            frame_dict = {}
            for i, frame in enumerate(Image_Start_KeyFrames):
                if frame <= total_frames and frame not in frame_dict:
                    frame_dict[frame] = i
            
            # Convert back to sorted list of unique frames
            valid_keyframes = sorted(frame_dict.keys())
            if not valid_keyframes:
                valid_keyframes = [0]
            
            # Image handling
            Image_Output = None
            try:
                Image_Batches = []
                transition_handler = DP_Video_Transition()
                
                for i, start_frame in enumerate(valid_keyframes):
                    if i < len(valid_keyframes) - 1:
                        end_frame = valid_keyframes[i + 1]
                    else:
                        end_frame = total_frames
                    
                    if start_frame >= total_frames:
                        continue
                        
                    image_index = frame_dict[start_frame]
                    current_image = images[image_index]
                    
                    if current_image is None:
                        continue
                        
                    # Convert to tensor if needed
                    if isinstance(current_image, np.ndarray):
                        current_image = torch.from_numpy(current_image)
                    if len(current_image.shape) == 3:
                        current_image = current_image.unsqueeze(0)
                    
                    frame_count = max(0, min(end_frame, total_frames) - start_frame)
                    
                    if frame_count > 0:
                        # Create batch of repeated frames
                        repeated_image = current_image.repeat(frame_count, 1, 1, 1)
                        
                        # Only create transition if we have enough frames and a valid next image
                        if (transition_frames > 0 and 
                            i < len(valid_keyframes) - 1 and 
                            frame_dict[valid_keyframes[i + 1]] < len(images) and 
                            images[frame_dict[valid_keyframes[i + 1]]] is not None and
                            frame_count >= transition_frames):
                            
                            next_image = images[frame_dict[valid_keyframes[i + 1]]]
                            
                            # Convert next image to tensor if needed
                            if isinstance(next_image, np.ndarray):
                                next_image = torch.from_numpy(next_image)
                            if len(next_image.shape) == 3:
                                next_image = next_image.unsqueeze(0)
                            
                            try:
                                # Create transition frames
                                transition_size = kwargs['Transition_Size']
                                transition_frames_tensor = next_image.repeat(transition_size, 1, 1, 1)
                                
                                # Blend the transition
                                transition_output = transition_handler.video_transition(
                                    repeated_image[-transition_size:],
                                    transition_frames_tensor,
                                    transition_size,
                                    "Normal Blend"
                                )[0]
                                
                                # Replace the end of repeated_image with the transition
                                repeated_image = torch.cat([
                                    repeated_image[:-transition_size],
                                    transition_output
                                ], dim=0)
                            except Exception as e:
                                self.logger.error(f"Transition error: {str(e)}")
                        
                        if repeated_image is not None and repeated_image.shape[0] > 0:
                            Image_Batches.append(repeated_image)

                if Image_Batches:
                    Image_Output = torch.cat(Image_Batches, dim=0)
            
            except Exception as img_error:
                print(f"Image processing error: {str(img_error)}")
                return (None, "", "", "", "", str(img_error))
            
            # Generate text outputs with proper formatting
            timing_entries = []
            for i, frame in enumerate(valid_keyframes):
                if frame == total_frames:  # Skip adding frame if it equals total_frames
                    continue
                i = frame_dict[frame] + 1  # Get original index (+1 for 1-based indexing)
                text = kwargs.get(f'Prompt_Image_{i:02d}', f'prompt {i:02d}')
                text = text.replace('"', '\\"')
                timing_entries.append(f'"{frame}":"{text}",')  # Always add comma

            # Ensure the last keyframe is total_frames - 1
            if valid_keyframes[-1] != total_frames - 1:
                last_index = frame_dict[valid_keyframes[-1]] + 1
                text = kwargs.get(f'Prompt_Image_{last_index:02d}', f'prompt {last_index:02d}')
                text = text.replace('"', '\\"')
                timing_entries.append(f'"{total_frames - 1}":"{text}"')  # No comma for the last entry
            else:
                # If we already have entries, remove the comma from the last one
                if timing_entries:
                    timing_entries[-1] = timing_entries[-1].rstrip(',')

            Text_output_01_Prompt = "\n".join(timing_entries)

            def generate_timing_string(min_value, max_value, invert=False):
                timing_entries = []
                pre_size = kwargs['Pre_Transition_Size']
                post_size = kwargs['Post_Transition_Size']
                
                # Determine if we need to swap min and max
                should_swap = min_value > max_value
                actual_min = max_value if should_swap else min_value
                actual_max = min_value if should_swap else max_value
                
                # Invert logic is now combined with the swap logic
                final_invert = invert != should_swap
                
                # Set initial value
                first_val = actual_min if final_invert else actual_max
                timing_entries.append(f"{valid_keyframes[0]}:({first_val:.1f}),")
                
                for frame in valid_keyframes[1:]:
                    if frame >= total_frames:
                        continue
                        
                    # Pre-transition point
                    pre_frame = frame - pre_size
                    if pre_frame > 0:
                        val = actual_min if final_invert else actual_max
                        timing_entries.append(f"{pre_frame}:({val:.1f}),")
                    
                    # Keyframe point
                    val = actual_max if final_invert else actual_min
                    timing_entries.append(f"{frame}:({val:.1f}),")
                    
                    # Post-transition point
                    post_frame = frame + post_size
                    if post_frame < total_frames:
                        val = actual_min if final_invert else actual_max
                        timing_entries.append(f"{post_frame}:({val:.1f}),")
                
                # Add final frame if needed
                if valid_keyframes[-1] != total_frames - 1:
                    val = actual_min if final_invert else actual_max
                    timing_entries.append(f"{total_frames - 1}:({val:.1f})")
                
                return "\n".join(timing_entries)

            Text_output_02_IP = generate_timing_string(kwargs['fade_mask_01_Min'], kwargs['fade_mask_01_Max'])
            Text_output_03_CN01 = generate_timing_string(kwargs['fade_mask_02_Min'], kwargs['fade_mask_02_Max'])
            Text_output_04_CN02 = generate_timing_string(kwargs['fade_mask_03_Min'], kwargs['fade_mask_03_Max'])

            validation_message = "All keyframes are in correct order"

            return (Image_Output, Text_output_01_Prompt, Text_output_02_IP, Text_output_03_CN01, Text_output_04_CN02, validation_message)
            
        except Exception as e:
            error_message = str(e)
            print(f"Error in DP_Animation_Calculator_5Inputs: {error_message}")
            return (None, "", "", "", "", error_message)

NODE_CLASS_MAPPINGS = {
    "DP_Animation_Calculator_5Inputs": DP_Animation_Calculator_5Inputs
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DP_Animation_Calculator_5Inputs": "DP Animation Calculator (5 Inputs)"
}