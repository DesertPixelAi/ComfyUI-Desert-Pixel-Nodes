# DP Logo Animator
<img src="https://github.com/user-attachments/assets/d56d6536-ea7a-4819-98b6-cc5c4b19f5f3" alt="DP_Logo_Animator" style="float: left; margin-right: 10px;"/>

## Description
The DP Logo Animator node is designed for animating logos or adding effects using AnimateDiff. It creates a looping sequence based on the user-defined number of frames, with a minimum shrink size. The animation features a smooth scale effect where the logo shrinks and grows back, making it ideal for creating logo movement videos. The node works best with isolated logos on black or white backgrounds, but it also includes an auto-detect feature for background colors.

## Inputs
- **IMAGE** - `image` - The input logo image to be animated.
- **INT** - `frame_count` - The total number of frames in the animation sequence. Default is 48, with a range from 2 to 300.
- **FLOAT** - `min_scale` - The minimum scale size for the logo during the animation. Default is 0.2, with a range from 0.1 to 0.99.
- **STRING** - `background` - The background color for the animation. Options include "Auto", "Black", and "White".
- **INT** - `loop_count` - The number of times the animation should loop. Default is 1, with a range from 1 to 5.

## Outputs
- **IMAGE** - `result` - The output frames of the animated logo sequence.

## Example Usage
To use the DP Logo Animator node, connect a logo image to the `image` input. Set the `frame_count` to define how many frames the animation will have, and adjust the `min_scale` to control the minimum size of the logo during the animation. Choose the `background` color as needed, and specify the `loop_count` for how many times the animation should repeat. This node is particularly effective for creating dynamic logo animations suitable for video content.
