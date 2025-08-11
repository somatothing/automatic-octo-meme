# automatic-octo-meme
test1

## Zip File Functionality

This repository now includes .zip file creation and extraction capabilities.

### Files Added:

- `create_zip.py` - Script to create a sample .zip file with example content
- `extract_zip.py` - Script to safely extract .zip files
- `sample_data.tar` - Sample archive file for testing extraction

### Usage:

1. **Create a sample .zip file:**
   ```bash
   python3 create_zip.py
   ```

2. **Extract a .zip file:**
   ```bash
   python3 extract_zip.py sample_archive.zip
   ```
   Or simply: `python3 extract_zip.py` (defaults to sample_archive.zip)

3. **Extract tar files:**
   ```bash
   tar -xf sample_data.tar
   ```

### Features:

- Safe extraction with directory creation
- Support for nested directory structures
- Error handling for corrupted archives
- Listing of extracted files
- Cross-platform compatibility

Run `python3 create_zip.py` to generate a sample .zip file that can be used for testing the extraction functionality.