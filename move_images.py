#!/usr/bin/env python3
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import exifread
from PIL import Image
from PIL import UnidentifiedImageError
from pillow_heif import register_heif_opener

register_heif_opener()


def move_file(src: Path, dest: Path):
    """
    This function is used to move a file from a source path to a destination path.
    If the destination path does not exist, it will be created.
    If the file already exists at the destination path, the operation will not be performed.

    Args:
    src (Path): The source file path.
    dest (Path): The destination path.

    """
    # Ensure that src file exists
    if not Path(src).is_file():
        print('The source file does not exist.')
        return

    # Create directories if they don't exist
    Path(dest).mkdir(parents=True, exist_ok=True)

    # Prepend the destination folder path to the source filename
    dest_path = os.path.join(dest, os.path.basename(src))

    # Ensure the destination file does not exist
    if os.path.isfile(dest_path):
        print(f'The destination file already exists: {dest_path}')
        return

    # Move the file
    print(f"Moving {src} to {dest_path}")
    shutil.move(src, dest_path)


def is_image(file_path: Path) -> bool:
    """
    This function checks if a given file is an image.

    Args:
    file_path (Path): The path to the file to check.

    Returns:
    bool: True if the file is an image, False otherwise.
    """
    try:
        Image.open(file_path).verify()
        return True
    except UnidentifiedImageError:
        return False
    except IOError:
        return False


def extract_capture_date(image_file_path: Path) -> Optional[datetime]:
    """
    This function extracts the capture date from an image file.

    Args:
    image_file_path (Path): The path to the image file.

    Returns:
    Optional[datetime]: The capture date of the image if available, None otherwise.
    """
    # Open image file for reading (binary mode)
    with open(image_file_path, 'rb') as f:
        # Return Exif tags
        tags = exifread.process_file(f)

    # Check if the key 'Image DateTime' exists
    if 'Image DateTime' in tags:
        # Get the capture date
        capture_date = tags['Image DateTime']
        return datetime.strptime(str(capture_date), '%Y:%m:%d %H:%M:%S')
    return None


def move_images(src: Path, dest: Path) -> None:
    """
    This function moves all images from the source path to the destination path, organizing them by the capture date.
    Non-image files will be ignored.

    Args:
    src (Path): The source directory path.
    dest (Path): The destination directory path.
    """
    # Check if the source directory exists
    if not os.path.isdir(src):
        print(f"Source directory {src} does not exist.")
        return

    # Check if the destination directory exists
    if not os.path.isdir(dest):
        print(f"Destination directory {dest} does not exist.")
        return

    for file in os.listdir(src):
        if is_image(Path(os.path.join(src, file))):
            try:
                capture_date = extract_capture_date(Path(os.path.join(src, file)))
                year = capture_date.strftime('%Y')
                month = capture_date.strftime('%m')
                date = capture_date.strftime('%Y-%m-%d')
                target_folder = Path(os.path.join(dest, year, month, date))

                file_basename = os.path.splitext(file)[0]
                files_with_same_basename = [f for f in os.listdir(src) if os.path.splitext(f)[0] == file_basename]
                for new_file in files_with_same_basename:
                    move_file(Path(os.path.join(src, new_file)), target_folder)

            except Exception as e:
                print(f"Could not extract capture date for {file}. {e}")


if __name__ == "__main__":
    """
    This is the entry point for the script.
    It expects two command-line arguments: the source directory and the destination directory.
    """
    # Check if there are enough arguments
    if len(sys.argv) != 3:
        print(f"Usage: python {os.path.basename(sys.argv[0])} [source folder] [destination folder]")
        sys.exit(1)

    # Get the source and destination directories
    source_dir = sys.argv[1]
    dest_dir = sys.argv[2]

    # Call the main function
    move_images(Path(source_dir), Path(dest_dir))
