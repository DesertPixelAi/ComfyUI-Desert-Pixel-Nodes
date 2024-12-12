# DP Animation Calculator (5 Inputs)
![DP_Animation_Calculator_5Inputs_detailed](https://github.com/user-attachments/assets/fa45806e-76f5-4d25-a0a5-8b6d494d9f90)
## Description
animation calculator helper for switch between images/styles with img2video & video2video with animatediff, helps to create timing data for prompt schedule, fade masks, and ip adapter batch.
each image has keyFrame start point and a prompt text, but you can use it also without image input to generate schedule prompt or fade masks timing.

## Inputs
- 5 optional image inputs - if connected will use to create an image batch in the size of Total_Frames for the ipadapter batch, with image crossfade transition controlled by the Transition_frames input.
- INT - Total_Frames - how many frames will be processed.
- 5 INT - Image_startPoint 01-05 - the start key frame for each image/style, image_01_startPoint is set to 0. notice that each keyFrame has to be bigger than the previous ones.
- 5 STRING Prompt_Image 01-05 - the prompts for each Image/keyframe.
- INT - Transition_Frames - the number in frames of the full transition between image to image, effects only the 3 fade_masks_timing and the image batch output (not affecting the prompt timing). This input controls the pre-transition, transition, and post-transition sizes, allowing for smooth transitions between images/styles.
- 6*FLOAT - fade_mask_Min fade_mask_Max 01-03 - the minimum and maximum weight of each fade mask, to invert the mask set the min bigger than the max.

## Transition Details
- **Pre-Transition Size**: This refers to the number of frames allocated before the transition begins. It allows for a gradual introduction of the new image/style.
- **Transition Size**: This is the duration of the actual transition between images/styles. It defines how long the crossfade effect will last.
- **Post-Transition Size**: This is the number of frames after the transition where the new image/style is fully visible. It ensures that the new image/style is established before moving on to the next transition.

## Outputs
- Image - Image_Batch_Output - if images connected to the inputs, it will export image batch in the size of Total_Frames, each image will be exported*its keyframes duration, with a crossfade between every image in the size of Transition frames.
- String - Text_Prompt_Timing - formatted string for prompt schedule node with all the prompts and their timing.
- 3*String - fade_mask_timing 01-03 - formatted string for fade mask advanced node.

*for img2video loop, set the last Image_startPoint same as Total_Frames, and the last PromptImage+Image same as the first.
