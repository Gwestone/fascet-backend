import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt

import base64
import cv2

import numpy as np
from scipy.spatial import cKDTree
import math

# Generate some random points
points = np.random.rand(int(2500), 2)

# Create a KD-tree from the points
# tree = cKDTree(points)

# Find the index of the nearest neighbor to a given point
# query_point = [0.5, 0.5]
# distance, index = tree.query(query_point)

# print(f"Index of the nearest neighbor to {query_point}: {index}")

for i in range(0, len(points)):
    points[i][0] = math.ceil(points[i][0] * 1920)
    points[i][1] = math.ceil(points[i][1] * 1080)
points = points.astype(int)

assignments = {}

tree = cKDTree(points)

for y in range(0, 1080):
    for x in range(0, 1920):
        distance, index = tree.query([x, y])
        if (not index in assignments):
            assignments[index] = [(x, y)]
        else:
            assignments[index].append((x, y))


def generate_mosaics(b64_string):

    # Decode the Base64 string to a NumPy array
    img_data = base64.b64decode(b64_string)
    np_arr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    img = cv2.resize(img, (1920, 1080), interpolation=cv2.INTER_AREA)
    # plt.imshow(img)


    colors = {}
    for index in assignments:
        color_sum = [0, 0, 0]
        color_count = 0
        for j in assignments[index]:
            val = img[j[1], j[0]]
            color_sum = [color_sum[0] + val[0], color_sum[1] + val[1], color_sum[2] + val[2]]
            color_count += 1

        if (not index in colors):
            colors[index] = [int(math.ceil(color_sum[0] / color_count)),
                             int(math.ceil(color_sum[1] / color_count)),
                             int(math.ceil(color_sum[2] / color_count)),
                             ]

    for index in assignments:
        for j in assignments[index]:
            img[j[1], j[0]] = colors[index]

    # cv2.imshow('image', img)
    # cv2.waitKey(0)

    retval, buffer = cv2.imencode('.jpg', img)
    return base64.b64encode(buffer).decode('utf-8')

