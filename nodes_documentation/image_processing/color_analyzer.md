# DP Image Color Analyzer
<img src="https://github.com/user-attachments/assets/bf90ffac-3925-40ed-9873-2ea3a7d42d1c" alt="DP_Image_Color_Analyzer" style="float: left; margin-right: 10px;"/>

## Description
The DP Image Color Analyzer node is designed to extract dominant colors from images and create color palettes based on the number of colors specified by the user. It provides detailed information about the color values, making it useful for various applications such as styling, design, and exploring image colors.

## Inputs
- **IMAGE** - `image` - The input image to analyze for dominant colors.
- **INT** - `num_colors` - The number of dominant colors to extract from the image. Default is 5, with a range from 3 to 16.
- **INT** - `color_sample_width` - The width of the color sample images. Default is 512, with a range from 8 to 4096.
- **INT** - `color_sample_height` - The height of the color sample images. Default is 512, with a range from 8 to 4096.
- **ANY** - `pipe_input` (optional) - An alternative input method for providing an image as a tensor or PIL Image.

## Outputs
- **IMAGE** - The output images of the extracted color panels, each as a separate image tensor.
- **STRING** - A summary of the dominant colors and their percentages.
- **STRING** - A description of the overall color theme detected in the image.
- **STRING** - Detailed information about each color, including RGB values and hex codes.

## Example Usage
To use the DP Image Color Analyzer node, connect an image to the `image` input or provide a tensor/PIL Image through the `pipe_input`. Set the `num_colors` to define how many dominant colors you want to extract. Adjust the `color_sample_width` and `color_sample_height` to control the size of the output color panels. The node will generate a palette of dominant colors along with detailed information about each color.
