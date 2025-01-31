# DP Set New Model Folder Link

## Description

This node manages symbolic links to model folders within ComfyUI. It allows you to create shortcuts to external model folders without copying files, saving disk space. **Requires administrator privileges** to create symbolic links.

## Inputs

### Required:
- **action**: (`COMBO`) - Operation to perform:
  - "create" - Make new symbolic link
  - "delete" - Remove existing link
  - "list" - Show all current links

### Optional:
- **your_model_folder**: (`STRING`) - Target folder in ComfyUI where link will be created
- **the_other_model_folder**: (`STRING`) - Source folder containing the models to link
- **link_to_delete**: (`STRING`) - Path of link to remove when using delete action

## Outputs

- **STRING**: Operation result message showing success/failure and link details

## Features

- **Link Management**:
  - Create symbolic links
  - Delete existing links
  - List active links
  - Status verification

- **Processing**:
  - Path validation
  - Permission checking
  - Link status monitoring
  - Error reporting

## Example Usage

Creating a Link:
```python
action: "create"
your_model_folder: "ComfyUI/models/checkpoints"
the_other_model_folder: "D:/AI/Models/Stable-diffusion"
# Creates shortcut in ComfyUI checkpoints folder
```

Listing Links:
```python
action: "list"
# Shows all active links with status (✓ active, ✗ broken)
```

Deleting a Link:
```python
action: "delete"
link_to_delete: "ComfyUI/models/checkpoints/Stable-diffusion"
# Removes specified symbolic link
```

## Notes

- Requires administrator privileges
- Validates paths before operations
- Checks link status
- Memory-efficient processing
- Comprehensive error handling
- Safe link management
- Status reporting
