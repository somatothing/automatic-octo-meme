"""File extraction utilities with robust error handling and logging."""

import logging
import os
import zipfile
from pathlib import Path
from typing import List, Optional, Union


class ExtractionError(Exception):
    """Custom exception for extraction-related errors."""
    pass


class FileExtractor:
    """A robust file extractor with comprehensive error handling."""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize the FileExtractor.
        
        Args:
            logger: Optional logger instance. If None, creates a default logger.
        """
        self.logger = logger or self._create_default_logger()
    
    def _create_default_logger(self) -> logging.Logger:
        """Create a default logger for the extractor."""
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def extract_zip(
        self, 
        zip_path: Union[str, Path], 
        extract_to: Union[str, Path],
        overwrite: bool = False
    ) -> List[str]:
        """Extract a zip file to the specified directory.
        
        Args:
            zip_path: Path to the zip file to extract.
            extract_to: Directory to extract files to.
            overwrite: Whether to overwrite existing files.
            
        Returns:
            List of extracted file paths.
            
        Raises:
            ExtractionError: If extraction fails.
        """
        zip_path = Path(zip_path)
        extract_to = Path(extract_to)
        
        # Validate inputs
        if not zip_path.exists():
            raise ExtractionError(f"Zip file not found: {zip_path}")
        
        if not zip_path.is_file():
            raise ExtractionError(f"Path is not a file: {zip_path}")
        
        # Create extraction directory if it doesn't exist
        extract_to.mkdir(parents=True, exist_ok=True)
        
        extracted_files = []
        
        try:
            self.logger.info(f"Starting extraction of {zip_path} to {extract_to}")
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for file_info in zip_ref.infolist():
                    target_path = extract_to / file_info.filename
                    
                    if target_path.exists() and not overwrite:
                        self.logger.warning(f"Skipping existing file: {target_path}")
                        continue
                    
                    zip_ref.extract(file_info, extract_to)
                    extracted_files.append(str(target_path))
                    self.logger.debug(f"Extracted: {target_path}")
            
            self.logger.info(f"Successfully extracted {len(extracted_files)} files")
            return extracted_files
            
        except zipfile.BadZipFile as e:
            raise ExtractionError(f"Invalid zip file: {zip_path}") from e
        except PermissionError as e:
            raise ExtractionError(f"Permission denied: {e}") from e
        except OSError as e:
            raise ExtractionError(f"OS error during extraction: {e}") from e