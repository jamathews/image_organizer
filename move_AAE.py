import os
import shutil

from pathlib import Path


def relocate_aae_files():
    for filename in os.listdir('.'):
        if filename.endswith('.AAE'):
            if filename.startswith("IMG_O"):
                no_o_filename = filename.replace("IMG_O", "IMG_")
                no_o_basename = os.path.splitext(no_o_filename)[0]
                target_dir = find_dir_with_matching_files(no_o_basename)
                print(f"{filename}->{target_dir}")
                try:
                    shutil.move(filename, target_dir)
                except shutil.Error as e:
                    print(f"{filename}->{e}")


def find_dir_with_matching_files(target_basename):
    # Start from the current directory
    current_directory = os.getcwd()

    matching_dirs = set()

    # Walk the directory tree
    for dirpath, dirnames, filenames in os.walk(current_directory):
        # Check each file
        for filename in filenames:
            # If the basename matches, append the file path to the list
            if os.path.splitext(filename)[0] == target_basename:
                matching_dirs.add(dirpath)

    assert len(matching_dirs) == 1
    return Path(matching_dirs.pop())


if __name__ == '__main__':
    relocate_aae_files()
