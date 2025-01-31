# DP Latent Split

## Description

This node splits latent space images into grids with optional overlap. It provides three output variations: original grid, horizontally flipped grid, and a combined version of both. This is particularly useful for tiled processing and creating mirror effects.

## Inputs

### Required:
- **latent**: (`LATENT`) - Input latent to be split
- **rows**: (`INT`, default: 2, range: 1-8) - Number of rows in grid
- **columns**: (`INT`, default: 4, range: 1-8) - Number of columns in grid
- **overlap_pixels**: (`INT`, default: 0, range: 0-128, step: 8) - Overlap between cells in pixels

## Outputs

- **latent_grid**: (`LATENT`) - Original split grid
- **latent_grid_flipped**: (`LATENT`) - Horizontally flipped version of the grid
- **latent_grid_plus_flipped**: (`LATENT`) - Combined original and flipped grids

## Features

- **Grid Processing**:
  - Flexible grid dimensions
  - Customizable overlap
  - Boundary handling
  - Automatic scaling

- **Output Options**:
  - Original grid splits
  - Mirrored versions
  - Combined outputs
  - Batch processing

## Example Usage

Basic Grid Split:
```python
latent: <latent_input>
rows: 2
columns: 2
overlap_pixels: 0
# Returns: 2x2 grid of latents
```

With Overlap:
```python
latent: <latent_input>
rows: 3
columns: 3
overlap_pixels: 64
# Returns: 3x3 grid with 64px overlap
```

## Notes

- Maintains latent space scaling (8x smaller than pixel space)
- Handles overlap boundaries correctly
- Memory-efficient processing
- Automatic batch handling
- Preserves tensor dimensions
- Comprehensive error handling
- Supports variable grid sizes
