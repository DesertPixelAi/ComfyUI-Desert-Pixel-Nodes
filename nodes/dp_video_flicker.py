import torch

class DPVideoFlicker:
    def __init__(self):
        pass
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Load_video_frames": ("IMAGE",),
                "frames_to_export": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 10000,
                    "step": 1
                }),
                "Flicker_1_key_frame": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 10000,
                    "step": 1
                }),
                "Flicker_1_size": ("INT", {
                    "default": 3,
                    "min": 3,
                    "max": 10,
                    "step": 1
                }),
                "Flicker_1_speed": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 3,
                    "step": 1
                }),
                "Flicker_1_color": ("STRING", {
                    "default": "#000000"
                })
            },
            "optional": {
                "Flicker_2_key_frame": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 10000,
                    "step": 1
                }),
                "Flicker_2_size": ("INT", {
                    "default": 3,
                    "min": 3,
                    "max": 10,
                    "step": 1
                }),
                "Flicker_2_speed": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 3,
                    "step": 1
                }),
                "Flicker_2_color": ("STRING", {
                    "default": "#000000"
                }),
                "Flicker_3_key_frame": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 10000,
                    "step": 1
                }),
                "Flicker_3_size": ("INT", {
                    "default": 3,
                    "min": 3,
                    "max": 10,
                    "step": 1
                }),
                "Flicker_3_speed": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 3,
                    "step": 1
                }),
                "Flicker_3_color": ("STRING", {
                    "default": "#000000"
                })
            }
        }
    
    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("IMAGE", "process_info")
    FUNCTION = "execute"
    CATEGORY = "DP/animation"

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        try:
            rgb = tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
            return rgb
        except ValueError:
            return (0.0, 0.0, 0.0)

    def execute(self, Load_video_frames, frames_to_export,
                Flicker_1_key_frame, Flicker_1_size, Flicker_1_speed, Flicker_1_color,
                Flicker_2_key_frame=0, Flicker_2_size=3, Flicker_2_speed=1, Flicker_2_color="#000000",
                Flicker_3_key_frame=0, Flicker_3_size=3, Flicker_3_speed=1, Flicker_3_color="#000000"):
        
        total_frames = Load_video_frames.shape[0]
        if frames_to_export <= 0 or frames_to_export > total_frames:
            frames_to_export = total_frames

        process_info = "All flickers processed successfully"
        flicker_settings = []
        
        # Calculate cycle lengths and validate flickers
        if Flicker_1_key_frame > 0:
            flicker1_end = Flicker_1_key_frame + (Flicker_1_size * (Flicker_1_speed + 1))
            flicker_settings.append({
                'keyframe': Flicker_1_key_frame,
                'size': Flicker_1_size,
                'speed': Flicker_1_speed,
                'color': self.hex_to_rgb(Flicker_1_color),
                'end_frame': flicker1_end
            })
        
        if Flicker_2_key_frame > 0:
            flicker2_end = Flicker_2_key_frame + (Flicker_2_size * (Flicker_2_speed + 1))
            if Flicker_1_key_frame > 0 and Flicker_2_key_frame < flicker1_end:
                process_info = "Flicker 2 cancelled - overlaps with Flicker 1"
            else:
                flicker_settings.append({
                    'keyframe': Flicker_2_key_frame,
                    'size': Flicker_2_size,
                    'speed': Flicker_2_speed,
                    'color': self.hex_to_rgb(Flicker_2_color),
                    'end_frame': flicker2_end
                })
        
        if Flicker_3_key_frame > 0:
            flicker3_end = Flicker_3_key_frame + (Flicker_3_size * (Flicker_3_speed + 1))
            should_add = True
            
            for setting in flicker_settings:
                if Flicker_3_key_frame < setting['end_frame']:
                    process_info = "Flicker 3 cancelled - overlaps with previous flicker"
                    should_add = False
                    break
                    
            if should_add:
                flicker_settings.append({
                    'keyframe': Flicker_3_key_frame,
                    'size': Flicker_3_size,
                    'speed': Flicker_3_speed,
                    'color': self.hex_to_rgb(Flicker_3_color),
                    'end_frame': flicker3_end
                })

        output_frames = []
        current_frame = 0

        while current_frame < frames_to_export:
            in_flicker_sequence = False
            
            for settings in flicker_settings:
                sequence_length = settings['size'] * (settings['speed'] + 1)
                if settings['keyframe'] <= current_frame < settings['keyframe'] + sequence_length:
                    frame_offset = current_frame - settings['keyframe']
                    if frame_offset % (settings['speed'] + 1) == 0 and frame_offset < sequence_length:
                        flicker_frame = torch.stack([
                            torch.full_like(Load_video_frames[0, :, :, c], fill_value=settings['color'][c])
                            for c in range(3)
                        ], dim=-1)
                        output_frames.append(flicker_frame)
                        in_flicker_sequence = True
                        break
            
            if not in_flicker_sequence:
                output_frames.append(Load_video_frames[current_frame])
            
            current_frame += 1

        output_batch = torch.stack(output_frames)
        
        return (output_batch, process_info)

NODE_CLASS_MAPPINGS = {
    "DPVideoFlicker": DPVideoFlicker
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DPVideoFlicker": "DP Video Flicker"
}