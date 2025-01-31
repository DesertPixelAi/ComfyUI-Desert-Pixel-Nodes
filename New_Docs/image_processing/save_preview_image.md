# DP Save Preview Image

## Description

The Save Preview Image node provides flexible options for saving and previewing images with metadata. It supports both single images and batches, with options for custom naming, folder organization, and metadata embedding.

## Inputs

### Required:
- **mode**: (`COMBO`) - Operation mode
  - "SAVE_IMAGE" - Save to output directory
  - "PREVIEW_ONLY" - Generate temporary preview
- **image**: (`IMAGE`) - Image to save/preview
- **folder_name**: (`STRING`, default: "dp_image_folder") - Output subfolder path
- **file_name**: (`STRING`, default: "image") - Base name for saved files
- **extra_text**: (`STRING`, default: "") - Additional text for filename
- **add_size_to_name**: (`BOOLEAN`, default: False) - Include dimensions in filename
- **save_caption**: (`BOOLEAN`, default: False) - Save prompt text as caption file

### Optional:
- **prompt_and_caption_text**: (`STRING`) - Text for caption and metadata
- **negative_or_other**: (`STRING`) - Additional metadata text

## Outputs

- UI update with saved/preview image information

## Features

- **File Management**:
  - Automatic subfolder creation
  - Duplicate filename handling
  - Path sanitization
  - Batch processing support

- **Naming Options**:
  - Custom base filename
  - Optional size suffix
  - Extra text addition
  - Automatic indexing for batches

- **Metadata Handling**:
  - PNG metadata embedding
  - Caption file generation
  - Prompt text storage
  - Additional info storage

## Example Usage

Basic Image Save:
```python
mode: "SAVE_IMAGE"
folder_name: "my_outputs"
file_name: "generated_image"
```

Preview with Caption:
```python
mode: "PREVIEW_ONLY"
save_caption: True
prompt_and_caption_text: "A detailed description"
```

## Notes

- Supports PNG format
- Compression level: 4 (1 for previews)
- Creates unique filenames
- Handles nested folders
- UTF-8 caption encoding
- Memory-efficient processing
- Automatic path sanitization
