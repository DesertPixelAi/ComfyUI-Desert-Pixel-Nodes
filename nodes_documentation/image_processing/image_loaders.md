# DP Image Loaders (Small/Medium/Big)

## Description

The DP Image Loaders are designed to load images with optional pre-processing effects and extract metadata, including names and prompts. Each loader supports a variety of image effects, allowing for flexible image manipulation. The available effects include: **grayscale, enhance, flip_h, flip_v, posterize, sharpen, contrast, equalize, sepia, blur, emboss, palette, solarize, denoise, vignette, glow_edges, edge_detect, edge_gradient, lineart_clean, lineart_anime, threshold, pencil_sketch, sketch_lines, bold_lines, depth_edges, relief_light, edge_enhance, edge_morph, relief_shadow**.

## Small Loader
<img src="https://github.com/user-attachments/assets/14545cb5-6868-4446-b6ec-711bed60c956" alt="DP_Image_Loader_Small" style="float: left; margin-right: 10px;"/>

### Inputs
- **STRING** - `image` - The input image to be loaded.
- **ANY** - `pipe_input` (optional) - An alternative input method for providing an image as a tensor or PIL Image. If this input is connected, it will be preferred over the load image button, allowing for seamless integration into workflows as a multi-effects node.
- **Each output has a combo input for selecting effects.**

### Outputs
- **IMAGE** - `output1` - The processed image with the first effect applied.
- **IMAGE** - `output2` - The processed image with the second effect applied.

### Example Usage
To use the DP Image Loader Small node, connect an image to the `image` input. The node will apply the default effects and output the processed images.

---

## Medium Loader
<img src="https://github.com/user-attachments/assets/5ab0c438-8841-4e1f-b7e2-23ac449d7475" alt="DP_Image_Loader_Medium" style="float: left; margin-right: 10px;"/>

### Inputs

- **STRING** - `image` - The input image to be loaded.
- **ANY** - `pipe_input` (optional) - An alternative input method for providing an image as a tensor or PIL Image. If this input is connected, it will be preferred over the load image button, allowing for seamless integration into workflows as a multi-effects node.
- **Each output has a combo input for selecting effects.**

### Outputs

- **IMAGE** - `output1` - The processed image with the first effect applied.
- **IMAGE** - `output2` - The processed image with the second effect applied.
- **IMAGE** - `output3` - The processed image with the third effect applied.

### Example Usage
To use the DP Image Loader Medium node, connect an image to the `image` input. The node will apply the default effects and output the processed images along with extracted metadata.

---

## Big Loader
<img src="https://github.com/user-attachments/assets/c76ec189-1634-4972-bdc4-81f32167abe9" alt="DP_Image_Loader_Big" style="float: left; margin-right: 10px;"/>

### Inputs
- **STRING** - `image` - The input image to be loaded.
- **ANY** - `pipe_input` (optional) - An alternative input method for providing an image as a tensor or PIL Image. If this input is connected, it will be preferred over the load image button, allowing for seamless integration into workflows as a multi-effects node.
- **Each output has a combo input for selecting effects.**

### Outputs
- **IMAGE** - `output1` - The processed image with the first effect applied.
- **IMAGE** - `output2` - The processed image with the second effect applied.
- **IMAGE** - `output3` - The processed image with the third effect applied.
- **IMAGE** - `output4` - The processed image with the fourth effect applied.

### Example Usage
To use the DP Image Loader Big node, connect an image to the `image` input. The node will apply the default effects and output the processed images along with extracted metadata and additional settings for some effects.
