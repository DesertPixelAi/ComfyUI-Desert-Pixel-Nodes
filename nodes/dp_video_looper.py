import torch

class DP_Video_Looper:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video": ("IMAGE",),
                "Total_Frames": ("INT", {"default": 100, "min": 1, "max": 9999, "step": 1}),
                "mode": (["StartOver_Mode", "BackAndForth"],),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("output_video",)
    FUNCTION = "loop_video"
    CATEGORY = "DP/animation"

    def loop_video(self, video, Total_Frames, mode):
        input_frames = video.shape[0]
        
        if input_frames >= Total_Frames:
            return (video[:Total_Frames],)

        if mode == "StartOver_Mode":
            # Calculate how many complete loops and remaining frames we need
            complete_loops = Total_Frames // input_frames
            remaining_frames = Total_Frames % input_frames
            
            # Create the output by repeating the video and adding remaining frames
            output_frames = []
            for _ in range(complete_loops):
                output_frames.append(video)
            if remaining_frames > 0:
                output_frames.append(video[:remaining_frames])
            
            return (torch.cat(output_frames, dim=0),)

        else:  # BackAndForth mode
            output_frames = []
            forward = True
            current_frame = 0
            
            while current_frame < Total_Frames:
                if forward:
                    for i in range(input_frames):
                        if current_frame >= Total_Frames:
                            break
                        output_frames.append(video[i].unsqueeze(0))
                        current_frame += 1
                    forward = False
                else:
                    for i in range(input_frames - 1, -1, -1):
                        if current_frame >= Total_Frames:
                            break
                        output_frames.append(video[i].unsqueeze(0))
                        current_frame += 1
                    forward = True
            
            return (torch.cat(output_frames, dim=0),)
