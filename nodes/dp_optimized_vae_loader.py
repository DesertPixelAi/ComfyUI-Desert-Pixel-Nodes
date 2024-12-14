import torch
import os
import folder_paths
import comfy.sd
import comfy.utils
from typing import Dict, Any, Tuple

class DP_VAE_Decode_Optimized:
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
            # Enable TF32 for better performance on Ampere GPUs
            torch.backends.cuda.matmul.allow_tf32 = True
            torch.backends.cudnn.allow_tf32 = True
            
            # Set optimal CUDNN settings
            torch.backends.cudnn.benchmark = True
            torch.backends.cudnn.deterministic = False

    def load_vae(self, vae_name: str) -> Tuple[Any]:
        """
        Load VAE model with optimizations and caching.
        
        Args:
            vae_name: Name of the VAE model file
        """
        vae_path = folder_paths.get_full_path_or_raise("vae", vae_name)
        vae_hash = self._get_vae_hash(vae_path)
        
        # Always use caching for best performance
        if vae_hash in self._vae_cache:
            return (self._vae_cache[vae_hash],)

        # Setup optimizations
        self._optimize_torch_settings()
        
        # Load VAE with optimized settings
        with torch.cuda.amp.autocast(enabled=True):  # Use mixed precision by default
            sd = comfy.utils.load_torch_file(vae_path)
            vae = comfy.sd.VAE(sd=sd)
        
        # Always cache the VAE
        self._vae_cache[vae_hash] = vae
            
        return (vae,)
    
    @classmethod
    def cleanup_cache(cls):
        """Clear the VAE cache to free memory."""
        cls._vae_cache.clear()

class DP_VAE_Encode_Optimized:
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
            # Enable TF32 for better performance on Ampere GPUs
            torch.backends.cuda.matmul.allow_tf32 = True
            torch.backends.cudnn.allow_tf32 = True
            
            # Set optimal CUDNN settings
            torch.backends.cudnn.benchmark = True
            torch.backends.cudnn.deterministic = False

    def load_vae(self, vae_name: str) -> Tuple[Any]:
        """
        Load VAE model with optimizations and caching.
        
        Args:
            vae_name: Name of the VAE model file
        """
        vae_path = folder_paths.get_full_path_or_raise("vae", vae_name)
        vae_hash = self._get_vae_hash(vae_path)
        
        # Always use caching for best performance
        if vae_hash in self._vae_cache:
            return (self._vae_cache[vae_hash],)

        # Setup optimizations
        self._optimize_torch_settings()
        
        # Load VAE with optimized settings
        with torch.cuda.amp.autocast(enabled=True):  # Use mixed precision by default
            sd = comfy.utils.load_torch_file(vae_path)
            vae = comfy.sd.VAE(sd=sd)
        
        # Always cache the VAE
        self._vae_cache[vae_hash] = vae
            
        return (vae,)
    
    @classmethod
    def cleanup_cache(cls):
        """Clear the VAE cache to free memory."""
        cls._vae_cache.clear()

class DP_UNET_Loader_Optimized:
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
            # Enable TF32 for better performance on Ampere GPUs
            torch.backends.cuda.matmul.allow_tf32 = True
            torch.backends.cudnn.allow_tf32 = True
            
            # Set optimal CUDNN settings
            torch.backends.cudnn.benchmark = True
            torch.backends.cudnn.deterministic = False

    def load_vae(self, vae_name: str) -> Tuple[Any]:
        """
        Load VAE model with optimizations and caching.
        
        Args:
            vae_name: Name of the VAE model file
        """
        vae_path = folder_paths.get_full_path_or_raise("vae", vae_name)
        vae_hash = self._get_vae_hash(vae_path)
        
        # Always use caching for best performance
        if vae_hash in self._vae_cache:
            return (self._vae_cache[vae_hash],)

        # Setup optimizations
        self._optimize_torch_settings()
        
        # Load VAE with optimized settings
        with torch.cuda.amp.autocast(enabled=True):  # Use mixed precision by default
            sd = comfy.utils.load_torch_file(vae_path)
            vae = comfy.sd.VAE(sd=sd)
        
        # Always cache the VAE
        self._vae_cache[vae_hash] = vae
            
        return (vae,)
    
    @classmethod
    def cleanup_cache(cls):
        """Clear the VAE cache to free memory."""
        cls._vae_cache.clear()

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
            # Enable TF32 for better performance on Ampere GPUs
            torch.backends.cuda.matmul.allow_tf32 = True
            torch.backends.cudnn.allow_tf32 = True
            
            # Set optimal CUDNN settings
            torch.backends.cudnn.benchmark = True
            torch.backends.cudnn.deterministic = False

    def load_vae(self, vae_name: str) -> Tuple[Any]:
        """
        Load VAE model with optimizations and caching.
        
        Args:
            vae_name: Name of the VAE model file
        """
        vae_path = folder_paths.get_full_path_or_raise("vae", vae_name)
        vae_hash = self._get_vae_hash(vae_path)
        
        # Always use caching for best performance
        if vae_hash in self._vae_cache:
            return (self._vae_cache[vae_hash],)

        # Setup optimizations
        self._optimize_torch_settings()
        
        # Load VAE with optimized settings
        with torch.cuda.amp.autocast(enabled=True):  # Use mixed precision by default
            sd = comfy.utils.load_torch_file(vae_path)
            vae = comfy.sd.VAE(sd=sd)
        
        # Always cache the VAE
        self._vae_cache[vae_hash] = vae
            
        return (vae,)
    
    @classmethod
    def cleanup_cache(cls):
        """Clear the VAE cache to free memory."""
        cls._vae_cache.clear()

class DP_Dual_CLIP_Loader_Optimized:
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
            # Enable TF32 for better performance on Ampere GPUs
            torch.backends.cuda.matmul.allow_tf32 = True
            torch.backends.cudnn.allow_tf32 = True
            
            # Set optimal CUDNN settings
            torch.backends.cudnn.benchmark = True
            torch.backends.cudnn.deterministic = False

    def load_vae(self, vae_name: str) -> Tuple[Any]:
        """
        Load VAE model with optimizations and caching.
        
        Args:
            vae_name: Name of the VAE model file
        """
        vae_path = folder_paths.get_full_path_or_raise("vae", vae_name)
        vae_hash = self._get_vae_hash(vae_path)
        
        # Always use caching for best performance
        if vae_hash in self._vae_cache:
            return (self._vae_cache[vae_hash],)

        # Setup optimizations
        self._optimize_torch_settings()
        
        # Load VAE with optimized settings
        with torch.cuda.amp.autocast(enabled=True):  # Use mixed precision by default
            sd = comfy.utils.load_torch_file(vae_path)
            vae = comfy.sd.VAE(sd=sd)
        
        # Always cache the VAE
        self._vae_cache[vae_hash] = vae
            
        return (vae,)
    
    @classmethod
    def cleanup_cache(cls):
        """Clear the VAE cache to free memory."""
        cls._vae_cache.clear()