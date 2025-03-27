import random

import torch


class DP_Image_Color_Effect:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "color": (
                    [
                        "purple",
                        "yellow",
                        "pink",
                        "blue",
                        "red",
                        "orange",
                        "magenta",
                        "green",
                        "violet",
                        "cyan",
                    ],
                ),
                "blend_mode": (
                    [
                        "Normal",
                        "Add",
                        "Multiply",
                        "Screen",
                        "Overlay",
                        "Soft Light",
                        "Hard Light",
                        "Color Dodge",
                        "Color Burn",
                        "Difference",
                    ],
                ),
                "strength": (
                    "FLOAT",
                    {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01},
                ),
            },
            "hidden": {"unique_id": "UNIQUE_ID"},
        }

    RETURN_TYPES = ("IMAGE", "IMAGE")
    RETURN_NAMES = ("single_effect", "all_colors_batch")
    FUNCTION = "process"
    CATEGORY = "DP/Image"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float(
            "NaN"
        )  # This ensures the node always executes with new random values

    def get_color_layer(self, image_shape, color):
        color_layer = torch.zeros(image_shape)
        # Set color values with new hex values matching our sequence
        if color == "deep_purple":
            color_layer[:, :, :, 0] = 0x24 / 255.0  # R
            color_layer[:, :, :, 1] = 0x13 / 255.0  # G
            color_layer[:, :, :, 2] = 0x7C / 255.0  # B
        elif color == "purple":
            color_layer[:, :, :, 0] = 0x74 / 255.0
            color_layer[:, :, :, 1] = 0x15 / 255.0
            color_layer[:, :, :, 2] = 0xA8 / 255.0
        elif color == "yellow":
            color_layer[:, :, :, 0] = 0xFF / 255.0
            color_layer[:, :, :, 1] = 0xE2 / 255.0
            color_layer[:, :, :, 2] = 0x29 / 255.0
        elif color == "pink":
            color_layer[:, :, :, 0] = 0xFF / 255.0
            color_layer[:, :, :, 1] = 0x1A / 255.0
            color_layer[:, :, :, 2] = 0xE0 / 255.0
        elif color == "light_green":
            color_layer[:, :, :, 0] = 0x9B / 255.0
            color_layer[:, :, :, 1] = 0xFF / 255.0
            color_layer[:, :, :, 2] = 0x70 / 255.0
        elif color == "blue":
            color_layer[:, :, :, 0] = 0x33 / 255.0
            color_layer[:, :, :, 1] = 0x9C / 255.0
            color_layer[:, :, :, 2] = 0xFF / 255.0
        elif color == "red":
            color_layer[:, :, :, 0] = 0xDF / 255.0
            color_layer[:, :, :, 1] = 0x11 / 255.0
            color_layer[:, :, :, 2] = 0x11 / 255.0
        elif color == "orange":
            color_layer[:, :, :, 0] = 0xFF / 255.0
            color_layer[:, :, :, 1] = 0x95 / 255.0
            color_layer[:, :, :, 2] = 0x0A / 255.0
        elif color == "yellow_green":
            color_layer[:, :, :, 0] = 0xF3 / 255.0
            color_layer[:, :, :, 1] = 0xFF / 255.0
            color_layer[:, :, :, 2] = 0x14 / 255.0
        elif color == "magenta":
            color_layer[:, :, :, 0] = 0xA7 / 255.0
            color_layer[:, :, :, 1] = 0x16 / 255.0
            color_layer[:, :, :, 2] = 0x7E / 255.0
        elif color == "royal_blue":
            color_layer[:, :, :, 0] = 0x2F / 255.0
            color_layer[:, :, :, 1] = 0x18 / 255.0
            color_layer[:, :, :, 2] = 0xC9 / 255.0
        elif color == "green":
            color_layer[:, :, :, 0] = 0x32 / 255.0
            color_layer[:, :, :, 1] = 0xEC / 255.0
            color_layer[:, :, :, 2] = 0x5D / 255.0
        elif color == "hot_pink":
            color_layer[:, :, :, 0] = 0xFF / 255.0
            color_layer[:, :, :, 1] = 0x1A / 255.0
            color_layer[:, :, :, 2] = 0x71 / 255.0
        elif color == "light_purple":
            color_layer[:, :, :, 0] = 0xBA / 255.0
            color_layer[:, :, :, 1] = 0x66 / 255.0
            color_layer[:, :, :, 2] = 0xFF / 255.0
        elif color == "violet":
            color_layer[:, :, :, 0] = 0x77 / 255.0
            color_layer[:, :, :, 1] = 0x0F / 255.0
            color_layer[:, :, :, 2] = 0xFF / 255.0
        elif color == "lime_green":
            color_layer[:, :, :, 0] = 0x62 / 255.0
            color_layer[:, :, :, 1] = 0xDD / 255.0
            color_layer[:, :, :, 2] = 0x31 / 255.0
        elif color == "cyan":
            color_layer[:, :, :, 0] = 0x29 / 255.0
            color_layer[:, :, :, 1] = 0xFB / 255.0
            color_layer[:, :, :, 2] = 0xFF / 255.0
        else:
            # Default to white instead of black if color not found
            color_layer[:, :, :, :] = 1.0
        return color_layer

    def apply_blend_mode(self, base, blend, mode, strength):
        if mode == "Normal":
            return base * (1 - strength) + blend * strength
        elif mode == "Add":
            return torch.clamp(base + (blend * strength), 0, 1)
        elif mode == "Multiply":
            return base * (1 - strength) + (base * blend) * strength
        elif mode == "Screen":
            return base * (1 - strength) + (1 - (1 - base) * (1 - blend)) * strength
        elif mode == "Overlay":
            return (
                base * (1 - strength)
                + (
                    torch.where(
                        base < 0.5, 2 * base * blend, 1 - 2 * (1 - base) * (1 - blend)
                    )
                )
                * strength
            )
        elif mode == "Soft Light":
            return (
                base * (1 - strength)
                + (
                    torch.where(
                        blend < 0.5,
                        base * (2 * blend),
                        1 - (1 - base) * (2 - 2 * blend),
                    )
                )
                * strength
            )
        elif mode == "Hard Light":
            return (
                base * (1 - strength)
                + (
                    torch.where(
                        blend < 0.5, 2 * base * blend, 1 - 2 * (1 - base) * (1 - blend)
                    )
                )
                * strength
            )
        elif mode == "Color Dodge":
            return torch.clamp(base / (1 - blend + 1e-6), 0, 1)
        elif mode == "Color Burn":
            return 1 - torch.clamp((1 - base) / (blend + 1e-6), 0, 1)
        elif mode == "Difference":
            return base * (1 - strength) + torch.abs(base - blend) * strength
        return base

    def create_retro_effect(self, image, blend_mode, strength):
        # Set new random seed for this execution
        random.seed(random.randint(0, 0xFFFFFFFFFFFFFFFF))

        # Define the exact color sequence with hex values
        color_sequence = [
            [0x24, 0x13, 0x7C],  # Deep Purple
            [0x74, 0x15, 0xA8],  # Purple
            [0xFF, 0xE2, 0x29],  # Yellow
            [0xFF, 0x1A, 0xE0],  # Pink
            [0x9B, 0xFF, 0x70],  # Light Green
            [0x33, 0x9C, 0xFF],  # Blue
            [0xDF, 0x11, 0x11],  # Red
            [0xFF, 0x95, 0x0A],  # Orange
            [0xF3, 0xFF, 0x14],  # Yellow-Green
            [0xA7, 0x16, 0x7E],  # Magenta
            [0x2F, 0x18, 0xC9],  # Royal Blue
            [0x32, 0xEC, 0x5D],  # Green
            [0xFF, 0x1A, 0x71],  # Hot Pink
            [0xFF, 0xEF, 0x0A],  # Yellow
            [0xBA, 0x66, 0xFF],  # Light Purple
            [0x77, 0x0F, 0xFF],  # Violet
            [0x62, 0xDD, 0x31],  # Lime Green
            [0xFF, 0x7B, 0x00],  # Orange
            [0xFF, 0x14, 0x47],  # Red
            [0x29, 0xFB, 0xFF],  # Cyan
        ]

        # Convert hex values to float RGB (0-1 range)
        color_sequence = [
            [r / 255.0, g / 255.0, b / 255.0] for r, g, b in color_sequence
        ]

        # Always generate new random sequence
        # 1. Random flip
        if random.random() < 0.5:
            color_sequence = color_sequence[::-1]

        # 2. Random starting point
        start_idx = random.randint(0, len(color_sequence) - 1)
        color_sequence = color_sequence[start_idx:] + color_sequence[:start_idx]

        retro_frames = []
        for color in color_sequence:
            color_layer = torch.zeros_like(image)
            color_layer[:, :, :, 0] = color[0]  # R
            color_layer[:, :, :, 1] = color[1]  # G
            color_layer[:, :, :, 2] = color[2]  # B

            modified = self.apply_blend_mode(image, color_layer, blend_mode, strength)
            retro_frames.append(modified)

        return torch.cat(retro_frames, dim=0)

    def process(self, image, color, blend_mode, strength, unique_id):
        try:
            # Set new random seed for this execution
            random.seed(random.randint(0, 0xFFFFFFFFFFFFFFFF))

            # Process single effect
            color_layer = self.get_color_layer(image.shape, color)
            single_effect = self.apply_blend_mode(
                image, color_layer, blend_mode, strength
            )

            # Process all colors batch - this creates a batch of 20 images
            all_colors_batch = self.create_retro_effect(image, blend_mode, strength)

            # Ensure both outputs have correct dimensions
            # single_effect should be [1, H, W, C]
            if len(single_effect.shape) == 3:
                single_effect = single_effect.unsqueeze(0)

            # all_colors_batch is already [20, H, W, C] from create_retro_effect

            return (single_effect, all_colors_batch)

        except Exception as e:
            print(f"Error in process: {str(e)}")
            raise e
