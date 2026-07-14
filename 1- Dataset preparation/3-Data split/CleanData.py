'''
This script cleans your Images folder by extracting pairs of annotated txt file + jpg img to a destination "Data" folder.
'''

import os
import shutil

# Directory where your files are located
source_folder = 'Images'

# Directory where matched .jpg and .txt files will be moved
destination_folder = 'Data'
os.makedirs(destination_folder, exist_ok=True)

# Get all the files in the source folder
files = os.listdir(source_folder)

# Create sets to store .jpg and .txt file names (without extensions)
jpg_files = set()
txt_files = set()

# Loop through files and categorize them based on extension
for file in files:
    if file.endswith('.jpg'):
        jpg_files.add(os.path.splitext(file)[0])
    elif file.endswith('.txt'):
        txt_files.add(os.path.splitext(file)[0])

# Find files with the same name (common in both sets)
common_files = jpg_files.intersection(txt_files)

# Move the matched files to the destination folder
for file_name in common_files:
    jpg_file_path = os.path.join(source_folder, file_name + '.jpg')
    txt_file_path = os.path.join(source_folder, file_name + '.txt')

    # Move .jpg file
    shutil.move(jpg_file_path, os.path.join(destination_folder, file_name + '.jpg'))

    # Move .txt file
    shutil.move(txt_file_path, os.path.join(destination_folder, file_name + '.txt'))

print(f'Moved {len(common_files)} pairs of .jpg and .txt files to the Data folder.')
