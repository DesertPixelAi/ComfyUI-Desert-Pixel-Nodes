# DP Video Flicker
<img src="https://github.com/user-attachments/assets/ffe900e0-2cac-445e-8b39-64e77d6f6081" alt="DP_Video_Flicker" style="float: left; margin-right: 10px;"/>
## Description
The DP Video Flicker node is designed to create flicker effects in video sequences. It allows users to specify up to three key frames where flicker effects will occur, with customizable sizes and speeds for each flicker. Users can also select colors for the flicker effects, making it suitable for transitions or as a standalone video effect.

## Inputs
- **IMAGE** - `Load_video_frames` - A batch of input video frames as a tensor. This is the sequence of frames that will be affected by the flicker effect.
- **INT** - `frames_to_export` - The total number of frames to export after applying the flicker effects. Default is 0, with a minimum of 0 and a maximum of 10,000.
- **INT** - `Flicker_1_key_frame` - The starting frame index for the first flicker effect.
- **INT** - `Flicker_1_size` - The size of the first flicker effect. Default is 3, with a minimum of 3 and a maximum of 10.
- **INT** - `Flicker_1_speed` - The speed of the first flicker effect. Default is 1, with a minimum of 1 and a maximum of 3.
- **STRING** - `Flicker_1_color` - The color for the first flicker effect in hex format (e.g., "#000000").
- **INT** - `Flicker_2_key_frame` (optional) - The starting frame index for the second flicker effect.
- **INT** - `Flicker_2_size` (optional) - The size of the second flicker effect. Default is 3, with a minimum of 3 and a maximum of 10.
- **INT** - `Flicker_2_speed` (optional) - The speed of the second flicker effect. Default is 1, with a minimum of 1 and a maximum of 3.
- **STRING** - `Flicker_2_color` (optional) - The color for the second flicker effect in hex format (e.g., "#000000").
- **INT** - `Flicker_3_key_frame` (optional) - The starting frame index for the third flicker effect.
- **INT** - `Flicker_3_size` (optional) - The size of the third flicker effect. Default is 3, with a minimum of 3 and a maximum of 10.
- **INT** - `Flicker_3_speed` (optional) - The speed of the third flicker effect. Default is 1, with a minimum of 1 and a maximum of 3.
- **STRING** - `Flicker_3_color` (optional) - The color for the third flicker effect in hex format (e.g., "#000000").

## Outputs
- **IMAGE** - `result` - The output frames after applying the flicker effects.
- **STRING** - `process_info` - Information about the processing status of the flicker effects.

## Example Usage
To use the DP Video Flicker node, connect a sequence of video frames to the `Load_video_frames` input. Specify the `frames_to_export` to define how many frames you want to output. Set the key frames, sizes, speeds, and colors for up to three flicker effects. This node is particularly effective for creating dynamic flicker effects in video transitions or as standalone video effects.
