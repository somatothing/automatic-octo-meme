#!/usr/bin/env python3
"""
Script to create a sample .zip file for extraction testing.
"""

import zipfile
import os

def create_sample_zip():
    """Create a sample .zip file with example content."""
    zip_filename = "sample_archive.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Create a directory structure with sample files
        zipf.writestr("example/hello.txt", "Hello, World!\nThis is a sample text file.")
        zipf.writestr("example/data.json", '{\n  "name": "sample",\n  "version": "1.0",\n  "description": "Sample data file"\n}')
        zipf.writestr("example/readme.md", "# Sample Archive\n\nThis is a sample archive for extraction testing.\n")
        zipf.writestr("config.ini", "[settings]\nversion=1.0\ndebug=true\n")
        zipf.writestr("script.py", "#!/usr/bin/env python3\nprint('Hello from extracted script!')\n")
    
    print(f"Created {zip_filename} successfully!")
    return zip_filename

if __name__ == "__main__":
    create_sample_zip()