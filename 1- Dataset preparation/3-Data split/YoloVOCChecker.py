"""
This script helps in visualizing and cleaning a dataset.
It displays annotated images from a dataset.
The annotations can either be in YOLO or VOC format.

Features:
1. Supports both YOLO and VOC annotation formats.
2. Provides two main modes for displaying the dataset images:
   - In the first mode, by setting `imagesToDisplay` to a specific number, the script will randomly display that
     many annotated images, stacked together in a single window.
   - In the second mode, by setting `imagesToDisplay` to None, it will display each annotated image one by one in
     a new window. This mode also provides additional functionalities to navigate through the images:
       - Press 'd': To delete the current image and its corresponding annotation.
       - Press space bar: To move to the next image.
       - Press 'z': To move back to the previous image.

Author: Murtaza Hassan
Website: www.computervision.zone

"""

import os
import random
import xml.etree.ElementTree as ET
import cv2
import cvzone
import numpy as np

# Define accepted image formats
acceptedFormats = ['.jpg', '.png', '.jpeg', '.bmp']
totalBbox = 0

# Utility function to get the color for a given class
def getColorForClass(classId, num_classes):
    # Create color map with proper shape
    colors = cv2.applyColorMap(np.linspace(0, 255, num_classes).astype(np.uint8), cv2.COLORMAP_JET)
    # Access the color properly
    color = tuple(map(int, colors[classId][0]))[::-1]
    return color

# Function to draw bounding boxes on images annotated in YOLO format
def drawBoxesYOLO(imagePath, fileExtension, class_names):
    global totalBbox
    img = cv2.imread(imagePath)
    if img is None:
        print(f"Warning: Could not read image {imagePath}")
        return None
    
    h, w, _ = img.shape
    txt_path = imagePath.replace(fileExtension, ".txt")
    
    if not os.path.exists(txt_path):
        print(f"Warning: Annotation file {txt_path} not found")
        return img
    
    with open(txt_path, 'r') as f:
        lines = f.readlines()

        # PRINT LABEL FILE CONTENTS
        print(f"\n--- {os.path.basename(txt_path)} ---")
        for i, line in enumerate(lines):
            print(f"  {line.strip()}")

        for line in lines:
            totalBbox += 1
            parts = line.strip().split()
            if len(parts) != 5:
                continue
            
            classId, xCenter, yCenter, width, height = map(float, parts)
            classId = int(classId)
            
            if classId >= len(class_names):
                print(f"Warning: classId {classId} out of range (max {len(class_names)-1})")
                continue
                
            xmin = int((xCenter - width / 2) * w)
            ymin = int((yCenter - height / 2) * h)
            xmax = int((xCenter + width / 2) * w)
            ymax = int((yCenter + height / 2) * h)

            color = getColorForClass(classId, len(class_names))
            cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color, 4)
            # Show both class ID and name
            label = f"{classId}:{class_names[classId]}"
            cvzone.putTextRect(img, label, (xmin + 10, ymin - 10))

    return img

# Function to draw bounding boxes on images annotated in VOC format
def drawBoxesVOC(imagePath, fileExtension, class_names):
    img = cv2.imread(imagePath)
    if img is None:
        print(f"Warning: Could not read image {imagePath}")
        return None
    
    xml_path = imagePath.replace(fileExtension, ".xml")
    
    if not os.path.exists(xml_path):
        print(f"Warning: Annotation file {xml_path} not found")
        return img
        
    tree = ET.parse(xml_path)
    root = tree.getroot()

    for obj in root.findall("object"):
        class_name = obj.find("name").text
        if class_name not in class_names:
            print(f"Warning: Class '{class_name}' not in class_names list")
            continue
            
        classId = class_names.index(class_name)

        bndbox = obj.find("bndbox")
        xmin = int(bndbox.find("xmin").text)
        ymin = int(bndbox.find("ymin").text)
        xmax = int(bndbox.find("xmax").text)
        ymax = int(bndbox.find("ymax").text)

        color = getColorForClass(classId, len(class_names))
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color, 4)
        cvzone.putTextRect(img, class_name, (xmin + 10, ymin - 10))

    return img

# Function to display a subset or navigate through all the dataset images
def displayDetectionDatasetSamples(dataFolder, annotationType="YOLO", imagesToDisplay=50, scale=0.3, imagesPerCol=5, class_names=None):
    allImages = [f for f in os.listdir(dataFolder) if any(f.endswith(ext) for ext in acceptedFormats)]

    if not class_names:
        print("Warning: Class names list is empty. No class names will be displayed.")
        return

    # Mode 1: Display a random set of annotated images
    if imagesToDisplay:
        selectedImages = random.sample(allImages, min(imagesToDisplay, len(allImages)))
        imageList = []

        for imgFile in selectedImages:
            imagePath = os.path.join(dataFolder, imgFile)
            fileExtension = os.path.splitext(imgFile)[1]

            if annotationType == "YOLO":
                img = drawBoxesYOLO(imagePath, fileExtension, class_names)
            elif annotationType == "VOC":
                img = drawBoxesVOC(imagePath, fileExtension, class_names)
            
            if img is not None:
                imageList.append(img)

        if imageList:
            # Stack and display the selected images
            imgStacked = cvzone.stackImages(imageList, imagesPerCol, scale)
            cv2.imshow('Stacked Images', imgStacked)
            cv2.waitKey(0)
        else:
            print("No valid images to display")

    # Mode 2: Navigate through each image one by one
    else:
        idx = 0
        while idx < len(allImages):
            imgFile = allImages[idx]
            imagePath = os.path.join(dataFolder, imgFile)
            fileName, fileExtension = os.path.splitext(imgFile)

            if annotationType == "YOLO":
                img = drawBoxesYOLO(imagePath, fileExtension, class_names)
            elif annotationType == "VOC":
                img = drawBoxesVOC(imagePath, fileExtension, class_names)
            
            if img is None:
                idx += 1
                continue

            print(f"[{idx+1}/{len(allImages)}] {fileName}")
            cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Image", 800, 600)
            cv2.imshow("Image", img)
            key = cv2.waitKey(0)
            # Navigation controls
            if key == ord('d'):  # Delete image and annotation
                try:
                    os.remove(imagePath)
                    if annotationType == "YOLO":
                        os.remove(imagePath.replace(fileExtension, ".txt"))
                    elif annotationType == "VOC":
                        os.remove(imagePath.replace(fileExtension, ".xml"))
                    del allImages[idx]
                except Exception as e:
                    print(f"Error deleting files: {e}")
                    idx += 1
                continue
            elif key == ord(' '):  # Next image
                idx += 1
            elif key == ord('z'):  # Previous image
                idx -= 1

            if idx >= len(allImages):
                break

# Main execution
if __name__ == "__main__":
    displayDetectionDatasetSamples(dataFolder="Data",
                                annotationType="VOC",
                                imagesToDisplay=None,
                                scale=0.3,
                                imagesPerCol=4,
                                class_names=["person"])