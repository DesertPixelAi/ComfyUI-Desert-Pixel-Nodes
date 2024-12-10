import os
import torch

class DP_Video_Transition(object):
    @classmethod
    def load_modes_from_file(cls):
        return ["Normal Blend", "Dissolve", "Overlay", "Multiply", "Screen", "Soft Light"]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video1": ("IMAGE",),
                "video2": ("IMAGE",),
                "frames_to_blend": ("INT", {"default": 20, "min": 1, "max": 100, "step": 1}),
                "blend_mode": (cls.load_modes_from_file(),),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("blended_image",)
    FUNCTION = "video_transition"
    CATEGORY = "DP/animation"

    def blend_images(self, image1, image2, blend_factor, blend_mode):
        if blend_mode == "Normal Blend":
            blended_image = (1 - blend_factor) * image1 + blend_factor * image2
        elif blend_mode == "Multiply":
            blended_image = image1 * (1 - blend_factor) + image2 * blend_factor
        elif blend_mode == "Screen":
            blended_image = 1 - (1 - image1) * (1 - image2)
        elif blend_mode == "Overlay":
            blended_image = torch.where(image1 < 0.5, 2 * image1 * image2, 1 - 2 * (1 - image1) * (1 - image2))
        elif blend_mode == "Soft Light":
            blended_image = image1 * (1 - blend_factor) + (2 * image1 * image2) * blend_factor
        elif blend_mode == "Dissolve":
            blended_image = torch.where(torch.rand_like(image1) < blend_factor, image2, image1)
        else:
            blended_image = (1 - blend_factor) * image1 + blend_factor * image2
        return blended_image

    def video_transition(self, video1, video2, frames_to_blend, blend_mode):
        image1_frames = video1[-frames_to_blend:]
        image2_frames = video2[:frames_to_blend]
        blend_amounts = [i / (frames_to_blend - 1) for i in range(frames_to_blend)]
        
        blended_frames = []
        for i in range(frames_to_blend):
            blended_frame = self.blend_images(image1_frames[i], image2_frames[i], blend_amounts[i], blend_mode)
            blended_frames.append(blended_frame)

        output_video = torch.cat([video1[:-frames_to_blend], torch.stack(blended_frames), video2[frames_to_blend:]], dim=0)
        return (output_video,)

NODE_CLASS_MAPPINGS = {
    "DP_Video_Transition": DP_Video_Transition
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DP_Video_Transition": "DP Video Transition"
}