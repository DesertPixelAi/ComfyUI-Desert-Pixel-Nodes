# DP Aspect Ratio
<img src="https://github.com/user-attachments/assets/514f81d2-3b50-442c-b9e1-d95f93647747" alt="DP_Aspect_Ratio" style="float: left; margin-right: 10px;"/>

## Description

A utility node for selecting image dimensions from predefined aspect ratios. Reads ratios from a customizable text file, making it easy to add or modify your preferred dimensions.

## Inputs

- `aspect_ratio`: Dropdown selection of available ratios from the text file

## Outputs

- `width`: Selected width in pixels
- `height`: Selected height in pixels

## Customization

The node reads from `my_aspect_ratios.txt` in the following format:
```
name, width, height
```

Example entries:
```
1024x1024 1:1 square, 1024, 1024
1280x768 5:3 gen3Ready landscape, 1280, 768
768x1280 3:5 gen3Ready portrait, 768, 1280
```

Default included ratios:
- Square formats (512x512, 768x768, 1024x1024)
- Standard ratios (4:3, 16:9, 3:2)
- Portrait & Landscape variants
- Special formats (Golden ratio, Cinematic, Panoramic)

Note: If the text file is not found, defaults to 1024x1024 square format.
