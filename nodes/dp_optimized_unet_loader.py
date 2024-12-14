import torch
import os
import folder_paths
import comfy.sd
from typing import Dict, Any, Tuple

class DP_UNET_Loader_Optimized:
    _model_cache = {}  # Class-level cache for loaded models
    _weight_cache = {}  # New cache for model weights
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "unet_name": (folder_paths.get_filename_list("diffusion_models"), ),
                "weight_dtype": (["default", "fp8_e4m3fn", "fp8_e4m3fn_fast", "fp8_e5m2"],),
            }
        }
    
    RETURN_TYPES = ("MODEL",)
    FUNCTION = "load_unet"
    CATEGORY = "DP/optimized"

    @classmethod
    def preload_weights(cls, unet_name: str):
        """Preload model weights into RAM before GPU transfer"""
        unet_path = folder_paths.get_full_path_or_raise("diffusion_models", unet_name)
        if unet_path not in cls._weight_cache:
            cls._weight_cache[unet_path] = comfy.utils.load_torch_file(unet_path)
    
    @staticmethod
    def _get_model_hash(unet_path: str) -> str:
        """Generate a unique hash for the model file."""
        return f"{os.path.getmtime(unet_path)}_{os.path.getsize(unet_path)}"

    @staticmethod
    def _setup_model_options(weight_dtype: str, enable_memory_efficient_attention: bool) -> Dict[str, Any]:
        """Configure model options based on weight dtype."""
        model_options = {}
        
        dtype_mapping = {
            "fp8_e4m3fn": (torch.float8_e4m3fn, False),
            "fp8_e4m3fn_fast": (torch.float8_e4m3fn, True),
            "fp8_e5m2": (torch.float8_e5m2, False)
        }
        
        if weight_dtype in dtype_mapping:
            dtype, fp8_optimizations = dtype_mapping[weight_dtype]
            model_options["dtype"] = dtype
            if fp8_optimizations:
                model_options["fp8_optimizations"] = True
        
        if enable_memory_efficient_attention:
            model_options["use_memory_efficient_attention"] = True
                
        return model_options

    @staticmethod
    def _optimize_torch_settings():
        """Apply various PyTorch optimizations."""
        if torch.cuda.is_available():
            # Enable TF32 for better performance on Ampere GPUs
            torch.backends.cuda.matmul.allow_tf32 = True
            torch.backends.cudnn.allow_tf32 = True
            
            # Set optimal CUDNN settings
            torch.backends.cudnn.benchmark = True
            torch.backends.cudnn.deterministic = False

    def load_unet(self, 
                  unet_name: str, 
                  weight_dtype: str) -> Tuple[Any]:
        """
        Load UNET model with optimizations and caching.
        
        Args:
            unet_name: Name of the UNET model file
            weight_dtype: Type of weight dtype to use
        """
        # Hard-code the optimization settings
        use_cached = True
        enable_memory_efficient_attention = True
        
        unet_path = folder_paths.get_full_path_or_raise("diffusion_models", unet_name)
        model_hash = self._get_model_hash(unet_path)
        
        # Check cache first if enabled
        if use_cached and model_hash in self._model_cache:
            return (self._model_cache[model_hash],)

        # Setup optimizations
        self._optimize_torch_settings()
        
        # Configure model options
        model_options = self._setup_model_options(weight_dtype, enable_memory_efficient_attention)
        
        # Use preloaded weights if available
        if unet_path in self._weight_cache:
            model = comfy.sd.create_model_from_weights(
                self._weight_cache[unet_path],
                model_options=model_options
            )
        else:
            model = comfy.sd.load_diffusion_model(unet_path, model_options=model_options)
        
        # Warmup pass with dummy data if model is on CUDA
        if hasattr(model, 'model') and hasattr(model.model, 'device'):
            if model.model.device.type == "cuda":
                dummy_input = torch.randn(1, 4, 64, 64, device=model.model.device)
                with torch.no_grad():
                    for _ in range(3):  # Multiple warmup passes
                        model(dummy_input)
        
        # Cache the model if caching is enabled
        if use_cached:
            self._model_cache[model_hash] = model
            
        return (model,)
    
    @classmethod
    def cleanup_cache(cls):
        """Clear the model cache to free memory."""
        cls._model_cache.clear()

class DP_VAE_Loader_Optimized:
    _vae_cache = {}  # Class-level cache for loaded VAEs
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "vae_name": (folder_paths.get_filename_list("vae"), ),
            }
        }
    
    RETURN_TYPES = ("VAE",)
    FUNCTION = "load_vae"
    CATEGORY = "DP/optimized"

    @staticmethod
    def _get_vae_hash(vae_path: str) -> str:
        """Generate a unique hash for the VAE file."""
        return f"{os.path.getmtime(vae_path)}_{os.path.getsize(vae_path)}"

    @staticmethod
    def _optimize_torch_settings():
        """Apply various PyTorch optimizations."""
        if torch.cuda.is_available():
            torch.backends.cuda.matmul.allow_tf32 = True
            torch.backends.cudnn.allow_tf32 = True
            torch.backends.cudnn.benchmark = True
            torch.backends.cudnn.deterministic = False

    def load_vae(self, vae_name: str) -> Tuple[Any]:
        """
        Load VAE model with optimizations and caching.
        """
        vae_path = folder_paths.get_full_path_or_raise("vae", vae_name)
        vae_hash = self._get_vae_hash(vae_path)
        
        # Always use caching for best performance
        if vae_hash in self._vae_cache:
            return (self._vae_cache[vae_hash],)

        # Setup optimizations
        self._optimize_torch_settings()
        
        # Load VAE with optimized settings
        with torch.cuda.amp.autocast(enabled=True):
            sd = comfy.utils.load_torch_file(vae_path)
            vae = comfy.sd.VAE(sd=sd)
        
        # Cache the VAE
        self._vae_cache[vae_hash] = vae
            
        return (vae,)