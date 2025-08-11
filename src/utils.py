"""Utility functions for file operations and validation."""

import os
from pathlib import Path
from typing import List, Union


def validate_file_path(file_path: Union[str, Path]) -> Path:
    """Validate and convert a file path to a Path object.
    
    Args:
        file_path: The file path to validate.
        
    Returns:
        A validated Path object.
        
    Raises:
        ValueError: If the path is invalid.
    """
    path = Path(file_path)
    if not path.exists():
        raise ValueError(f"Path does not exist: {path}")
    return path


def get_file_size(file_path: Union[str, Path]) -> int:
    """Get the size of a file in bytes.
    
    Args:
        file_path: Path to the file.
        
    Returns:
        File size in bytes.
    """
    return os.path.getsize(file_path)


def list_files_in_directory(directory: Union[str, Path], pattern: str = "*") -> List[Path]:
    """List all files in a directory matching a pattern.
    
    Args:
        directory: Directory to search in.
        pattern: Glob pattern to match files.
        
    Returns:
        List of matching file paths.
    """
    dir_path = Path(directory)
    return list(dir_path.glob(pattern))