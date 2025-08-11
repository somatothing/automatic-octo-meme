"""Tests for utility functions."""

import tempfile
from pathlib import Path

import pytest

from src.utils import get_file_size, list_files_in_directory, validate_file_path


class TestValidateFilePath:
    """Test cases for validate_file_path function."""
    
    def test_validate_existing_file(self):
        """Test validation of existing file path."""
        with tempfile.NamedTemporaryFile() as temp_file:
            result = validate_file_path(temp_file.name)
            assert isinstance(result, Path)
            assert result.exists()
    
    def test_validate_existing_directory(self):
        """Test validation of existing directory path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = validate_file_path(temp_dir)
            assert isinstance(result, Path)
            assert result.exists()
            assert result.is_dir()
    
    def test_validate_nonexistent_path(self):
        """Test validation of nonexistent path."""
        nonexistent_path = "/this/path/does/not/exist"
        with pytest.raises(ValueError, match="Path does not exist"):
            validate_file_path(nonexistent_path)


class TestGetFileSize:
    """Test cases for get_file_size function."""
    
    def test_get_size_of_existing_file(self):
        """Test getting size of existing file."""
        test_content = "This is test content"
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write(test_content)
            temp_file.flush()
            
            size = get_file_size(temp_file.name)
            assert size == len(test_content.encode())
            
            Path(temp_file.name).unlink()


class TestListFilesInDirectory:
    """Test cases for list_files_in_directory function."""
    
    def test_list_all_files(self):
        """Test listing all files in directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create test files
            (temp_path / "file1.txt").touch()
            (temp_path / "file2.py").touch()
            (temp_path / "subdir").mkdir()
            (temp_path / "subdir" / "file3.txt").touch()
            
            files = list_files_in_directory(temp_dir)
            file_names = [f.name for f in files]
            
            assert "file1.txt" in file_names
            assert "file2.py" in file_names
            assert "subdir" in file_names
    
    def test_list_files_with_pattern(self):
        """Test listing files with specific pattern."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create test files
            (temp_path / "file1.txt").touch()
            (temp_path / "file2.py").touch()
            (temp_path / "file3.txt").touch()
            
            txt_files = list_files_in_directory(temp_dir, "*.txt")
            txt_file_names = [f.name for f in txt_files]
            
            assert len(txt_files) == 2
            assert "file1.txt" in txt_file_names
            assert "file3.txt" in txt_file_names
            assert "file2.py" not in txt_file_names