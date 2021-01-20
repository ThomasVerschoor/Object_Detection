import json
import numpy as np
import matplotlib.pyplot as plt
# import cv2
# pip install opencv-python
import matplotlib.patches as patches


class PostProcessor:
    def __init__(self):
        self.classes = [line.rstrip('\n') for line in open('Models/coco_labels.txt')]

    def display_objdetect_image(self, image, boxes, labels, scores, score_threshold=0.7):
        ratio = 800.0 / min(image.size[0], image.size[1])
        boxes /= ratio

        _, ax = plt.subplots(1, figsize=(12, 9))
        image = np.array(image)
        ax.imshow(image)

        # Showing boxes with score > 0.7
        for box, label, score in zip(boxes, labels, scores):
            if score > score_threshold:
                rect = patches.Rectangle((box[0], box[1]), box[2] - box[0], box[3] - box[1], linewidth=1, edgecolor='b',
                                         facecolor='none')
                ax.annotate(self.classes[label] + ':' + str(np.round(score, 2)), (box[0], box[1]), color='w',
                            fontsize=12)
                ax.add_patch(rect)
        plt.show()

    def make_json(self, image, boxes, labels, scores, score_threshold=0.7):

        # print(boxes.shape[1])
        # print(boxes.shape[2])
        # print(boxes.shape[3])
        # print(boxes.shape[4])

        ratio = 800.0 / min(image.size[0], image.size[1])
        boxes = boxes / ratio

        # _, ax = plt.subplots(1, figsize=(12, 9))

        # image = np.array(image)
        data = []

        for box, label, score in zip(boxes, labels, scores):
            # Showing boxes with score > 0.7
            if score <= score_threshold:
                continue
            x1 = float(box[0])
            y1 = float(box[1])
            x2 = float(box[2])
            y2 = float(box[3])
            # print("mid point")
            # print((x_mid, y_mid))
            data.append({self.classes[label]: [{'x': x1}, {'y': y1}, {'width': x2-x1}, {'height': y2-y1}]})
            # mid point formula x: x1+ (x2-x1)/2
            # mid point formula y: y1 + (y2-y1)/2
        print(data)
        with open('data.txt', 'w') as outfile:
            json.dump(data, outfile)

        # ax.imshow(image)
        # plt.show()
