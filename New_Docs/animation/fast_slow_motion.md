# DP Fast/Slow Motion

<img src="https://github.com/user-attachments/assets/fast_slow_motion.png" alt="DP_Fast_Slow_Motion" style="float: left; margin-right: 10px;"/>

## Description

The Fast/Slow Motion node allows you to modify the playback speed of image sequences by duplicating or skipping frames. This node is particularly useful for creating slow-motion effects, fast-forward sequences, or adjusting animation timing without regenerating frames.

## Inputs

### Required:
- **images**: (`IMAGE`) - Input image sequence to modify
- **mode**: (`COMBO`, default: "Slow Motion") - Select between modes:
  - "Slow Motion" - Duplicates frames to slow down animation
  - "Fast Motion" - Skips frames to speed up animation
- **frames_to_add**: (`INT`, default: 1, range: 0-7) - In Slow Motion mode:
  - Number of duplicate frames to add between each original frame
  - Example: 1 = doubles duration, 2 = triples duration
- **frames_to_skip**: (`INT`, default: 1, range: 1-7) - In Fast Motion mode:
  - Number of frames to skip between kept frames
  - Example: 1 = half duration, 2 = one-third duration

## Outputs

- **IMAGE**: Modified image sequence with adjusted playback speed
- **frame_count**: Total number of frames in output sequence

## Usage Examples

### Slow Motion Effect
Input: 24 frames
Mode: "Slow Motion"
frames_to_add: 2
Result: 72 frames (each original frame repeated 3 times)

### Fast Motion Effect
Input: 60 frames
Mode: "Fast Motion"
frames_to_skip: 2
Result: 20 frames (every third frame kept)

## Notes

- Slow Motion increases file size and memory usage
- Fast Motion reduces frame count but may cause less smooth motion
- No interpolation is performed; frames are simply duplicated or skipped
- Original frame order is maintained
- Works with any image sequence input (animations, video frames, etc.)
