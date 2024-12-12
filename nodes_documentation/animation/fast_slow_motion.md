# DP Fast/Slow Motion
<img src="https://github.com/user-attachments/assets/b64a26ea-54ad-421a-a8bf-a573389fbae9" alt="DP_Fast_Slow_Motion" style="float: left; margin-right: 10px;"/>
## Description
The DP Fast/Slow Motion node allows users to manipulate the speed of a sequence of frames. By specifying a start frame, end frame, and a speed factor, users can create fast or slow motion effects on the selected frames. This node is particularly useful for video editing and animation, enabling dynamic visual effects based on user-defined parameters.

## Inputs
- **IMAGE** - `frames` - A batch of input frames as a tensor. This is the sequence of images that will be affected by the speed adjustment.
- **INT** - `start_frame` - The starting frame index for the speed effect.
- **INT** - `end_frame` - The ending frame index for the speed effect.
- **FLOAT** - `speed` - The speed factor for the motion effect. A positive value results in fast motion (reducing the number of frames), while a negative value results in slow motion (increasing the number of frames). Default is 0.0, with a range from -4.0 to 4.0.

## Outputs
- **IMAGE** - `result` - The output frames after applying the speed effect. The output will reflect the changes based on the specified start and end frames, as well as the speed factor.

## Example Usage
To use the DP Fast/Slow Motion node, connect a sequence of images to the `frames` input. Set the `start_frame` and `end_frame` to define the range of frames you want to affect. Adjust the `speed` input to create the desired motion effect. For instance, a speed of 2.0 will create a fast motion effect, while a speed of -2.0 will create a slow motion effect.
