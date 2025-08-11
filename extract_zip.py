#!/usr/bin/env python3
"""
Script to extract .zip files safely.
"""

import zipfile
import os
import sys

def extract_zip(zip_path, extract_to="extracted"):
    """
    Extract a .zip file to the specified directory.
    
    Args:
        zip_path (str): Path to the .zip file
        extract_to (str): Directory to extract files to
    """
    if not os.path.exists(zip_path):
        print(f"Error: {zip_path} not found!")
        return False
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            # Create extraction directory if it doesn't exist
            os.makedirs(extract_to, exist_ok=True)
            
            # Extract all files
            zipf.extractall(extract_to)
            print(f"Successfully extracted {zip_path} to {extract_to}/")
            
            # List extracted files
            print("Extracted files:")
            for file in zipf.namelist():
                print(f"  - {file}")
            
            return True
    except zipfile.BadZipFile:
        print(f"Error: {zip_path} is not a valid .zip file!")
        return False
    except Exception as e:
        print(f"Error extracting {zip_path}: {e}")
        return False

if __name__ == "__main__":
    zip_file = sys.argv[1] if len(sys.argv) > 1 else "sample_archive.zip"
    extract_zip(zip_file)