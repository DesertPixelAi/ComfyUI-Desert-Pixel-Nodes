import torch

class DPVideoEffectSender:
    def __init__(self):
        pass
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Load_video_frames": ("IMAGE",),
                "Effect_1_key_frame": ("INT", {
                    "default": 24,
                    "min": 1,
                    "max": 10000,
                    "step": 1
                }),
                "Effect_1_size": ("INT", {
                    "default": 3,
                    "min": 3,
                    "max": 10,
                    "step": 1
                }),
                "Effect_1_speed": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 3,
                    "step": 1
                })
            },
            "optional": {
                "Effect_2_key_frame": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 10000,
                    "step": 1
                }),
                "Effect_2_size": ("INT", {
                    "default": 3,
                    "min": 3,
                    "max": 10,
                    "step": 1
                }),
                "Effect_2_speed": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 3,
                    "step": 1
                }),
                "Effect_3_key_frame": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 10000,
                    "step": 1
                }),
                "Effect_3_size": ("INT", {
                    "default": 3,
                    "min": 3,
                    "max": 10,
                    "step": 1
                }),
                "Effect_3_speed": ("INT", {
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

    def execute(self, Load_video_frames, 
                Effect_1_key_frame, Effect_1_size, Effect_1_speed,
                Effect_2_key_frame=0, Effect_2_size=3, Effect_2_speed=1,
                Effect_3_key_frame=0, Effect_3_size=3, Effect_3_speed=1):
        
        total_frames = Load_video_frames.shape[0]
        frames_to_export = total_frames

        if frames_to_export <= 0 or frames_to_export > total_frames:
            frames_to_export = total_frames

        process_info = "All effects processed successfully"
        effect_settings = []
        
        # Add error handling for key frames
        if Effect_1_key_frame < 1:
            process_info = "Error: Effect 1 key frame must be greater than 0"
            return (Load_video_frames, Load_video_frames[0:0], "", process_info)
        
        # Calculate cycle lengths and validate effects
        if Effect_1_key_frame > 0:
            effect1_end = Effect_1_key_frame + (Effect_1_size * (Effect_1_speed + 1))
            effect_settings.append({
                'keyframe': Effect_1_key_frame,
                'size': Effect_1_size,
                'speed': Effect_1_speed,
                'end_frame': effect1_end
            })
        
        if Effect_2_key_frame > 0:
            effect2_end = Effect_2_key_frame + (Effect_2_size * (Effect_2_speed + 1))
            if Effect_1_key_frame > 0 and Effect_2_key_frame < effect1_end:
                process_info = "Effect 2 cancelled - overlaps with Effect 1"
            else:
                effect_settings.append({
                    'keyframe': Effect_2_key_frame,
                    'size': Effect_2_size,
                    'speed': Effect_2_speed,
                    'end_frame': effect2_end
                })
        
        if Effect_3_key_frame > 0:
            effect3_end = Effect_3_key_frame + (Effect_3_size * (Effect_3_speed + 1))
            should_add = True
            
            for setting in effect_settings:
                if Effect_3_key_frame < setting['end_frame']:
                    process_info = "Effect 3 cancelled - overlaps with previous effect"
                    should_add = False
                    break
                    
            if should_add:
                effect_settings.append({
                    'keyframe': Effect_3_key_frame,
                    'size': Effect_3_size,
                    'speed': Effect_3_speed,
                    'end_frame': effect3_end
                })

        # Create list of frames that need effects
        effect_frame_indices = []
        for settings in effect_settings:
            sequence_length = settings['size'] * (settings['speed'] + 1)
            current_frame = settings['keyframe']
            
            for _ in range(settings['size']):
                if current_frame < frames_to_export:
                    effect_frame_indices.append(current_frame)
                current_frame += settings['speed'] + 1

        # Sort frame indices
        effect_frame_indices.sort()
        
        # Convert frame indices to string
        frames_index = ", ".join(map(str, effect_frame_indices))
        
        # Extract frames that need effects
        effect_frames = torch.stack([Load_video_frames[i] for i in effect_frame_indices]) if effect_frame_indices else Load_video_frames[0:0]  # Empty tensor if no effects
        
        # Extract all frames up to frames_to_export
        all_frames = Load_video_frames[:frames_to_export]
        
        return (all_frames, effect_frames, frames_index, process_info)


class DPVideoEffectReceiver:
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
            # Parse the frame indices
            frame_indices = [int(x.strip()) for x in frames_index.split(",") if x.strip()]
            
            # Add debug info
            process_info = f"Frames to replace: {frame_indices}\n"
            process_info += f"Number of processed frames: {processed_frames.shape[0]}\n"
            process_info += f"Total frames in sequence: {all_frames.shape[0]}"
            
            if len(frame_indices) != processed_frames.shape[0]:
                return (all_frames, f"Error: Number of processed frames ({processed_frames.shape[0]}) doesn't match number of frame indices ({len(frame_indices)})", all_frames)
            
            # Create output frames
            output_frames = all_frames.clone()
            
            # Replace frames with processed ones
            for idx, frame_num in enumerate(frame_indices):
                if frame_num < output_frames.shape[0]:
                    output_frames[frame_num] = processed_frames[idx]
                    process_info += f"\nReplaced frame {frame_num} with processed frame {idx}"
            
            return (output_frames, process_info, all_frames)
            
        except ValueError as e:
            return (all_frames, f"Error parsing frame indices: {str(e)}", all_frames)
        except Exception as e:
            return (all_frames, f"Error processing frames: {str(e)}", all_frames)


NODE_CLASS_MAPPINGS = {
    "DPVideoEffectSender": DPVideoEffectSender,
    "DPVideoEffectReceiver": DPVideoEffectReceiver
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DPVideoEffectSender": "DP Video Effect Sender",
    "DPVideoEffectReceiver": "DP Video Effect Receiver"
}