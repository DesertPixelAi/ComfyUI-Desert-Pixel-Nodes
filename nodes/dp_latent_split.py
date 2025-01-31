import torch

class DP_Latent_Split:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "latent": ("LATENT",),
                "rows": ("INT", {"default": 2, "min": 1, "max": 8, "step": 1}),
                "columns": ("INT", {"default": 4, "min": 1, "max": 8, "step": 1}),
                "overlap_pixels": ("INT", {"default": 0, "min": 0, "max": 128, "step": 8}),
            }
        }

    RETURN_TYPES = ("LATENT", "LATENT", "LATENT")
    RETURN_NAMES = ("latent_grid", "latent_grid_flipped", "latent_grid_plus_flipped")
    FUNCTION = "split_latent"
    CATEGORY = "DP/latent"

    def split_latent(self, latent, rows, columns, overlap_pixels):
        # Get the original latent tensor
        samples = latent["samples"]
        
        # Get dimensions
        batch, channels, height, width = samples.shape
        
        # Calculate cell dimensions with overlap
        cell_height = height // rows
        cell_width = width // columns
        
        # Add overlap (in latent space)
        overlap = overlap_pixels // 8  # Convert from pixel space to latent space
        
        # Initialize list for split latents
        split_latents = []
        
        # Split the latents into grid
        for row in range(rows):
            for col in range(columns):
                # Calculate base coordinates
                h_start = row * cell_height
                h_end = (row + 1) * cell_height
                w_start = col * cell_width
                w_end = (col + 1) * cell_width
                
                # Add overlap while respecting boundaries
                if overlap > 0:
                    h_start = max(0, h_start - overlap)
                    h_end = min(height, h_end + overlap)
                    w_start = max(0, w_start - overlap)
                    w_end = min(width, w_end + overlap)
                
                # Extract the cell
                cell = samples[:, :, h_start:h_end, w_start:w_end]
                split_latents.append(cell)
        
        # Stack all splits into a batch
        batched_splits = torch.cat(split_latents, dim=0)
        
        # Create flipped versions
        flipped_splits = torch.flip(batched_splits, [3])  # Flip horizontally
        
        # Combine original and flipped for third output
        combined_splits = torch.cat([batched_splits, flipped_splits], dim=0)
        
        # Return all three outputs in ComfyUI latent format
        return (
            {"samples": batched_splits},    # Original grid
            {"samples": flipped_splits},     # Flipped grid only
            {"samples": combined_splits}     # Original + flipped grid
        ) 