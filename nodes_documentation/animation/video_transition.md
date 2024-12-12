# DP Video Transition
<img src="https://github.com/user-attachments/assets/67234ca8-2496-405b-a1a7-3211fb225887" alt="DP_Video_Transition" style="float: left; margin-right: 10px;"/>

## Description

The DP Video Transition node is designed to create smooth transitions between two video sequences. It takes the last frames from video 1 and the last frames from video 2, combining them with a smooth transition based on user-defined parameters. The node also supports various blend modes for additional style effects, making it ideal for creating dynamic video transitions.

## Inputs
- **IMAGE** - `video_1_frames` - The frames from the first video sequence to transition from.
- **IMAGE** - `video_2_frames` - The frames from the second video sequence to transition to.
- **INT** - `transition_frames` - The number of frames over which the transition will occur. Default is 30, with a minimum of 1 and a maximum of 1000.
- **STRING** - `blend_mode` - The blend mode to apply during the transition. Options include "Normal", "Multiply", "Screen", "Overlay", etc.

## Outputs
- **IMAGE** - `result` - The output frames after applying the transition effect.

## Example Usage
To use the DP Video Transition node, connect the frames from the first video to the `video_1_frames` input and the frames from the second video to the `video_2_frames` input. Set the `transition_frames` to define how long the transition should last, and choose a `blend_mode` to apply during the transition. This node is particularly effective for creating seamless transitions between video clips.
