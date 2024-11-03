from textnode import *
from htmlnode import *
import os
import shutil


def prepare_copying():
    # Check if static exist
    if not os.path.exists("./static"):
        raise Exception("No 'static' folder inside path, nothing to generate")
    # Wipe public folder and create it again
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    os.mkdir("./public")


def copy_files_recursively(source_folder, dest_folder):
    files = os.listdir(source_folder)
    for file in files:
        path_to_file = os.path.join(source_folder, file)
        if os.path.isfile(path_to_file):
            shutil.copy(path_to_file, dest_folder)
        elif os.path.isdir(path_to_file):
            new_folder_path = os.path.join(dest_folder, file)
            os.mkdir(new_folder_path)
            copy_files_recursively(path_to_file, new_folder_path)
    pass


def main():
    prepare_copying()
    copy_files_recursively("./static", "./public/")


if __name__ == "__main__":
    main()
