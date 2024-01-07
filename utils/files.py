import os
from shutil import rmtree


def remove_folder_contents(folder_path):
    # Iterate over all files and subfolders in the given folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        # Check if the item is a file and remove it
        if os.path.isfile(item_path):
            os.remove(item_path)

        # If the item is a directory, recursively remove its contents
        elif os.path.isdir(item_path):
            rmtree(item_path)


def create_folder(folder_path):
    # Check if the folder does not exist
    if not os.path.exists(folder_path):
        # Create the folder
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print(f"Folder '{folder_path}' already exists.")
