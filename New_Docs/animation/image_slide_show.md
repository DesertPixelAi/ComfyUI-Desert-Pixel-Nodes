# DP Image Slide Show

<img src="https://github.com/user-attachments/assets/image_slide_show.png" alt="DP_Image_Slide_Show" style="float: left; margin-right: 10px;"/>

## Description

The Image Slide Show node creates smooth transitions between a sequence of images, perfect for creating video slideshows or animated presentations. It handles image transitions with customizable durations and effects, making it ideal for creating dynamic visual presentations from static images.

## Inputs

### Required:
- **images**: (`IMAGE`) - Input image sequence to create slideshow from
- **frames_per_image**: (`INT`, default: 30, range: 1-120) - How long each image is displayed
- **transition_frames**: (`INT`, default: 10, range: 0-30) - Duration of transition effect between images
- **transition_type**: (`COMBO`, default: "Crossfade") - Type of transition effect:
  - "Crossfade" - Smooth opacity blend
  - "Fade to Black" - Fade through black
  - "Fade to White" - Fade through white

### Optional:
- **loop_slideshow**: (`BOOLEAN`, default: True) - Whether to loop back to first image
- **reverse_order**: (`BOOLEAN`, default: False) - Play slideshow in reverse

## Outputs

- **IMAGE**: Final image sequence with transitions
- **frame_count**: Total number of frames in output sequence

## Usage Examples

### Basic Slideshow
Input: 5 images
frames_per_image: 30
transition_frames: 10
Result: 190 frames total ((30 + 10) × 4 + 30)

### Looping Presentation
Input: 3 images
frames_per_image: 60
transition_frames: 15
loop_slideshow: True
Result: 225 frames total ((60 + 15) × 3)

## Notes

- Total frames = (frames_per_image + transition_frames) × (number_of_images - 1) + frames_per_image
- Transitions are automatically handled between consecutive images
- Works with any number of input images
- Memory usage increases with number of images and frame count
- Compatible with any image size/aspect ratio
- Can be combined with other animation nodes for complex effects
