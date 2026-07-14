"""
Script to Split Dataset into Train, Validation, and Test Sets for YOLO or Pascal VOC Formats

This script takes an input dataset, which could be in YOLO or Pascal VOC format, and splits it into
three sets: training, validation, and test. The script supports both YOLO and Pascal VOC annotation formats.
The directory structure is created accordingly, and for YOLO format, a 'data.yaml' file is generated for
easy configuration with YOLO.

Usage:
1. Specify the inputFolderPath containing the original dataset.
2. Specify the outputFolderPath where the split dataset and 'data.yaml' will be saved.
3. Adjust the splitRatio to define the percentage of data for each set (train, val, test).
4. Specify the format_type as "YOLO" or "PascalVOC" based on the dataset format.
5. Provide a list of classes relevant to the dataset in the 'classes' parameter.
6. Run the script.

Original Author: Murtaza Hassan - contact@murtazahassan.com
Modification by: Zainab Ishtiaq
"""

import os
import random
import shutil
from itertools import islice


def createDirectories(outputFolderPath, format_type):
    """Create directories for storing train, test, (and val) images and labels."""
    if format_type == "YOLO":
        os.makedirs(f"{outputFolderPath}/train/images", exist_ok=True)
        os.makedirs(f"{outputFolderPath}/train/labels", exist_ok=True)
        os.makedirs(f"{outputFolderPath}/val/images", exist_ok=True)
        os.makedirs(f"{outputFolderPath}/val/labels", exist_ok=True)
        os.makedirs(f"{outputFolderPath}/test/images", exist_ok=True)
        os.makedirs(f"{outputFolderPath}/test/labels", exist_ok=True)
    elif format_type == "PascalVOC":
        os.makedirs(f"{outputFolderPath}/train", exist_ok=True)
        os.makedirs(f"{outputFolderPath}/test", exist_ok=True)


def splitData(inputFolderPath, outputFolderPath, splitRatio, format_type="YOLO", classes=["object"]):
    """Main function to handle data splitting for both YOLO and Pascal VOC formats."""

    # Remove existing output folder if exists, else create it
    try:
        shutil.rmtree(outputFolderPath)
    except OSError as e:
        os.mkdir(outputFolderPath)

    createDirectories(outputFolderPath, format_type)

    listNames = os.listdir(inputFolderPath)
    uniqueNames = list(set([os.path.splitext(name)[0] for name in listNames]))

    # Shuffle and split the data
    random.shuffle(uniqueNames)
    lenData = len(uniqueNames)

    if format_type == "YOLO":
        lenTrain = int(lenData * splitRatio['train'])
        lenVal = int(lenData * splitRatio['val'])
        lenTest = int(lenData * splitRatio['test'])

        if lenData != lenTrain + lenTest + lenVal:
            remaining = lenData - (lenTrain + lenTest + lenVal)
            lenTrain += remaining

        sequence = ['train', 'val', 'test']
        lenSplit = [lenTrain, lenVal, lenTest]
    elif format_type == "PascalVOC":
        lenTrain = int(lenData * splitRatio['train'])
        lenTest = int(lenData * splitRatio['test'])

        if lenData != lenTrain + lenTest:
            remaining = lenData - (lenTrain + lenTest)
            lenTrain += remaining

        sequence = ['train', 'test']
        lenSplit = [lenTrain, lenTest]

    Input = iter(uniqueNames)
    Output = [list(islice(Input, elem)) for elem in lenSplit]
    if format_type == "YOLO":
        print(f'Total Images: {lenData} \nSplit: {len(Output[0])} {len(Output[1])} {len(Output[2])}')
    elif format_type == "PascalVOC":
        print(f'Total Images: {lenData} \nSplit: {len(Output[0])} {len(Output[1])}')

    for i, out in enumerate(Output):
        for fileName in out:
            if format_type == "YOLO":
                shutil.copy(f'{inputFolderPath}/{fileName}.jpg', f'{outputFolderPath}/{sequence[i]}/images/{fileName}.jpg')
                shutil.copy(f'{inputFolderPath}/{fileName}.txt', f'{outputFolderPath}/{sequence[i]}/labels/{fileName}.txt')
            elif format_type == "PascalVOC":
                shutil.copy(f'{inputFolderPath}/{fileName}.jpg', f'{outputFolderPath}/{sequence[i]}/{fileName}.jpg')
                shutil.copy(f'{inputFolderPath}/{fileName}.xml', f'{outputFolderPath}/{sequence[i]}/{fileName}.xml')

    print("Split Process Completed...")

# path: /content/Data/Data_ready
    if format_type == "YOLO":
        dataYaml = f'path: /content/Data/Data_ready\n\
train: ../train/images\n\
val: ../val/images\n\
test: ../test/images\n\
\n\
nc: {len(classes)}\n\
names: {classes}'

        with open(f"{outputFolderPath}/data.yaml", 'w') as f:
            f.write(dataYaml)

        print("Data.yaml file Created...")


if __name__ == "__main__":
    splitData(inputFolderPath="Data",
              outputFolderPath="Data_ready",
              splitRatio={"train": 0.8, "val": 0.1, "test": 0.1},
              format_type="YOLO",
              classes=["person"])


    # Example for Pascal VOC format
    # splitData(inputFolderPath="Project_CarCounter/PascalVOC",
    #           outputFolderPath="data_voc",
    #           splitRatio={"train": 0.8, "test": 0.2},
    #           format_type="PascalVOC",
    #           classes=["object"])

