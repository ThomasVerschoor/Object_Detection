import numpy as np
import onnxruntime
from PIL import Image


def preprocess(image):
    # Resize
    ratio = 800.0 / min(image.size[0], image.size[1])
    image = image.resize((int(ratio * image.size[0]), int(ratio * image.size[1])), Image.BILINEAR)

    # Convert to BGR
    image = np.array(image)[:, :, [2, 1, 0]].astype('float32')

    # HWC -> CHW
    image = np.transpose(image, [2, 0, 1])

    # Normalize
    mean_vec = np.array([102.9801, 115.9465, 122.7717])
    for i in range(image.shape[0]):
        image[i, :, :] = image[i, :, :] - mean_vec[i]

    # Pad to be divisible of 32
    import math
    padded_h = int(math.ceil(image.shape[1] / 32) * 32)
    padded_w = int(math.ceil(image.shape[2] / 32) * 32)

    padded_image = np.zeros((3, padded_h, padded_w), dtype=np.float32)
    padded_image[:, :image.shape[1], :image.shape[2]] = image
    image = padded_image

    return image

img = Image.open('/home/thomas/Downloads/BMF.png')
img_data = preprocess(img)



print("---------------------------------------------")

model = "/home/thomas/Documents/Object_Detection/Object_Detection/models/MaskRCNN.onnx"

# load a simple model
session = onnxruntime.InferenceSession(model,None)

# see the input name and shape
input_name = session.get_inputs()[0].name
print("input name = ", input_name)

input_shape = session.get_inputs()[0].shape
print("input shape =",input_shape)

input_type = session.get_inputs()[0].type
print("input type", input_type)

print("---------------------------------------------")

output_name = session.get_outputs()[0].name
print("output name", output_name)
output_shape = session.get_outputs()[0].shape
print("output shape", output_shape)
output_type = session.get_outputs()[0].type
print("output type", output_type)


resboxes = session.run([session.get_outputs()[0].name], {input_name: img_data})
reslabels = session.run([session.get_outputs()[1].name], {input_name: img_data})
resscores = session.run([session.get_outputs()[2].name], {input_name: img_data})
resmasks = session.run([session.get_outputs()[3].name], {input_name: img_data})


"""
boxes = session.get_outputs()[0]
labels = session.get_outputs()[1]
scores = session.get_outputs()[2]
masks = session.get_outputs()[3]

print(input_name)
print(boxes)
print(labels)
print(scores)
print(masks)

lol = boxes.name

result = session.run([boxes], {input_name: img_data})

print(result)
"""






print("---------------------------------------------")

import matplotlib.pyplot as plt
import matplotlib.patches as patches

import pycocotools.mask as mask_util
import cv2

classes = [line.rstrip('\n') for line in open('models/coco_classes.txt')]

def display_objdetect_image(image, boxes, labels, scores, masks, score_threshold=0.7):
    # Resize boxes


    #print(boxes.shape[1])
    #print(boxes.shape[2])
    #print(boxes.shape[3])
    #print(boxes.shape[4])

    ratio = 800.0 / min(image.size[0], image.size[1])
    boxes = boxes/ratio

    _, ax = plt.subplots(1, figsize=(12,9))

    image = np.array(image)

    for mask, box, label, score in zip(masks, boxes, labels, scores):
        # Showing boxes with score > 0.7
        if score <= score_threshold:
            continue

        # Finding contour based on mask
        mask = mask[0, :, :, None]
        int_box = [int(i) for i in box]
        mask = cv2.resize(mask, (int_box[2]-int_box[0]+1, int_box[3]-int_box[1]+1))
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
            int(mask_y_0) : int(mask_y_1), int(mask_x_0) : int(mask_x_1)
        ]
        im_mask = im_mask[:, :, None]

        # OpenCV version 4.x
        contours, hierarchy = cv2.findContours(
            im_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )

        #image = cv2.drawContours(image, contours, -1, 25, 3)
        #image = cv2.drawContours(image,contours,255,255,255)
        image = cv2.drawContours(image, contours, -1, (0, 255, 0), 3)

        rect = patches.Rectangle((box[0], box[1]), box[2] - box[0], box[3] - box[1], linewidth=1, edgecolor='y', facecolor='none')
        ax.annotate(classes[label] + ':' + str(np.round(score, 2)), (box[0], box[1]), color='b', fontsize=12)
        ax.add_patch(rect)

    ax.imshow(image)
    plt.show()


#

print(resboxes[0][0])
print(reslabels[0][0])
print(resscores[0][0])
print(resmasks[0][0][0][0])
display_objdetect_image(img, resboxes[0], reslabels[0], resscores[0], resmasks[0])

# print(res,res1,res2,res3)


# print(res[0],res1[0],res2[0])



# display_objdetect_image(img, res, classes, res2, res3)
