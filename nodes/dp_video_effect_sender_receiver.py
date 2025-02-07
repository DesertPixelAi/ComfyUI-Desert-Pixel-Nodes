import torch

class DP_Video_Effect_Sender:
    def __init__(self):
        pass
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Load_video_frames": ("IMAGE",),
                "Effect_key_frame": ("INT", {
                    "default": 24,
                    "min": 1,
                    "max": 10000,
                    "step": 1
                }),
                "Effect_steps": ("INT", {
                    "default": 3,
                    "min": 3,
                    "max": 10,
                    "step": 1
                }),
                "Effect_Distance": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 3,
                    "step": 1
                }),
                "Effect_Length": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 3,
                    "step": 1
                })
            }
        }
    
    RETURN_TYPES = ("IMAGE", "IMAGE", "STRING", "STRING")
    RETURN_NAMES = ("all_frames", "effect_frames", "frames_index", "process_info")
    FUNCTION = "execute"
    CATEGORY = "DP/animation"

    def execute(self, Load_video_frames, Effect_key_frame, Effect_steps, Effect_Distance, Effect_Length):
        # Validate input
        if Load_video_frames is None or Load_video_frames.shape[0] == 0:
            return (Load_video_frames, Load_video_frames[0:0], "", "Error: No input frames provided")
            
        total_frames = Load_video_frames.shape[0]
        
        # Validate key frame is within video length
        if Effect_key_frame >= total_frames:
            return (Load_video_frames, Load_video_frames[0:0], "", f"Error: Effect key frame {Effect_key_frame} exceeds video length {total_frames}")
        
        frames_to_export = total_frames
        process_info = "Effect processed successfully"
        
        # Add error handling for key frame
        if Effect_key_frame < 1:
            process_info = "Error: Effect key frame must be greater than 0"
            return (Load_video_frames, Load_video_frames[0:0], "", process_info)
        
        # Calculate effect frames
        effect_frame_indices = []
        current_frame = Effect_key_frame
        
        # For each step
        for _ in range(Effect_steps):
            # Add consecutive frames based on Effect_Length
            for offset in range(Effect_Length):
                if current_frame + offset < frames_to_export:
                    effect_frame_indices.append(current_frame + offset)
            
            # Move to next position based on Distance and Length
            current_frame += Effect_Length + Effect_Distance

        # Sort frame indices
        effect_frame_indices.sort()
        
        # Convert frame indices to string
        frames_index = ", ".join(map(str, effect_frame_indices))
        
        # Extract frames that need effects
        effect_frames = torch.stack([Load_video_frames[i] for i in effect_frame_indices]) if effect_frame_indices else Load_video_frames[0:0]  # Empty tensor if no effects
        
        # Extract all frames up to frames_to_export
        all_frames = Load_video_frames[:frames_to_export]
        
        # Add debug info to process_info
        process_info = f"Effect frames: {frames_index}\n"
        process_info += f"Steps: {Effect_steps}, Distance: {Effect_Distance}, Length: {Effect_Length}"
        
        return (all_frames, effect_frames, frames_index, process_info)


class DP_Video_Effect_Receiver:
    def __init__(self):
        pass
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "all_frames": ("IMAGE",),
                "processed_frames": ("IMAGE",),
                "frames_index": ("STRING", {
                    "multiline": False
                })
            }
        }
    
    RETURN_TYPES = ("IMAGE", "STRING", "IMAGE")
    RETURN_NAMES = ("IMAGE", "process_info", "all_frames")
    FUNCTION = "execute"
    CATEGORY = "DP/animation"

    def execute(self, all_frames, processed_frames, frames_index):
        try:
            # Validate inputs
            if not frames_index.strip():
                return (all_frames, "No frames to process", all_frames)
                
            if processed_frames is None or processed_frames.shape[0] == 0:
                return (all_frames, "No processed frames provided", all_frames)
            
            # Check resolution matching
            original_height, original_width = all_frames.shape[1:3]
            processed_height, processed_width = processed_frames.shape[1:3]
            
            if original_height != processed_height or original_width != processed_width:
                return (all_frames, 
                       f"Error: Resolution mismatch. Original frames: {original_width}x{original_height}, " +
                       f"Processed frames: {processed_width}x{processed_height}", 
                       all_frames)
                
            # Parse the frame indices and ensure they are integers
            try:
                frame_indices = [int(x.strip()) for x in frames_index.split(",") if x.strip()]
            except ValueError:
                return (all_frames, f"Error: Invalid frame indices in '{frames_index}'", all_frames)
            
            # Rest of the validation
            if not frame_indices:
                return (all_frames, "Error: No valid frame indices found", all_frames)
            
            if max(frame_indices) >= all_frames.shape[0]:
                return (all_frames, f"Error: Frame index {max(frame_indices)} exceeds video length {all_frames.shape[0]}", all_frames)
            
            if len(frame_indices) != processed_frames.shape[0]:
                return (all_frames, f"Error: Number of processed frames ({processed_frames.shape[0]}) doesn't match number of frame indices ({len(frame_indices)})", all_frames)
            
            # Create a new tensor for output to avoid modifying the input
            output_frames = all_frames.clone()
            
            # Replace frames with processed ones
            for idx, frame_num in enumerate(frame_indices):
                output_frames[frame_num] = processed_frames[idx].clone()
            
            # Add debug info
            process_info = f"Successfully replaced frames at indices: {frame_indices}\n"
            process_info += f"Resolution: {original_width}x{original_height}\n"
            process_info += f"Number of processed frames: {processed_frames.shape[0]}\n"
            process_info += f"Total frames in sequence: {all_frames.shape[0]}"
            
            return (output_frames, process_info, all_frames)
            
        except Exception as e:
            return (all_frames, f"Error processing frames: {str(e)}", all_frames)

