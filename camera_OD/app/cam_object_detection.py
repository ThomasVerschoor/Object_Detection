# import the opencv library
import sys
import time

import cv2

# define a video capture object
from PIL import Image

from ModelLoader import ModelLoader
from PostProcessor import PostProcessor
from preprocess import PreProcessor

[script, onnxmodel] = sys.argv

vid = cv2.VideoCapture(0)
model_loader = ModelLoader(onnxmodel)
while (True):

    # Capture the video frame
    # by frame
    ret, frame = vid.read()
    # Display the resulting frame
    cv2.imshow('frame', frame)
    img = Image.fromarray(frame)
    preprocessor = PreProcessor(0, img)
    img_data = preprocessor.preprocess()

    # print("---------------------------------------------")
    # load a simple model
    session = model_loader.load_session(1)
    begin = time.time()

    # see the input name and shape
    input_name = session.get_inputs()[0].name
    # print(session.get_inputs()[0])
    resboxes = session.run([session.get_outputs()[0].name], {input_name: img_data})
    reslabels = session.run([session.get_outputs()[1].name], {input_name: img_data})
    resscores = session.run([session.get_outputs()[2].name], {input_name: img_data})
    # resmasks = session.run([session.get_outputs()[3].name], {input_name: img_data})

    postprocessor = PostProcessor()
    postprocessor.make_json(img, resboxes[0], reslabels[0], resscores[0])
    end = time.time()

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
