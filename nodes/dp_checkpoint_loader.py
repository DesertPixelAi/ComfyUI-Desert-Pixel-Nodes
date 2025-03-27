import os

import comfy.sd
import comfy.utils
import folder_paths


class DP_Load_Checkpoint_With_Info:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "ckpt_name": (
                    folder_paths.get_filename_list("checkpoints"),
                    {"tooltip": "The name of the checkpoint (model) to load."},
                )
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP", "VAE", "STRING")
    RETURN_NAMES = ("model", "clip", "vae", "model_info")
    FUNCTION = "load_checkpoint"

    CATEGORY = "Desert Pixel/loaders"

    def load_checkpoint(self, ckpt_name):
        ckpt_path = folder_paths.get_full_path_or_raise("checkpoints", ckpt_name)
        out = comfy.sd.load_checkpoint_guess_config(
            ckpt_path,
            output_vae=True,
            output_clip=True,
            embedding_directory=folder_paths.get_folder_paths("embeddings"),
        )
        model, clip, vae = out[:3]

        # Get model name without extension
        model_name = os.path.splitext(ckpt_name)[0]

        # Format info string
        info = f"checkpoint name: {model_name}"

        return (model, clip, vae, info)
