import csv
import math
import time

import pygame

with open('/home/thomas/Github/Object_Detection/lidar/lidar_data/2020-12-03-17-26-18/scan.csv') as csvfile:
    reader = csv.DictReader(csvfile)

    rowcounter = 0
    columncounter = 0

    # to get values out of csv file
    lidarrange = "ranges_"
    print(lidarrange)

    # number of points captured
    points = 1080



    # iterate over rows
    for row in reader:

        sweeps = []
        list = []

        # iterate over columns
        for x in range(points + 1):
            value = lidarrange + str(x)
            #print(lidarrange + str(x))
            #print(value)
            # print(row[value])
            list.append(row[value])

        sweeps.append(list)
        #print(row['ranges_1'] +" "+ row['ranges_2'])
        rowcounter = rowcounter +1


#print("counted "+ str(rowcounter) + " rows")
print(list)
print(sweeps)
pygame.init()

width = 1000
height = 1000

screen = pygame.display.set_mode([width,height])
running = True
while running:

    pointlist = []


    # Did the user click the window close button?

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white

    screen.fill((0, 0, 0))

    scaling = 80
    #newAngle = 270/points

    angleStart = 0

    startx = width/2
    starty = height/2

    # Draw a solid blue circle in the center

    pygame.draw.circle(screen, (255, 0, 0), (startx, starty), 1)

    anglectr = angleStart

    for r in list:

        coordinates = []

        radian = anglectr * (math.pi / 180)
        #print(str(r) +" at angle of "+str(radian))
        anglectr = anglectr + 0.25

        x = float(scaling)*float(r)*math.cos(radian)
        y = float(scaling)*float(r)*math.sin(radian)

        coordinates.append(x)
        coordinates.append(y)
        #print(angleStart)
        pygame.draw.circle(screen, (0, 255, 0), (x+startx, y+starty), 1)

        pointlist.append(coordinates)
        #time.sleep(0.1)
        pygame.display.flip()

    print(pointlist)
    time.sleep(50)
    # Flip the display



pygame.quit()


