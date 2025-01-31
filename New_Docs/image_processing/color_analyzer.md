# DP Color Analyzer

<img src="https://github.com/user-attachments/assets/bf90ffac-3925-40ed-9873-2ea3a7d42d1c" alt="DP_Image_Color_Analyzer" style="float: left; margin-right: 10px;"/>

## Description

The Color Analyzer node extracts dominant colors from images using advanced clustering techniques. It provides detailed color information including RGB values, hex codes, color names, and percentages. The node features smart color naming, theme detection, and customizable color sample generation.

## Inputs

### Required:
- **image**: (`IMAGE`) - Input image to analyze
- **num_colors**: (`INT`, default: 5, range: 3-16) - Number of dominant colors to extract
- **color_sample_width**: (`INT`, default: 512, range: 8-4096) - Width of color sample images
- **color_sample_height**: (`INT`, default: 512, range: 8-4096) - Height of color sample images

## Outputs

- **image**: (`IMAGE`) - Color sample panels showing extracted colors
- **color_names**: (`STRING`) - List of identified color names
- **theme**: (`STRING`) - Overall color theme description
- **color_info**: (`STRING`) - Detailed color information including:
  - Color names
  - Percentages
  - RGB values
  - Hex codes
- **hex_values**: (`STRING`) - List of hex color codes

## Features

- **Advanced Color Analysis**:
  - K-means clustering for accurate color extraction
  - Delta-E color difference calculations
  - L*a*b* color space conversion
  - Smart color naming system

- **Comprehensive Color Data**:
  - RGB values
  - Hex codes
  - Color percentages
  - Closest named colors
  - Theme detection

- **Color Sample Generation**:
  - Customizable panel dimensions
  - Sorted by color prominence
  - Visual color representation

- **Smart Theme Detection**:
  - Identifies dominant colors
  - Generates theme descriptions
  - Handles multiple color combinations

- **Error Handling**:
  - Input validation
  - Memory management
  - Fallback color systems
  - Graceful error recovery

## Example Output
```
Color Names:
Deep Blue
Crimson Red
Forest Green

Theme:
Deep blue and crimson color palette

Detailed Information:
Deep Blue  |  45.2%  |  r=28 g=35 b=129  |  #1C2381
Crimson Red  |  30.5%  |  r=220 g=20 b=60  |  #DC143C
Forest Green  |  24.3%  |  r=34 g=139 b=34  |  #228B22
```

## Notes

- Supports both RGB and RGBA input images
- Processes images up to 4096x4096 pixels
- Uses comprehensive color name database
- Automatically handles color space conversions
- Provides fallback for undefined colors
- Memory-efficient processing for large images
