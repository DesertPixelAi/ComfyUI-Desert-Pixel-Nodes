# DP Quick Link
<img src="https://github.com/user-attachments/assets/b58b9557-e3be-4639-9958-ea0a901210e8" alt="DP_Quick_Link" style="float: left; margin-right: 10px;"/>

## Description

A utility node for managing symbolic links to model folders within ComfyUI. It allows you to create shortcuts to external model folders without copying files, saving disk space. **Requires administrator privileges** to create symbolic links.

## Inputs

**Required:**
- `action`: Selection between:
  - `create`: Make new symbolic link
  - `delete`: Remove existing link
  - `list`: Show all current links

**Optional:**
- `your_model_folder`: Target folder in ComfyUI where link will be created
- `the_other_model_folder`: Source folder containing the models to link
- `link_to_delete`: Path of link to remove when using delete action

## Outputs

- `STRING`: Operation result message showing success/failure and link details

## Example Usage

**Creating a Link:**
```
action: "create"
your_model_folder: "ComfyUI/models/checkpoints"
the_other_model_folder: "D:/AI/Models/Stable-diffusion"
```
This will create a shortcut in your ComfyUI checkpoints folder pointing to your external models.

**Listing Links:**
```
action: "list"
```
Shows all active links with their status (✓ active, ✗ broken)

**Deleting a Link:**
```
action: "delete"
link_to_delete: "ComfyUI/models/checkpoints/Stable-diffusion"
```

Note: Remember to run ComfyUI as administrator for this node to work properly.
