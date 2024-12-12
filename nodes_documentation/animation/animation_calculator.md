# DP Animation Calculator (5 Inputs)
<img src="https://github.com/user-attachments/assets/fa45806e-76f5-4d25-a0a5-8b6d494d9f90" alt="DP_Animation_Calculator_5Inputs" style="float: left; margin-right: 10px;"/>

## Description

A utility node for managing animations with image transitions and prompt scheduling. Helps create timing data for prompt schedules, fade masks, and IP adapter batches. Can generate timing data with or without image inputs.

## Inputs

**Required:**
- `Total_Frames`: Total number of frames to process (16-2000)
- `Image_01_startPoint` to `Image_05_startPoint`: Starting keyframes for each image/style × 5 (first is locked to 0)
- `Prompt_Image_01` to `Prompt_Image_05`: Prompt text for each keyframe × 5
- `Transition_Frames`: Duration of crossfade transitions (0-32, step 4)
- `fade_mask_01_Min/Max` to `fade_mask_03_Min/Max`: Min/Max weights for fade masks × 3 (0.0-1.0)

**Optional:**
- `Image_01_Input` to `Image_05_Input`: Source images for transitions × 5

## Outputs

- `Image_Batch_Output`: Combined image sequence with transitions
- `Text_Prompt_Timing`: Formatted string for prompt schedule
- `fade_mask_01_timing` to `fade_mask_03_timing`: Formatted strings for fade masks × 3
- `Check_Log`: Operation status and errors

## Notes

- Each keyframe must be greater than previous ones
- Transition consists of pre-transition, transition, and post-transition phases
- For img2video loops, set last keyframe = Total_Frames and last prompt/image = first
- Setting min > max in fade masks inverts the mask
- Images will crossfade based on Transition_Frames setting
- Can generate timing data without images for scheduling only
