# https://rahulbhadani.medium.com/reading-ros-messages-from-a-bagfile-in-python-b006538bb520

import bagpy
from bagpy import bagreader
import pandas as pd
import seaborn as sea
import matplotlib.pyplot as plt
import numpy as np

# read the .bag file given
b = bagreader('lidar_data/test2.bag')

# check the available topics
print(b.topic_table)

csvfiles = []
for t in b.topics:
    data = b.message_by_topic(t)
    csvfiles.append(data)


# to decode specific type
# data = b.message_by_topic('/scan')
data = b.message_by_topic('/rosout')

print("File saved: {}".format(data))

df_imu = pd.read_csv(data)
print(df_imu)

