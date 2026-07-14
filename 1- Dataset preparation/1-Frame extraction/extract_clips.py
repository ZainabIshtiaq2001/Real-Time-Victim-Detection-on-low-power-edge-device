'''
This script will extract frames of particular ranges from .mp4 type videos
Store your videos of mp4 format in Videos folder and change the following accordinly:
    - count: change this for every video to avoid overwriting of frames.
    - ranges: change this according to the time ranges you want to extract frames from.
the extracted frames are stored in Frames folder

'''

import cv2, os

video = r"Videos\video_number.mp4"
out_dir = r"Frames"
os.makedirs(out_dir, exist_ok=True)

cap = cv2.VideoCapture(video)
# make sure to add emty frames if using yolo for further training, helps rdeuce FPs

# times 0:05-0:09, 0:16-0:23, 0:29-0:42, 0:50-0:52,  2:35-2:50
ranges = [ (5, 9), (16, 23), (29, 42), (50, 52), (155, 170) ]
count = 0  #change this count according to last frame to avoid overwriting.
# 1182 current count

for start, end in ranges:
    t = start
    while True:
        if end and t > end:
            
            break

        # set time in milliseconds (NOT frames)
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)

        ret, frame = cap.read()
        if not ret:
            break

        cv2.imwrite(f"{out_dir}\\frame_{count:04d}.jpg", frame)
        count += 1

        t += 1   # EXACTLY 1 second step
     
print("stopped at frame: ", count ) # enter the count output here in count on line 21. change for every video
cap.release()