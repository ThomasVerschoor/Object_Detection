# https://thenewstack.io/tutorial-using-a-pre-trained-onnx-model-for-inferencing/

import json
import sys
import os
import time
import numpy as np
import cv2
import onnx
import onnxruntime
from onnx import numpy_helper


# model_dir = "./mnist"

model_dir = "/home/thomas/Documents/Object_Detection/Object_Detection/mnist"

model = model_dir + "/model.onnx"
# path = sys.argv[1]

# index of camera
cam = 4

# set up videocapture from webcam
cap = cv2.VideoCapture(cam)


while(True):
    # wait for 5 milliseconds
    cv2.waitKey(5)



    ret, img = cap.read()

    # cv2.imshow('frame', img)

    # Preprocess the image
    img = cv2.imread("/home/thomas/Downloads/cijfer4.jpg")
    cv2.imshow('frame', img)

    # print(img)
    # print(img[..., :3])

    img = np.dot(img[..., :3], [0.299, 0.587, 0.114])

    # print(img)

    img = cv2.resize(img, dsize=(28, 28), interpolation=cv2.INTER_AREA)
    img.resize((1, 1, 28, 28))

    # print(img)

    data = json.dumps({'data': img.tolist()})
    # print(data)
    data = np.array(json.loads(data)['data']).astype('float32')

    # print(data)
    session = onnxruntime.InferenceSession(model, None)
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    # print(input_name)
    # print(output_name)

    result = session.run([output_name], {input_name: data})
    #print({input_name: data})
    #print(result)
    #print(np.array(result).squeeze())
    prediction = int(np.argmax(np.array(result).squeeze(), axis=0))
    print(prediction)