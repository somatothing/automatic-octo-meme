"""Tests for the file extractor module."""

import tempfile
import zipfile
from pathlib import Path
from unittest.mock import Mock

import pytest

from src.extractor import ExtractionError, FileExtractor


class TestFileExtractor:
    """Test cases for FileExtractor class."""
    
    @pytest.fixture
    def extractor(self):
        """Create a FileExtractor instance for testing."""
        return FileExtractor()
    
    @pytest.fixture
    def mock_logger(self):
        """Create a mock logger for testing."""
        return Mock()
    
    @pytest.fixture
    def sample_zip_file(self):
        """Create a sample zip file for testing."""
        with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_zip:
            with zipfile.ZipFile(temp_zip.name, 'w') as zip_ref:
                zip_ref.writestr('test_file.txt', 'This is test content')
                zip_ref.writestr('folder/nested_file.txt', 'Nested content')
            yield Path(temp_zip.name)
            Path(temp_zip.name).unlink(missing_ok=True)
    
    def test_extractor_initialization_with_default_logger(self):
        """Test FileExtractor initialization with default logger."""
        extractor = FileExtractor()
        assert extractor.logger is not None
        assert extractor.logger.name == 'src.extractor'
    
    def test_extractor_initialization_with_custom_logger(self, mock_logger):
        """Test FileExtractor initialization with custom logger."""
        extractor = FileExtractor(logger=mock_logger)
        assert extractor.logger is mock_logger
    
    def test_extract_zip_success(self, extractor, sample_zip_file):
        """Test successful zip extraction."""
        with tempfile.TemporaryDirectory() as temp_dir:
            extract_to = Path(temp_dir)
            
            extracted_files = extractor.extract_zip(sample_zip_file, extract_to)
            
            assert len(extracted_files) == 2
            assert (extract_to / 'test_file.txt').exists()
            assert (extract_to / 'folder' / 'nested_file.txt').exists()
            
            # Verify content
            with open(extract_to / 'test_file.txt', 'r') as f:
                assert f.read() == 'This is test content'
    
    def test_extract_zip_nonexistent_file(self, extractor):
        """Test extraction with nonexistent zip file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            nonexistent_zip = Path(temp_dir) / 'nonexistent.zip'
            extract_to = Path(temp_dir) / 'extract'
            
            with pytest.raises(ExtractionError, match="Zip file not found"):
                extractor.extract_zip(nonexistent_zip, extract_to)
    
    def test_extract_zip_invalid_file(self, extractor):
        """Test extraction with invalid zip file."""
        with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_file:
            temp_file.write(b'This is not a zip file')
            temp_file.flush()
            
            with tempfile.TemporaryDirectory() as temp_dir:
                extract_to = Path(temp_dir)
                
                with pytest.raises(ExtractionError, match="Invalid zip file"):
                    extractor.extract_zip(temp_file.name, extract_to)
            
            Path(temp_file.name).unlink(missing_ok=True)
    
    def test_extract_zip_directory_path_as_zip(self, extractor):
        """Test extraction when zip path is a directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_dir = Path(temp_dir) / 'not_a_file'
            zip_dir.mkdir()
            extract_to = Path(temp_dir) / 'extract'
            
            with pytest.raises(ExtractionError, match="Path is not a file"):
                extractor.extract_zip(zip_dir, extract_to)
    
    def test_extract_zip_creates_extraction_directory(self, extractor, sample_zip_file):
        """Test that extraction creates the target directory if it doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            extract_to = Path(temp_dir) / 'new_directory' / 'nested'
            
            extracted_files = extractor.extract_zip(sample_zip_file, extract_to)
            
            assert extract_to.exists()
            assert len(extracted_files) == 2
    
    def test_extract_zip_overwrite_behavior(self, extractor, sample_zip_file):
        """Test overwrite behavior when files already exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            extract_to = Path(temp_dir)
            
            # Create existing file
            existing_file = extract_to / 'test_file.txt'
            existing_file.write_text('Existing content')
            
            # Extract without overwrite (default)
            extracted_files = extractor.extract_zip(sample_zip_file, extract_to, overwrite=False)
            
            # Should skip existing file
            assert len(extracted_files) == 1  # Only the nested file
            assert existing_file.read_text() == 'Existing content'
            
            # Extract with overwrite
            extracted_files = extractor.extract_zip(sample_zip_file, extract_to, overwrite=True)
            
            # Should overwrite existing file
            assert len(extracted_files) == 2
            assert existing_file.read_text() == 'This is test content'