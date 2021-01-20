import rospy
import cv2 as cv
import numpy as np
import math

from sensor_msgs.msg import LaserScan


def callback(data):

	width = 800
	height = 800

	img = np.zeros((height,width,3),np.uint8)


	cartesianlist =[]

	# indicate new sweep
	print("-------------------------------------------------------------------------------------------------")
	#print (len(data.ranges))

	angleIncrement = 0.25
	currentAngle=0


	scaling = 60
	startx = width/2
	starty = width/2

	# starts with 0, goes over all values
	for x in range(1081):

		coordinates = []
		#print(data.ranges[x])
		#print(currentAngle)
		currentAngle = currentAngle + angleIncrement

		radian = currentAngle*(math.pi/180)

		distance = data.ranges[x]

		x = float(distance)*math.cos(radian)
		y = float(distance)*math.sin(radian)
		
		coordinates.append(x)
		coordinates.append(y)
		cartesianlist.append(coordinates)

		cv.circle(img,(int(scaling*x)+startx,int(scaling*y)+starty),1,(0,255,0),-1)
		cv.imshow('laser',img)
		cv.waitKey(1)

	print(cartesianlist)
		
	#points.append(data.ranges)
	#print(len(points))
#frame = np.zeros((500, 500,3), np.uint8)
    #angle = data.angle_min
    #for r in data.ranges:
        #change infinite values to 0
        #if math.isinf(r) == True:
        #    r = 0
        #convert angle and radius to cartesian coordinates
       # x = math.trunc((r * 30.0)*math.cos(angle + (-90.0*3.1416/180.0)))
       # y = math.trunc((r * 30.0)*math.sin(angle + (-90.0*3.1416/180.0)))

        #set the borders (all values outside the defined area should be 0)
        #if y > 0 or y < -35 or x<-40 or x>40:
        #    x=0
        #    y=0

        #cv2.line(frame,(250, 250),(x+250,y+250),(255,0,0),2)
        #angle= angle + data.angle_increment 
        #cv2.circle(frame, (250, 250), 2, (255, 255, 0))
        #cv2.imshow('frame',frame)
        #cv2.waitKey(1)

def laser_listener():
    	rospy.init_node('laser_listener', anonymous=True)
    	rospy.Subscriber("/scan", LaserScan,callback)
    	rospy.spin()

if __name__ == '__main__':
    	laser_listener()

