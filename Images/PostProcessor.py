import json
import numpy as np
import matplotlib.pyplot as plt
import cv2
import matplotlib.patches as patches


class PostProcessor:
    def __init__(self):
        self.classes = [line.rstrip('\n') for line in open('models/coco_classes.txt')]

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
        data = {}

        for box, label, score in zip(boxes, labels, scores):
            # Showing boxes with score > 0.7
            if score <= score_threshold:
                continue

            # Finding contour based on mask
            """
            mask = mask[0, :, :, None]
            int_box = [int(i) for i in box]
            mask = cv2.resize(mask, (int_box[2] - int_box[0] + 1, int_box[3] - int_box[1] + 1))
            mask = mask > 0.5
            im_mask = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
            x_0 = max(int_box[0], 0)
            x_1 = min(int_box[2] + 1, image.shape[1])
            y_0 = max(int_box[1], 0)
            y_1 = min(int_box[3] + 1, image.shape[0])
            mask_y_0 = max(y_0 - box[1], 0)
            mask_y_1 = mask_y_0 + y_1 - y_0
            mask_x_0 = max(x_0 - box[0], 0)
            mask_x_1 = mask_x_0 + x_1 - x_0
            im_mask[int(y_0):int(y_1), int(x_0):int(x_1)] = mask[
                                                            int(mask_y_0): int(mask_y_1), int(mask_x_0): int(mask_x_1)
                                                            ]
            im_mask = im_mask[:, :, None]

            # OpenCV version 4.x
            contours, hierarchy = cv2.findContours(
                im_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
            )

            # image = cv2.drawContours(image, contours, -1, 25, 3)
            # image = cv2.drawContours(image,contours,255,255,255)

            image = cv2.drawContours(image, contours, -1, (0, 255, 0), 3)

            rect = patches.Rectangle((box[0], box[1]), box[2] - box[0], box[3] - box[1], linewidth=1, edgecolor='y',
                                     facecolor='none')
            ax.annotate(self.classes[label] + ':' + str(np.round(score, 2)), (box[0], box[1]), color='b', fontsize=12)
            ax.add_patch(rect)
            print("object detected: " + self.classes[label])
            """
            x1 = float(box[0])
            y1 = float(box[1])
            x2 = float(box[2])
            y2 = float(box[3])
            # print("mid point")
            # print((x_mid, y_mid))
            data.update({self.classes[label]: [{'x': x1}, {'y': y1}, {'width': x2-x1}, {'height': y2-y1}]})
            # mid point formula x: x1+ (x2-x1)/2
            # mid point formula y: y1 + (y2-y1)/2
        print(data)
        with open('data.txt', 'w') as outfile:
            json.dump(data, outfile)

        # ax.imshow(image)
        # plt.show()
