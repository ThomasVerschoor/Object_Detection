from Pytorch_export_to_onnx import testfile

# a = testfile()
# a.run()
# a.export()

import onnxruntime
import numpy as np
import time
from onnxruntime.datasets import get_example
import os

# get the directory path till here
dirname = os.path.dirname(__file__)
# print(dirname)

# add the map output and the file we need
filename = os.path.join(dirname, 'output/model.onnx')

# print out the full path to the file
print(filename)

# get the example
example_model = get_example(filename)
sess = onnxruntime.InferenceSession(example_model)

input_name = sess.get_inputs()[0].name
input_shape = sess.get_inputs()[0].shape
input_type = sess.get_inputs()[0].type

print(input_name, input_shape, input_type)

output_name = sess.get_outputs()[0].name
output_shape = sess.get_outputs()[0].shape
output_type = sess.get_outputs()[0].type

print(output_name, output_shape, output_type)

x = np.random.random(input_shape)
x = x.astype(np.float32)

print(sess.get_providers())

sess.set_providers(['CPUExecutionProvider'])
start_time = time.time()
for i in range(1000):
    result = sess.run([output_name], {input_name: x})
end_time = time.time()
time_elapsed = end_time - start_time
print(time_elapsed)

"""
#sess.set_providers(['CUDAExecutionProvider'])
start_time = time.time()
for i in range(1000):
    result = sess.run([output_name], {input_name: x})
end_time = time.time()
time_elapsed = end_time - start_time
print(time_elapsed)
"""
