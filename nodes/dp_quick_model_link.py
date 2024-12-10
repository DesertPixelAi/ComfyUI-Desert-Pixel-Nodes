import os
import subprocess
import json
from pathlib import Path
import ctypes
import sys

class DP_symlink:
    """
    ComfyUI node for managing symbolic links to model folders.
    Allows creating and managing symbolic links without leaving ComfyUI.
    """
    def __init__(self):
        # Create symbolic_links directory if it doesn't exist
        self.links_dir = Path(os.path.join(os.path.dirname(__file__), 'symbolic_links'))
        self.links_dir.mkdir(exist_ok=True)
        self.links_file = Path(os.path.join(self.links_dir, 'symlinks.json'))
        self.load_links()
        
    def load_links(self):
        """Load saved symlinks from JSON file"""
        if self.links_file.exists():
            with open(self.links_file, 'r') as f:
                self.links = json.load(f)
        else:
            self.links = {}
            self.save_links()
            
    def save_links(self):
        """Save symlinks to JSON file"""
        with open(self.links_file, 'w') as f:
            json.dump(self.links, f, indent=4)
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "action": (["create", "delete", "list"], {"default": "list"}),
            },
            "optional": {
                "target_folder": ("STRING", {"default": ""}),
                "source_folder": ("STRING", {"default": ""}),
                "link_to_delete": ("STRING", {"default": ""})
            }
        }
    RETURN_TYPES = ("STRING",)
    FUNCTION = "execute"
    CATEGORY = "DP/utils"
    OUTPUT_NODE = True
    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    def create_symlink(self, target, source):
        if not os.path.exists(source):
            return f"Error: Source folder does not exist: {source}"
        # Check if target is an existing folder with content
        if os.path.isdir(target) and os.listdir(target):
            # Create a subfolder automatically
            subfolder_name = os.path.basename(source)
            target = os.path.join(target, subfolder_name)
        try:
            # Check if the exact target path exists
            if os.path.exists(target):
                if os.path.isdir(target):
                    subprocess.run(['rmdir', target], shell=True, check=True)
                else:
                    os.remove(target)
            # Create symlink using mklink /D
            cmd = f'cmd /c mklink /D "{target}" "{source}"'
            process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if process.returncode == 0:
                self.links[target] = source
                self.save_links()
                return f"Successfully created symlink:\nTarget: {target}\nSource: {source}"
            else:
                error_msg = process.stderr.strip() if process.stderr else "Unknown error"
                return f"Failed to create symlink:\n{error_msg}"
        except Exception as e:
            return f"Error creating symlink:\n{str(e)}"
    def delete_symlink(self, target):
        if not target in self.links:
            return f"Error: Symlink not found: {target}"
        try:
            subprocess.run(['rmdir', target], shell=True, check=True)
            del self.links[target]
            self.save_links()
            return f"Successfully deleted symlink:\n{target}"
        except Exception as e:
            return f"Error deleting symlink:\n{str(e)}"
    def list_symlinks(self):
        if not self.links:
            return "No symbolic links found."
        result = "Current Symbolic Links:\n\n"
        for target, source in self.links.items():
            exists = "✓" if os.path.exists(target) else "✗"
            result += f"{exists} Target: {target}\n   Source: {source}\n\n"
        return result
    def execute(self, action, target_folder="", source_folder="", link_to_delete=""):
        if not self.is_admin():
            return ("This node requires administrator privileges. Please run ComfyUI as administrator.",)
        if action == "create":
            if not target_folder or not source_folder:
                return ("Please provide both target and source folders.",)
            result = self.create_symlink(target_folder, source_folder)
            
        elif action == "delete":
            if not link_to_delete:
                return ("Please provide the target path to delete.",)
            result = self.delete_symlink(link_to_delete)
            
        else:  # list
            result = self.list_symlinks()
        return (result,)