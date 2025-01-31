# DP Animation Calculator (5/10 Inputs)

<img src="https://github.com/user-attachments/assets/fa45806e-76f5-4d25-a0a5-8b6d494d9f90" alt="DP_Animation_Calculator" style="float: left; margin-right: 10px;"/>

## Description

The Animation Calculator nodes (available in 5-input and 10-input variants) are powerful utilities for managing complex animations with image transitions and prompt scheduling. These nodes help create timing data for prompt schedules, fade masks, and IP adapter batches, with the ability to generate timing data with or without image inputs. The main difference between the variants is the number of keyframes they can handle (5 vs 10 inputs).

## Inputs

### Required:
- **Total_Frames**: (`INT`, default: 96) - Total number of frames to process (16-2000)
- **Image_XX_startPoint**: (`INT`) - Starting keyframes for each image/style
  - First point (01) is locked to 0
  - For 5-inputs: 01-05 (defaults: 0, 24, 48, 72, 96)
  - For 10-inputs: 01-10 (defaults: 0, 24, 48, 72, 96, 120, 144, 168, 192, 216)
- **Prompt_Image_XX**: (`STRING`) - Prompt text for each keyframe (01-05 or 01-10)
- **Transition_Frames**: (`INT`, default: 8) - Duration of crossfade transitions (0-32, step 4)
- **fade_mask_XX_Min/Max**: (`FLOAT`, default: 0.0/1.0) - Min/Max weights for fade masks (3 pairs, range 0.0-1.0)

### Optional:
- **Image_XX_Input**: (`IMAGE`) - Source images for transitions (5 or 10 inputs)

## Outputs

- **Image_Batch_Output**: (`IMAGE`) - Combined image sequence with transitions
- **Text_Prompt_Timing**: (`STRING`) - Formatted string for prompt schedule
- **fade_mask_01_timing**: (`STRING`) - Timing string for first fade mask
- **fade_mask_02_timing**: (`STRING`) - Timing string for second fade mask
- **fade_mask_03_timing**: (`STRING`) - Timing string for third fade mask
- **Check_Log**: (`STRING`) - Operation status and error messages

## Usage Examples

### Basic Animation Setup
Example timing output format:
"0":"first prompt",
"24":"second prompt",
"48":"third prompt",
"95":"first prompt"  # For loops, last frame uses first prompt

### Fade Mask Timing
Example fade mask timing:
0:(1.0),
20:(1.0),
24:(0.0),
32:(1.0)

## Notes

- **Keyframe Order**: Each keyframe must be greater than previous ones
- **Transitions**: 
  - Consists of pre-transition, transition, and post-transition phases
  - Pre-transition size = Transition_Frames ÷ 2
  - Post-transition size = Transition_Frames - Pre-transition size
- **Looping**: For seamless loops, set last keyframe = Total_Frames - 1 and use same prompt/image as first
- **Fade Masks**: 
  - Setting min > max inverts the mask
  - Three independent fade masks allow complex animations
- **Image Processing**:
  - Images will crossfade based on Transition_Frames setting
  - Can generate timing data without images for scheduling only
- **Error Handling**: 
  - Validates frame order and timing string format
  - Returns error messages in Check_Log output

## Advanced Features

- **Automatic Transition Sizing**: Calculates optimal pre/post transition sizes
- **Duplicate Frame Handling**: Automatically handles duplicate keyframes, keeping first occurrence
- **Tensor Conversion**: Automatically converts between numpy arrays and torch tensors as needed
- **Empty Frame Handling**: Gracefully handles missing or None image inputs
