#########################################################################################################
# Sensor Fusion
#########################################################################################################

import json

# get config
with open("config/camera_config.json")as f:
  camera_config = json.load(f)

# get config
with open("config/lidar_config.json") as f:
  lidar_config = json.load(f)

print("--------------------------------------------------------------------")
print("Camera that will be used for sensor fusion: "+camera_config['name'])
print(camera_config['description'])
print("Lidar that will be used for sensor fusion: "+lidar_config['name'])
print(lidar_config['description'])
print("--------------------------------------------------------------------")


# config, angels can be found in datasheet
# put angles in list to easily add or remove angles
angles = []

lidar_angle = lidar_config['FOV_angle']
camera_angle = camera_config['FOV_angle']

angles.append(lidar_angle)
angles.append(camera_angle)


# calculate differences from center angles
center_angle_lidar = lidar_angle/2
center_angle_camera = camera_angle/2

# print(center_angle_lidar)
# print(center_angle_camera)


# assume x-axis is the direction we have our object
camera_angle_min = 0 - center_angle_camera
camera_angle_max = 0 + center_angle_camera

lidar_angle_min = 0 - center_angle_lidar
lidar_angle_max = 0 + center_angle_lidar

print("Camera angle from "+ str(camera_angle_min) + " to "+ str(camera_angle_max) + " , good for a total range of " +str((camera_angle_max - camera_angle_min)))
print("Lidar angle from "+ str(lidar_angle_min) + " to "+str(lidar_angle_max) + " ,good for a total range of "+str(lidar_angle_max - lidar_angle_min))

# calculate the "bottleneck" for the system, the smallest range
lowest_angle = min(angles)
print("minimum angle is: " + str(lowest_angle))
view_angle = lowest_angle/2

minimum_angle = 0 - view_angle
maximum_angle = 0 + view_angle
print("All sensors will work between " +str(minimum_angle) + " and "+str(maximum_angle))

############################################
# execute object recognition using photo's #
############################################

#Mask_RCNN_Test.py = Mask_RCNN_Test.py()

############################################
# execute clustering with the lidar sensor #
############################################

# lidar_data_bounding_box = lidar_data_bounding_box()

############################################
# find depth detection using RGBD camera   #
############################################

# fuse

print(camera_config["resolution_width"])
print("corresponds to")
print(lidar_config["points"])

