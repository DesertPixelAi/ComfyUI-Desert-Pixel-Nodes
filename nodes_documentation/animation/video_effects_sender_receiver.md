# DP Video Effects (Sender/Receiver)
<img src="https://github.com/user-attachments/assets/d6fb3fb7-f58a-452c-9454-1d23092e5461" alt="DP_Video_Effect_Sender_reciver" style="float: left; margin-right: 10px;"/>

## Description

A paired system of nodes for applying effects to specific frames in a video sequence. The Sender extracts frames in a pattern for processing, while the Receiver places the processed frames back into their original positions.

## Sender Node

Extracts frames from video for processing, supporting up to three effect sequences.

### Inputs

**Required:**
- `Load_video_frames`: Input video frames
- `frames_to_export`: Number of frames to process (0 = all)
- `Effect_1_key_frame`: Starting frame for first effect sequence
- `Effect_1_size`: Number of frames to extract (3-10)
- `Effect_1_speed`: Frame interval (1-3)

**Optional:**
- `Effect_2_key_frame`, `Effect_2_size`, `Effect_2_speed`: Second effect sequence
- `Effect_3_key_frame`, `Effect_3_size`, `Effect_3_speed`: Third effect sequence

### Outputs

- `effect_frames`: Extracted frames for processing
- `all_frames`: Complete video sequence
- `frames_index`: Frame numbers for receiver reference
- `process_info`: Status and error messages

## Receiver Node

Reintegrates processed frames back into the original sequence.

### Inputs

- `all_frames`: Original video sequence
- `processed_frames`: Modified frames to insert
- `frames_index`: Frame numbers from sender

### Outputs

- `IMAGE`: Final video sequence with replaced frames
- `process_info`: Operation status and details

## Example Usage

Basic Frame Effect:
```
Sender:
- Effect_1_key_frame: 10
- Effect_1_size: 5
- Effect_1_speed: 1
→ Extracts frames 10, 12, 14, 16, 18

Receiver:
- Takes processed frames
- Replaces original frames at positions 10, 12, 14, 16, 18
```

Multiple Effects:
```
Sender:
- Effect_1: frames 10-18 (step 2)
- Effect_2: frames 30-38 (step 2)
→ Extracts two sequences for processing

Receiver:
- Replaces both sequences in order
```

Notes:
- Effects cannot overlap
- Higher speed means more frames between effects
- Size determines how many frames are affected
