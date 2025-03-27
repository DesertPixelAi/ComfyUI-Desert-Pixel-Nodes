# Standard library imports
import logging
from typing import Any, Dict, Optional, Tuple

import numpy as np

# Third-party imports
import torch

from .dp_video_transition import DP_Video_Transition


class DP_Image_Slide_Show:
    def __init__(self):
        # Initialize logging
        self.logger = logging.getLogger(__name__)

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Total_Frames": (
                    "INT",
                    {
                        "default": 96,
                        "min": 16,
                        "max": 2000,
                        "step": 1,
                        "display": "number",
                    },
                ),
                "Image_01_startPoint": (
                    "INT",
                    {"default": 0, "min": 0, "max": 0, "step": 1, "display": "number"},
                ),
                **{
                    f"Image_{i:02d}_startPoint": (
                        "INT",
                        {
                            "default": {2: 24, 3: 48, 4: 72, 5: 96}[i],
                            "min": 0,
                            "max": 1000,
                            "step": 1,
                            "display": "number",
                        },
                    )
                    for i in range(2, 6)
                },
                "Transition_Frames": (
                    "INT",
                    {"default": 8, "min": 0, "max": 32, "step": 4, "display": "number"},
                ),
                "blend_mode": (
                    [
                        "Normal Blend",
                        "Dissolve",
                        "Overlay",
                        "Multiply",
                        "Screen",
                        "Soft Light",
                    ],
                ),
            },
            "optional": {**{f"Image_{i:02d}_Input": ("IMAGE",) for i in range(1, 6)}},
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("Image_Batch_Output",)
    FUNCTION = "calc"
    CATEGORY = "DP/animation"

    def validate_transition_sizes(self, transition_size, pre_size, post_size):
        try:
            if pre_size + post_size > transition_size:
                # Instead of raising an error, adjust the sizes automatically
                adjusted_pre = transition_size // 2
                adjusted_post = transition_size - adjusted_pre
                self.logger.warning(
                    f"Adjusting transition sizes: Pre={adjusted_pre}, Post={adjusted_post} "
                    f"(original Pre={pre_size}, Post={post_size} exceeded Transition={transition_size})"
                )
                return adjusted_pre, adjusted_post
            return pre_size, post_size
        except Exception as e:
            self.logger.error(f"Error validating transition sizes: {str(e)}")
            return transition_size // 2, transition_size // 2

    def calc(self, **kwargs: Dict[str, Any]) -> Tuple[Optional[torch.Tensor]]:
        try:
            total_frames = kwargs["Total_Frames"]
            Image_Start_KeyFrames = [
                kwargs[f"Image_{i:02d}_startPoint"] for i in range(1, 6)
            ]
            images = [kwargs.get(f"Image_{i:02d}_Input") for i in range(1, 6)]

            # Automatically calculate pre and post transition sizes
            transition_frames = kwargs["Transition_Frames"]
            if transition_frames == 0:
                kwargs["Transition_Size"] = 0
                kwargs["Pre_Transition_Size"] = 0
                kwargs["Post_Transition_Size"] = 0
            else:
                kwargs["Transition_Size"] = transition_frames
                kwargs["Pre_Transition_Size"] = transition_frames // 2
                kwargs["Post_Transition_Size"] = transition_frames - (
                    transition_frames // 2
                )

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
                        if (
                            transition_frames > 0
                            and i < len(valid_keyframes) - 1
                            and frame_dict[valid_keyframes[i + 1]] < len(images)
                            and images[frame_dict[valid_keyframes[i + 1]]] is not None
                            and frame_count >= transition_frames
                        ):
                            next_image = images[frame_dict[valid_keyframes[i + 1]]]

                            # Convert next image to tensor if needed
                            if isinstance(next_image, np.ndarray):
                                next_image = torch.from_numpy(next_image)
                            if len(next_image.shape) == 3:
                                next_image = next_image.unsqueeze(0)

                            # Create transition frames
                            transition_size = kwargs["Transition_Size"]
                            transition_frames_tensor = next_image.repeat(
                                transition_size, 1, 1, 1
                            )

                            try:
                                # Blend the transition
                                transition_output = transition_handler.video_transition(
                                    repeated_image[-transition_size:],
                                    transition_frames_tensor,
                                    transition_size,
                                    kwargs["blend_mode"],
                                )[0]

                                # Replace the end of repeated_image with the transition
                                repeated_image = torch.cat(
                                    [
                                        repeated_image[:-transition_size],
                                        transition_output,
                                    ],
                                    dim=0,
                                )
                            except Exception as e:
                                self.logger.error(f"Transition error: {str(e)}")

                        if repeated_image is not None and repeated_image.shape[0] > 0:
                            Image_Batches.append(repeated_image)

                if Image_Batches:
                    Image_Output = torch.cat(Image_Batches, dim=0)

            except Exception as img_error:
                print(f"Image processing error: {str(img_error)}")
                return (None,)

            # Add additional error checking before returning
            if Image_Output is None:
                self.logger.warning("No valid image output was generated")
                # Return a black frame of size 512x512 as fallback
                return (torch.zeros((1, 3, 512, 512)),)

            return (Image_Output,)

        except Exception as e:
            self.logger.error(f"Error in DP_Image_Slide_Show: {str(e)}")
            # Return a black frame of size 512x512 as fallback
            return (torch.zeros((1, 3, 512, 512)),)
