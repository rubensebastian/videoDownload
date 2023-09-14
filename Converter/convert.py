# import image files
# determine image dimensions and generate blank image
# import XML and python XML library
# import video manipulation library
# create video object
# append images as frames to video
# keep repeating images based on durations pulled from XML file

# NOTE: intended to be run from a shell script, as a number of folders already have their slides in mp4 format

import cv2
import math
import sys
import re
import xml.etree.ElementTree as ET
from pathlib import Path
import imageio.v3 as iio
import os
os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/cellar/ffmpeg/6.0_1/bin/ffmpeg"


# NOTE: path to slides is: root[1][4][0][8][0][7][19] and iterate over children
# NOTE: child[0] is slide number
# NOTE: child[1] is time in milliseconds since start of video

folder_path = sys.argv[1]

folder_path_split = folder_path.split("/")
folder_path_split[len(folder_path_split) - 1] = "MediasitePresentation_70.xml"
xml_path = "/".join(folder_path_split)

tree = ET.parse(xml_path)
root = tree.getroot()

# get length of presentation video to know how long to extend final slide
for file in Path(folder_path).iterdir():
    if Path(file).suffix == ".mp4" and re.search("^._", Path(file).stem) == None:
        video = cv2.VideoCapture(folder_path + "/" + file.name)

        frames_per_second = math.floor(video.get(cv2.CAP_PROP_FPS))
        frame_count = math.floor(video.get(cv2.CAP_PROP_FRAME_COUNT))
        video_total_runtime = math.floor(frame_count / frames_per_second)
        break

images = []
for index, child in enumerate(root[1][4][0][8][0][7][19]):
    slide_number = child[0].text

    slide_first_frame = 0 if index == 0 else math.floor(
        int(child[1].text) * frames_per_second / 1000)
    slide_last_frame = int(video_total_runtime * 15) if index == len(
        root[1][4][0][8][0][7][19]) - 1 else math.floor(int(root[1][4][0][8][0][7][19][index+1][1].text) * frames_per_second / 1000)

    while len(slide_number) < 4:
        slide_number = "0" + slide_number

    img_path = folder_path + "/slide_" + slide_number + "_full.jpg"
    current_img = iio.imread(img_path)

    for frame in range(slide_first_frame, slide_last_frame):
        images.append(current_img)

iio.imwrite(folder_path + '/slides.mp4', images, fps=frames_per_second)
with open('Converter/finished.txt', 'w') as f:
    f.write(folder_path.split("/")[len(folder_path_split) - 1])
    f.write("\n")