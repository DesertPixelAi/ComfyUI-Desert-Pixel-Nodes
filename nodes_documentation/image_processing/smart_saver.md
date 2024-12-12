# DP Smart Image Saver
<img src="https://github.com/user-attachments/assets/704ed83f-daa9-46aa-aadc-7e89a3943010" alt="DP_Smart_Saver" style="float: left; margin-right: 10px;"/>

## Description
The DP Smart Image Saver node is designed to save images with customizable options for folder and file naming, size, and additional text. It supports both preview and save modes, allowing users to see the dimensions of the image without saving it. Additionally, it can save a caption text file, which is useful for model training captions.

## Inputs
- **STRING** - `mode` - The mode of operation, either "SAVE_IMAGE" or "PREVIEW_ONLY". Default is "SAVE_IMAGE".
- **IMAGE** - `image` - The input image to be saved.
- **STRING** - `folder_name` - The name of the folder where the image will be saved. Default is "folder_name".
- **STRING** - `file_name` - The base name for the saved file. Default is "my_file_name".
- **STRING** - `extra_text` - Additional text to append to the file name. Default is an empty string.
- **BOOLEAN** - `add_size_to_name` - Whether to include the image dimensions in the file name. Default is false.
- **BOOLEAN** - `save_caption` - Whether to save a caption text file. Default is false.
- **STRING** - `caption_text` - The text to be saved in the caption file. Default is an empty string.

## Outputs
- **STRING** - `file_info` - Information about the saved file, including its path, dimensions, and size.

## Example Usage
To use the DP Smart Image Saver node, connect an image to the `image` input. Set the `folder_name` and `file_name` to define where and how the image will be saved. Use the `extra_text` input to add any additional information to the file name. If you want to save a caption, enable the `save_caption` option and provide the `caption_text`. Choose "SAVE_IMAGE" to save the image or "PREVIEW_ONLY" to see the dimensions without saving.
