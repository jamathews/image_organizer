#!/usr/bin/env python3
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

import PIL
import exifread
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()


def move_file(src: Path, dest: Path):
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


def is_image(file_path):
    try:
        Image.open(file_path).verify()
        return True
    except PIL.UnidentifiedImageError:
        return False
    except IOError:
        return False


def extract_capture_date(image_file_path):
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


def move_images(src, dest):
    # Check if the source directory exists
    if not os.path.isdir(src):
        print(f"Source directory {src} does not exist.")
        return

    # Check if the destination directory exists
    if not os.path.isdir(dest):
        print(f"Destination directory {dest} does not exist.")
        return

    for file in os.listdir(src):
        if is_image(os.path.join(src, file)):
            try:
                capture_date = extract_capture_date(os.path.join(src, file))
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
    # Check if there are enough arguments
    if len(sys.argv) != 3:
        print(f"Usage: python {os.path.basename(sys.argv[0])} [source folder] [destination folder]")
        sys.exit(1)

    # Get the source and destination directories
    source_dir = sys.argv[1]
    dest_dir = sys.argv[2]

    # Call the main function
    move_images(source_dir, dest_dir)
