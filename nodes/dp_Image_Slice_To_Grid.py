import torch


class DP_Image_Slice_To_Grid:
    def __init__(self):
        self.output_dir = "ComfyUI/temp"
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "rows": ("INT", {"default": 2, "min": 1, "max": 32}),
                "columns": ("INT", {"default": 2, "min": 1, "max": 32}),
                "overlap_pixels": ("INT", {"default": 0, "min": 0, "max": 512}),
            },
        }

    RETURN_TYPES = ("IMAGE", "INT", "INT", "INT", "INT", "INT")
    RETURN_NAMES = (
        "slices",
        "original_height",
        "original_width",
        "rows",
        "columns",
        "overlap",
    )
    FUNCTION = "slice_image"
    CATEGORY = "image/processing"

    def slice_image(self, image, rows, columns, overlap_pixels):
        # Convert from tensor format
        if isinstance(image, torch.Tensor):
            image = image.cpu().numpy()

        # Get image dimensions
        height, width = image.shape[1:3]

        # Calculate slice dimensions
        slice_height = height // rows
        slice_width = width // columns

        # Prepare list for slices
        slices = []

        # Create slices with overlap
        for i in range(rows):
            for j in range(columns):
                # Calculate boundaries with overlap
                y_start = max(0, i * slice_height - overlap_pixels)
                y_end = min(height, (i + 1) * slice_height + overlap_pixels)
                x_start = max(0, j * slice_width - overlap_pixels)
                x_end = min(width, (j + 1) * slice_width + overlap_pixels)

                # Extract slice
                slice_img = image[:, y_start:y_end, x_start:x_end, :]
                slices.append(torch.from_numpy(slice_img))

        # Stack all slices vertically
        result = torch.cat(slices, dim=0)

        return (result, height, width, rows, columns, overlap_pixels)
