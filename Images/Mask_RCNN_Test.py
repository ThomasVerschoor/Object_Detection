import numpy as np
#from PIL import Image
from Pillow import Image

from timeit import default_timer as timer
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from ModelLoader import ModelLoader
from PostProcessor import PostProcessor
from preprocess import PreProcessor
import json

model_loader = ModelLoader()
img = Image.open('/home/bilal/Downloads/foto_van_yosra1.jpg')
# print("---------------------------------")
# print("0 for tinyYolo")
# val = input("give your neural network architecture type: ")

preprocessor = PreProcessor(0, img)
img_data = preprocessor.preprocess()

# print("---------------------------------------------")
# load a simple model
session = model_loader.load_session(1)
begin = timer()

# see the input name and shape
input_name = session.get_inputs()[0].name
"""# print("input name = ", input_name)

input_shape = session.get_inputs()[0].shape
# print("input shape =",input_shape)

input_type = session.get_inputs()[0].type
# print("input type", input_type)

# print("---------------------------------------------")

output_name = session.get_outputs()[0].name
# print("output name", output_name)
output_shape = session.get_outputs()[0].shape
# print("output shape", output_shape)
output_type = session.get_outputs()[0].type
# print("output type", output_type)

"""
resboxes = session.run([session.get_outputs()[0].name], {input_name: img_data})
reslabels = session.run([session.get_outputs()[1].name], {input_name: img_data})
resscores = session.run([session.get_outputs()[2].name], {input_name: img_data})
# resmasks = session.run([session.get_outputs()[3].name], {input_name: img_data})

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

# classes = [line.rstrip('\n') for line in open('models/coco_classes.txt')]

"""
print(resboxes[0][0])
print(reslabels[0][0])
print(resscores[0][0])
print(resmasks[0][0][0][0])
"""
postprocessor = PostProcessor()
postprocessor.make_json(img, resboxes[0], reslabels[0], resscores[0])
end = timer()
postprocessor.display_objdetect_image(img, resboxes[0], reslabels[0], resscores[0])
print(end-begin)
# print(res,res1,res2,res3)


# print(res[0],res1[0],res2[0])


# display_objdetect_image(img, res, classes, res2, res3)
