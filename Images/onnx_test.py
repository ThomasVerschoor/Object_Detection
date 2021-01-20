"""
Followed this tutorial
https://thenewstack.io/tutorial-accelerate-ai-at-edge-with-onnx-runtime-and-intel-neural-compute-stick-2/
Made adaptions to make it work

"""

# import cv2 to capture frames
import time

import cv2
import numpy as np
import onnxruntime as rt

from MQTT import MQTT

# preprocess the frame
from watershed_segmentation import watershed_segmentation


def preprocess(msg):

    #print(msg)

    # array of lengt msg
    inp = np.array(msg).reshape((len(msg), 1))
    #print(inp)
    frame = cv2.imdecode(inp.astype(np.uint8), 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.array(frame).astype(np.float32)
    frame = cv2.resize(frame, (416, 416))
    frame = frame.transpose(2, 0, 1)
    frame = np.reshape(frame, (1, 3, 416, 416))
    return frame


def infer(frame, sess, conf_threshold,labels_path):
    # input_name = sess.get_inputs()[0].name
    output = sess.get_outputs()[0]
    # print(output)
    output = {}

    def softmax(x):
        return np.exp(x) / np.sum(np.exp(x), axis=0)

    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    # pred = sess.run(None, {input_name: frame})
    pred = sess.run([sess.get_outputs()[0].name], {sess.get_inputs()[0].name: frame })

    pred = np.array(pred[0][0])



    labels_file = open(labels_path)
    labels = labels_file.read().split(",")

    tiny_yolo_cell_width = 13
    tiny_yolo_cell_height = 13
    num_boxes = 5
    tiny_yolo_classes = 20


    # loop over image width
    for bx in range(0, tiny_yolo_cell_width):

        # loop over image height
        for by in range(0, tiny_yolo_cell_height):

            # maximum of x boxes
            for bound in range(0, num_boxes):
                channel = bound * 25
                tx = pred[channel][by][bx]
                ty = pred[channel + 1][by][bx]
                tw = pred[channel + 2][by][bx]
                th = pred[channel + 3][by][bx]
                tc = pred[channel + 4][by][bx]



                confidence = sigmoid(tc)
                class_out = pred[channel + 5:channel + 5 + tiny_yolo_classes][bx][by]
                class_out = softmax(np.array(class_out))
                class_detected = np.argmax(class_out)
                display_confidence = class_out[class_detected] * confidence
                #if display_confidence & gt; conf_threshold:

                # print(display_confidence)
                # print(conf_threshold)


                if display_confidence > conf_threshold:
                    output['object'] = labels[class_detected]
                    output['confidence'] = display_confidence
                    #print("box predicted: [" + str(tx) + ", " + str(ty) + ", " + str(tw) + ", " + str(th) + "]")


    return output


def input_video():
    # print("video chosen")

    cap = cv2.VideoCapture('/home/thomas/Downloads/Diana_Cropped_29.mp4')

    return cap

def input_photo():
    # print("photo chosen")

    frame = cv2.imread('/home/thomas/Downloads/bill_gates.jpeg', 0)
    return frame

def input_cam():
    # print("camerastream chosen")

    # index of camera
    cam = 0

    # set up videocapture from webcam
    cap = cv2.VideoCapture(cam)

    return cap


def main():

    input_type = input("Enter your input type: ")
    print(input_type)


    if (input_type=="video"):
        cap = input_video()

    if (input_type=="cam"):
        cap = input_cam()


    # set a confidence threshold
    conf_threshold = 0.01

    # inference Model.onnx (downloaded)
    model ="models/Model.onnx"
    sess = rt.InferenceSession(model)

    # print("splitted string")
    # print(model.split(".")[0])

    labels_path = model.split(".")[0] + "_labels.txt"
    # print(labels_path)

    MQTT_Connect = "OFF"
    img_Segmentation = "ON"


    if (MQTT_Connect == "ON"):

    # import mqtt
        client1 = MQTT("broker.mqttdashboard.com", "smartcam", 2)

    while (True):

        # wait for 5 milliseconds
        cv2.waitKey(5)

        if (input_type == "video" or input_type == "cam"):

            # capture frame by frame
            # ret will return a boolean (True of False), wether frame is read correctly
            ret, frame = cap.read()

        # show the frame


        if (input_type == "photo"):
            frame = input_photo()
            # frame = cv2.imread('/home/thomas/Downloads/diningtable.jpg', 0)

            #segm = watershed_segmentation(frame)
            #segm.segment()


        cv2.imshow('frame', frame)
        #time.sleep(1)

        # return a single-row matrix
        # imencode makes from a 3 dimensional matrix to single column rows
        ret, enc = cv2.imencode('.jpg', frame)
        # print(ret, enc)

        # make one list [a b c d e]
        # flatten will change your rows of 1 column to columns of 1 row
        enc = enc.flatten()
        # print(enc)

        # preprocess this data
        fr = preprocess(enc.tolist())
        # infer
        p = infer(fr, sess, conf_threshold,labels_path)

        # print(len(p))
        # print only if there is an object detected
        if not len(p) == 0:

            print(p)

            if(MQTT_Connect == "ON"):



                client1.sendMessage(str(p))


"""
    if (input_type == "photo"):

        while(True):

            print("photo processing")

            cv2.imshow('frame',cv2.imread('/home/thomas/Downloads/bill_gates.jpeg', 0))



            # return a single-row matrix
            # imencode makes from a 3 dimensional matrix to single column rows
            ret, enc = cv2.imencode('.jpg', frame2)
            # print(ret, enc)

            # make one list [a b c d e]
            # flatten will change your rows of 1 column to columns of 1 row
            enc = enc.flatten()
            # print(enc)

            # preprocess this data
            fr = preprocess(enc.tolist())
            # infer
            p = infer(fr, sess, conf_threshold)

            # print(len(p))
            # print only if there is an object detected
            if not len(p) == 0:
                print(p)
                # client1.sendMessage(str(p))
            # print(p)

    if (input_type == "cam" or input_type == "video"):

        while (True):

            # wait for 5 milliseconds
            cv2.waitKey(5)

            # capture frame by frame
            # ret will return a boolean (True of False), wether frame is read correctly
            ret, frame = cap.read()

            # show the frame

            cv2.imshow('frame',frame)
            time.sleep(1)

            # return a single-row matrix
            # imencode makes from a 3 dimensional matrix to single column rows
            ret, enc = cv2.imencode('.jpg', frame)
            # print(ret, enc)

            # make one list [a b c d e]
            # flatten will change your rows of 1 column to columns of 1 row
            enc = enc.flatten()
            # print(enc)

            # preprocess this data
            fr = preprocess(enc.tolist())
            # infer
            p = infer(fr, sess, conf_threshold)


            #print(len(p))
            # print only if there is an object detected
            if not len(p) == 0:
                print(p)


                #client1.sendMessage(str(p))
            #print(p)


"""

"""
    
    To make it more clean code:
    
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    """

if __name__ == "__main__":
    main()