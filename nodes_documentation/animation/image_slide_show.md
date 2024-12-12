# DP Image Slide Show
![DP_Image_Slide_Show](https://github.com/user-attachments/assets/c3001c1e-4d57-46fd-9d0f-4a62109a46dd)
## Description
Creates image sequences with blend mode transitions, perfect for GIFs and videos. This node allows for smooth transitions between images while applying various blend modes.

## Inputs
- **5 optional image inputs** - If connected, will use to create an image batch sized to Total_Frames for the output, with image crossfade transitions controlled by the Transition_Frames input.
- **INT - Total_Frames** - Defines the total number of frames to process.
- **5 INT - Image_startPoint 01-05** - The start key frame for each image/style. The first image's start point is set to 0, and each key frame must be larger than the previous ones.
- **INT - Transition_Frames** - The number of frames for the full transition between images. This input controls the pre-transition, transition, and post-transition sizes, allowing for smooth transitions between images/styles.
- **STRING - blend_mode** - Select from various blend modes: Normal Blend, Dissolve, Overlay, Multiply, Screen, Soft Light.

## Outputs
- **IMAGE - Image_Batch_Output** - export image batch sized to Total_Frames, with each image spanning its keyframe duration and crossfade transitions between 

## Example Usage
To create a GIF or video using the DP Image Slide Show node, connect your images to the input slots, set the Total_Frames, and define the start points for each image. Adjust the Transition_Frames to control the duration of transitions and select your desired blend mode for the output.
