# DP Big Letters
<img src="https://github.com/user-attachments/assets/c40205d0-6327-47f3-b9f0-29fb3d048ef8" alt="DP_Big_Letters" style="float: left; margin-right: 10px;"/>

## Description

The DP Big Letters node splits user-provided text into individual letters and creates an image for each letter in the selected size. This is useful for later effects or animations. Users can customize the color, background, font, and padding for each letter, allowing for a wide range of creative possibilities.

## Inputs
- **STRING** - `text` - The text to be split into letters. Default is "DESERT PIXEL".
- **INT** - `image_width` - The width of the image for each letter. Default is 1024, with a range from 64 to 2048.
- **INT** - `image_height` - The height of the image for each letter. Default is 1024, with a range from 64 to 2048.
- **INT** - `padding_top` - The top padding for the letter image. Default is 120, with a range from 0 to 500.
- **INT** - `padding_bottom` - The bottom padding for the letter image. Default is 120, with a range from 0 to 500.
- **INT** - `padding_left` - The left padding for the letter image. Default is 100, with a range from 0 to 500.
- **INT** - `padding_right` - The right padding for the letter image. Default is 100, with a range from 0 to 500.
- **STRING** - `font_name` - The name of the font to use for the letters.
- **STRING** - `font_weight` - The weight of the font (e.g., regular, bold).
- **STRING** - `font_color` - The color of the font. Options include "white", "black", "red", "green", "blue", "yellow".
- **STRING** - `background_color` - The background color of the letter images. Options include "black", "white", "red", "green", "blue", "yellow".

## Outputs
- **IMAGE** - The output images of the letters, each as a separate image tensor.

## Example Usage
To use the DP Big Letters node, provide the text you want to split into letters. Set the desired image dimensions, padding, font name, font weight, font color, and background color. The node will generate an image for each letter, which can be used for effects or animations.
