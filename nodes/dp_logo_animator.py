import numpy as np
import torch
import torch.nn.functional as F


class DP_Logo_Animator:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "frame_count": (
                    "INT",
                    {"default": 48, "min": 2, "max": 300, "step": 1},
                ),
                "min_scale": (
                    "FLOAT",
                    {"default": 0.2, "min": 0.1, "max": 0.99, "step": 0.01},
                ),
                "background": (["Auto", "Black", "White"],),
                "animation_pattern": (
                    [
                        "Big>Small>Big",
                        "Small>Big>Small",
                        "Big>Small",
                        "Small>Big",
                        "batch_flow_big>small",
                        "batch_flow_small>big",
                        "batch_alternate_big>small",
                        "batch_alternate_small>big",
                    ],
                ),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "animate_logo"
    CATEGORY = "DP/animation"

    def create_scale_sequence(
        self, start_scale, end_scale, frames_per_direction, pattern, batch_size=1
    ):
        """Create a smooth scale sequence based on the selected pattern"""
        if pattern.startswith("batch_alternate"):
            sequences = []
            for i in range(batch_size):
                if pattern == "batch_alternate_big>small":
                    if i % 2 == 0:  # Even indices - Big to Small
                        sequence = torch.linspace(
                            start_scale, end_scale, frames_per_direction
                        )
                    else:  # Odd indices - Small to Big
                        sequence = torch.linspace(
                            end_scale, start_scale, frames_per_direction
                        )
                else:  # batch_alternate_small>big
                    if i % 2 == 0:  # Even indices - Small to Big
                        sequence = torch.linspace(
                            end_scale, start_scale, frames_per_direction
                        )
                    else:  # Odd indices - Big to Small
                        sequence = torch.linspace(
                            start_scale, end_scale, frames_per_direction
                        )
                sequences.append(sequence)

            # Combine all sequences
            sequence = torch.cat(sequences)
            return sequence

        elif pattern.startswith("batch_flow"):
            # Each image gets frames_per_direction frames
            sequences = []
            for i in range(batch_size):
                if pattern == "batch_flow_big>small":
                    sequence = torch.linspace(
                        start_scale, end_scale, frames_per_direction
                    )
                else:  # batch_flow_small>big
                    sequence = torch.linspace(
                        end_scale, start_scale, frames_per_direction
                    )
                sequences.append(sequence)

            # Combine all sequences
            sequence = torch.cat(sequences)
            return sequence

        elif pattern in ["Big>Small>Big", "Small>Big>Small"]:
            # Full cycle patterns
            half_frames = frames_per_direction // 2
            if pattern == "Big>Small>Big":
                down = torch.linspace(start_scale, end_scale, half_frames)
                up = torch.linspace(
                    end_scale, start_scale, frames_per_direction - half_frames
                )
                sequence = torch.cat([down, up])
            else:  # Small>Big>Small
                up = torch.linspace(end_scale, start_scale, half_frames)
                down = torch.linspace(
                    start_scale, end_scale, frames_per_direction - half_frames
                )
                sequence = torch.cat([up, down])
        else:
            # Single direction patterns
            sequence = torch.linspace(start_scale, end_scale, frames_per_direction)

        # Reverse the sequence if starting from small (for original patterns)
        if pattern.startswith("Small") and not pattern.startswith("batch"):
            sequence = torch.flip(sequence, [0])

        return sequence

    def detect_background_color(self, image):
        """Detect the background color using edge sampling similar to BackgroundColorThief"""
        print("\nStarting background color detection...")
        print(f"Input image value range: {image.min():.3f} to {image.max():.3f}")

        # Convert to numpy if it's a tensor
        if torch.is_tensor(image):
            if len(image.shape) == 4:
                image = image[0]
            image = image.cpu().numpy()
            print(f"Converted tensor to numpy array, shape: {image.shape}")

        print(f"Image shape: {image.shape}, dtype: {image.dtype}")
        print(f"Image min/max values: {image.min():.3f}/{image.max():.3f}")

        h, w = image.shape[:2]

        # Calculate sampling limits (10% of width/height)
        width_limit = int(w * 0.1)
        height_limit = int(h * 0.1)
        print(f"Sampling limits - width: {width_limit}, height: {height_limit}")

        pixels = []

        # Sample top edge
        top_edge = image[:height_limit, :].reshape(-1, 3)
        pixels.extend(top_edge)
        print(f"Top edge samples: {len(top_edge)}")

        # Sample bottom edge
        bottom_edge = image[-height_limit:, :].reshape(-1, 3)
        pixels.extend(bottom_edge)
        print(f"Bottom edge samples: {len(bottom_edge)}")

        # Sample left edge (excluding corners already sampled)
        left_edge = image[height_limit:-height_limit, :width_limit].reshape(-1, 3)
        pixels.extend(left_edge)
        print(f"Left edge samples: {len(left_edge)}")

        # Sample right edge (excluding corners already sampled)
        right_edge = image[height_limit:-height_limit, -width_limit:].reshape(-1, 3)
        pixels.extend(right_edge)
        print(f"Right edge samples: {len(right_edge)}")

        # Convert to numpy array
        pixels = np.array(pixels)
        print(f"Total pixel samples: {len(pixels)}")

        # Use median to get the most common color
        bg_color = np.median(pixels, axis=0)
        print(
            f"Detected background color RGB: R={bg_color[0]:.3f}, G={bg_color[1]:.3f}, B={bg_color[2]:.3f}"
        )

        return bg_color

    def animate_logo(
        self,
        images,
        frame_count=48,
        min_scale=0.2,
        background="Black",
        animation_pattern="Big>Small>Big",
    ):
        print(f"\nAnimating logo batch with {frame_count} frames")

        # Ensure we're working with a batch of images
        if len(images.shape) == 3:
            images = images.unsqueeze(0)

        # Limit batch size to 10
        batch_size = min(images.shape[0], 10)
        images = images[:batch_size]

        print(
            f"Processing batch of {batch_size} images with pattern: {animation_pattern}"
        )

        all_animated_frames = []

        # Generate scale sequence once for all images
        scales = self.create_scale_sequence(
            1.0, min_scale, frame_count, animation_pattern, batch_size
        )

        # For batch_flow pattern, frame_count is the duration of one direction (big to small)
        if (
            animation_pattern == "batch_flow_big>small"
            or animation_pattern == "batch_flow_small>big"
        ):
            # Each image gets exactly frame_count frames to go from big to small
            for idx in range(batch_size):
                current_image = images[idx]

                # Process image format conversion
                if current_image.shape[-1] in [3, 4]:
                    current_image = current_image.permute(2, 0, 1)
                    if current_image.shape[0] == 4:
                        rgb = current_image[:3]
                        alpha = current_image[3:]
                        current_image = rgb * alpha + (1 - alpha)

                c, h, w = current_image.shape

                # Set background color
                if background == "Auto":
                    temp_img = current_image.permute(1, 2, 0).cpu().numpy()
                    bg_color = self.detect_background_color(temp_img)
                    bg_value = torch.tensor(
                        bg_color, device=current_image.device, dtype=torch.float32
                    ).view(3, 1, 1)
                else:
                    bg_value = 1.0 if background == "White" else 0.0
                    bg_value = torch.tensor(
                        [bg_value] * 3, device=current_image.device
                    ).view(3, 1, 1)

                # Get scales for this image - each image gets frame_count frames
                start_idx = idx * frame_count
                end_idx = start_idx + frame_count
                image_scales = scales[start_idx:end_idx]

                # Create frames for this image
                for scale in image_scales:
                    scale_factor = scale.item()
                    new_h = max(int(h * scale_factor), 1)
                    new_w = max(int(w * scale_factor), 1)

                    background_frame = bg_value.expand(3, h, w)

                    resized = F.interpolate(
                        current_image.unsqueeze(0),
                        size=(new_h, new_w),
                        mode="bilinear",
                        align_corners=False,
                    )[0]

                    pad_h = (h - new_h) // 2
                    pad_w = (w - new_w) // 2

                    frame = background_frame.clone()
                    frame[:, pad_h : pad_h + new_h, pad_w : pad_w + new_w] = resized

                    frame = frame.permute(1, 2, 0)
                    all_animated_frames.append(frame)
        else:
            # Original processing for other patterns
            # Process each image in the batch
            for idx in range(batch_size):
                current_image = images[idx]

                # Convert image from HWC to CHW format if needed
                if current_image.shape[-1] in [3, 4]:  # Handle both RGB and RGBA
                    current_image = current_image.permute(2, 0, 1)
                    if current_image.shape[0] == 4:  # If RGBA, convert to RGB
                        rgb = current_image[:3]
                        alpha = current_image[3:]
                        current_image = rgb * alpha + (1 - alpha)

                c, h, w = current_image.shape

                # Set background color
                if background == "Auto":
                    # Convert to HWC for background detection
                    temp_img = current_image.permute(1, 2, 0).cpu().numpy()
                    bg_color = self.detect_background_color(temp_img)
                    bg_value = torch.tensor(
                        bg_color, device=current_image.device, dtype=torch.float32
                    ).view(3, 1, 1)
                else:
                    bg_value = 1.0 if background == "White" else 0.0
                    bg_value = torch.tensor(
                        [bg_value] * 3, device=current_image.device
                    ).view(3, 1, 1)

                # Get scales for this image - each image gets frame_count frames
                start_idx = idx * frame_count
                end_idx = start_idx + frame_count
                image_scales = scales[start_idx:end_idx]

                frames = []
                for scale in image_scales:
                    # Calculate new dimensions while maintaining aspect ratio
                    scale_factor = scale.item()
                    new_h = max(int(h * scale_factor), 1)
                    new_w = max(int(w * scale_factor), 1)

                    # Create background frame
                    background_frame = bg_value.expand(3, h, w)

                    # Resize the current image
                    resized = F.interpolate(
                        current_image.unsqueeze(0),
                        size=(new_h, new_w),
                        mode="bilinear",
                        align_corners=False,
                    )[0]

                    # Calculate padding for centering
                    pad_h = (h - new_h) // 2
                    pad_w = (w - new_w) // 2

                    # Create the frame
                    frame = background_frame.clone()
                    frame[:, pad_h : pad_h + new_h, pad_w : pad_w + new_w] = resized

                    # Convert to HWC format
                    frame = frame.permute(1, 2, 0)
                    frames.append(frame)

                all_animated_frames.extend(frames)

        # Stack all frames
        final_frames = torch.stack(all_animated_frames)

        return (final_frames,)
