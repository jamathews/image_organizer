import argparse
import fnmatch
import os
import shutil

# Parse command line arguments
parser = argparse.ArgumentParser(description='Process a root folder.')
parser.add_argument('root_folder', type=str, help='The root folder to process.')

args = parser.parse_args()


# Function to process folder
def process_folder(folder):
    for year in range(2001, 2025):
        year_folder = os.path.join(folder, str(year))
        for month in range(1, 13):
            month_folder = os.path.join(folder, str(year), str(month).zfill(2))
            os.makedirs(month_folder, exist_ok=True)
            sub_folders = find_matching_subfolders(year_folder, year, month)
            if sub_folders:
                for sub_folder in sub_folders:
                    src = os.path.join(year_folder,sub_folder)
                    dest = os.path.join(month_folder, sub_folder)
                    print(f"Moving {src} to {dest}")
                    shutil.move(src, dest)


def find_matching_subfolders(root_path, year, month):
    pattern_dash = f"{year}-{str(month).zfill(2)}-*"
    pattern_underscore = f"{year}_{str(month).zfill(2)}_*"
    contents = os.listdir(root_path)
    return fnmatch.filter(contents, pattern_dash) + fnmatch.filter(contents, pattern_underscore)


if __name__ == '__main__':
    process_folder(args.root_folder)
