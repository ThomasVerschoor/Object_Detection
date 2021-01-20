"""

FINAL

"""

import csv
import math
import time
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering

from matplotlib.patches import Rectangle

number_of_clusters = 99


#import pygame

with open('/home/thomas/Github/Object_Detection/lidar/lidar_data/2020-12-03-17-26-18/scan.csv') as csvfile:
    reader = csv.DictReader(csvfile)

    rowcounter = 0
    columncounter = 0

    # to get values out of csv file
    lidarrange = "ranges_"
    #print(lidarrange)

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
#print(list)
#print(sweeps)
#pygame.init()

width = 1000
height = 1000

#screen = pygame.display.set_mode([width,height])
running = True
#while running:

pointlist = []
scaling = 80
    #newAngle = 270/points

angleStart = 0

startx = width/2
starty = height/2

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
        #pygame.draw.circle(screen, (0, 255, 0), (x+startx, y+starty), 1)

    pointlist.append(coordinates)

#print(pointlist)
    #time.sleep(50)
    # Flip the display

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#print(cluster.labels_)

#print(len(pointlist))

plotlist = []
"""
X = np.array([[5,3],
    [10,15],
    [15,12],
    [24,10],
    [30,30],
    [85,70],
    [71,80],
    [60,78],
    [70,55],
    [80,91],])
    """

#cluster.fit_predict(X)

for point in range(len(pointlist)):

    #convert values in tuple to int
    x = int(pointlist[point][0])
    y = int(pointlist[point][1])

    #bring them back together
    intcoordinates =[]

    intcoordinates.append(x)
    intcoordinates.append(y)
    #print(intcoordinates)
    plotlist.append(intcoordinates)


plotlistArray = np.asarray(plotlist)

print(plotlistArray)

#print(plotlistArray)

###################################################
# Apply clustering / choose clustering model
###################################################

cluster_model = "agglomerative2"

#kmeans clustering
if cluster_model == "kmeans":
    clustermodel = KMeans(n_clusters=number_of_clusters)

# about agglomerative clustering: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html

#agglomerative Clustering
elif cluster_model =="agglomerative":
    clustermodel = AgglomerativeClustering(number_of_clusters,affinity='euclidean',linkage='ward')

#agglomerative clustering 2
elif cluster_model =="agglomerative2":
    clustermodel = AgglomerativeClustering(None,distance_threshold=25,linkage='single')

else:
    print("Cluster Model Error")


######################################################
# cluster processing
######################################################

#fit kmean
clustermodel.fit(plotlistArray)


print(plotlistArray)

#plot points
plt.scatter(plotlistArray[:,0],plotlistArray[:,1], c=clustermodel.labels_, cmap='rainbow')


boundingboxes = []
clustercenters = []

#print(clustermodel.cluster_centers_)

# iterate over all clusters
for numbclust in range(number_of_clusters):

    x_coordinates = []
    y_coordinates = []
    afstanden = []

    print("number of cluster "+str(numbclust))

    for i in range (len(clustermodel.labels_)):

        #print(i)

        if numbclust == clustermodel.labels_[i]:
            #print(X[i])
            #print(X[i][0])
            x_coordinates.append(plotlistArray[i][0])
            y_coordinates.append(plotlistArray[i][1])

            totaalx = sum(x_coordinates)
            totaaly = sum(y_coordinates)

    gemiddeldex = totaalx/len((x_coordinates))
    gemiddeldey = totaaly / len((y_coordinates))
    #print(gemiddeldex)
    #print(gemiddeldey)

    clustercenters.append([gemiddeldex, gemiddeldey])
    #print(clustermodel.cluster_centers_)



    """
    # print(kmeans.cluster_centers_[numbclust])
    absolute_center = np.absolute(clustermodel.cluster_centers_[numbclust])
    # print(absolute_center)

    gemiddelde_afstand = math.sqrt((absolute_center[0]**2+absolute_center[1]**2))
    # print(gemiddelde_afstand)
    gemiddelde_afstand_real = gemiddelde_afstand/scaling
    print(gemiddelde_afstand_real)
    """
    # print(kmeans.cluster_centers_[numbclust])
    absolute_center = np.absolute(clustercenters[numbclust])
    # print(absolute_center)

    gemiddelde_afstand = math.sqrt((absolute_center[0] ** 2 + absolute_center[1] ** 2))
    # print(gemiddelde_afstand)
    gemiddelde_afstand_real = gemiddelde_afstand / scaling
    print("gemiddelde afstand tot cluster = " + str(gemiddelde_afstand_real)+" [m]")


    maximum_x = max(x_coordinates)
    minimum_x = min(x_coordinates)

    maximum_y = max(y_coordinates)
    minimum_y = min(y_coordinates)


    for i in range (len(x_coordinates)):
        afstand_naar_punt = math.sqrt((x_coordinates[i]**2 + y_coordinates[i]**2))
        afstanden.append(afstand_naar_punt)

    # show all the distances
    #print(afstanden)

    minimale_afstand_real = min(afstanden)/scaling

    # show minimal distance
    print("Minimale afstand naar cluster: "+str(minimale_afstand_real) +" [m]")


    #print(str(minimum_x_distance) + " "+ str(minimum_y_distance))

    #for i in range (len(absolute_x_values)):
    #    if (minimum_x_distance == absolute_x_values[i]):
            #print("MINIMALX")
    #        if(minimum_y_distance == absolute_y_values[i]):
                #print("MINIMALY")
                #print("MINIMALVALUE")



        #print(i)



    #minimale_afstand = math.sqrt((absolute_center[0] ** 2 + absolute_center[1] ** 2))
    # print(gemiddelde_afstand)
    #gemiddelde_afstand_real = gemiddelde_afstand / scaling
    #print("gemiddelde afstand tot cluster = " + str(gemiddelde_afstand_real) + " [m]")


    #print("bounding box ["+str(minimum_x)+" "+str(maximum_x) +" "+str(minimum_y)+" "+str(maximum_y)+"]")
    boundingboxes.append([numbclust,minimum_x,minimum_y,maximum_x-minimum_x,maximum_y-minimum_y])

#print(clustercenters)



#print(boundingboxes)
#print("number of bounding boxes found: "+ str(len(boundingboxes)))


for i in boundingboxes:
    #print(i[0])
    plt.gca().add_patch(Rectangle((i[1], i[2]), i[3], i[4], linewidth=1, edgecolor='r', facecolor='none'))
    plt.text(i[1],i[2],'number of cluster '+str(i[0]))


#print(kmeans.labels_)

#print(kmeans.cluster_centers_)

plt.show()


