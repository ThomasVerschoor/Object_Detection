import numpy as np
# OpenCV2 for saving an image
import cv2
from PIL import Image

filepath = 'raw_data.txt'
testimage = cv2.imread("testImage.jpg", -1)
print(testimage)

import time

text = []

with open(filepath) as fp:
    line = fp.readline()
    cnt = 1
    while line:
        text.append(line)
        # print("Line {}: {}".format(cnt, line.strip()))

        # time.sleep(1)
        line = fp.readline()
        cnt += 1

seq = text[1].split(":")[1]
secs = text[3].split(":")[1]
nsecs = text[4].split(":")[1]
frame_id = text[5].split(":")[1]
height = int(text[6].split(":")[1])
width = int(text[7].split(":")[1])
encoding = text[8].split(":")[1]
is_bigendian = text[9].split(":")[1]
step = text[10].split(":")[1]

# text format data, this still is a string
data = text[11].split(": [")[1]

# remove last element of string ']'
data = data[:-1]

data = np.fromstring(data, dtype=int, sep=',')

# print(data)
# print(data[1])
# print(len(data))
# print(lel)

# build matrix

# get length of matrix
print(len(data))

# get width of matrix
print(width)

# get height of matrix
print(height)

l = width
h = height

shape = (l, h)
matrix = np.zeros(shape)

# print(matrix)

# matrix[0][0] = 5

# print(matrix)
print(data)
print("-----------------------")
# print(data)
print(len(data))
print(l * h)
counter = 0
for i in range(l):
    for k in range(h):
        matrix[i][k] = int(data[counter])
        counter += 1
depth = cv2.split(testimage)[0]
depth[depth > 800] = 0
depth = depth / 1000.0000
file = open('raw_data_test.txt','w')

file.close()

