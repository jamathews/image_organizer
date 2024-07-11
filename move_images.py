#!/usr/bin/env python3
import os
import sys

import PIL
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()

from PIL.ExifTags import TAGS
from datetime import datetime


def get_capture_date(image):
    try:
        exif_data = image.getexif()
    except Exception:
        print(f"No exif data in {image.filename}")
        return None

    for tag_id in exif_data:
        tag_str = TAGS.get(tag_id, tag_id)
        if tag_str in ['DateTimeOriginal', 'DateTime', 'DateTimeDigitized']:
            date_str = exif_data[tag_id]
            return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
    else:
        print(f"No capture date in {image.filename}, only {[TAGS.get(tag_id, tag_id) for tag_id in exif_data]}")
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

    # Process files here...
    print(f"Processing files from {src} to {dest}")

    for file in os.listdir(src):
        try:
            image = Image.open(os.path.join(src, file))
            image.verify()
            capture_date = get_capture_date(image)
            if capture_date:
                print(capture_date)

        except (PIL.UnidentifiedImageError, IOError, SyntaxError):
            pass


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
