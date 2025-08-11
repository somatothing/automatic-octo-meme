"""Main entry point for the automatic-octo-meme application."""

import argparse
import logging
import sys
from pathlib import Path

from .extractor import ExtractionError, FileExtractor


def setup_logging(verbose: bool = False) -> logging.Logger:
    """Set up logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)


def main() -> int:
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description="Extract and process files with robust error handling"
    )
    parser.add_argument("zip_file", help="Path to the zip file to extract")
    parser.add_argument("extract_to", help="Directory to extract files to")
    parser.add_argument("--overwrite", action="store_true", 
                       help="Overwrite existing files")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose logging")
    
    args = parser.parse_args()
    
    logger = setup_logging(args.verbose)
    extractor = FileExtractor(logger)
    
    try:
        extracted_files = extractor.extract_zip(
            args.zip_file, args.extract_to, args.overwrite
        )
        logger.info(f"Successfully extracted {len(extracted_files)} files")
        return 0
    except ExtractionError as e:
        logger.error(f"Extraction failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())