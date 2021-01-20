# imports
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

from matplotlib.patches import Rectangle

number_of_clusters = 5

# get data
X = np.array([[5,3],
     [10,15],
     [15,12],
     [24,10],
     [30,45],
     [85,70],
     [71,80],
     [60,78],
     [55,52],
     [80,91],])



#kmeans clustering
kmeans = KMeans(n_clusters=number_of_clusters)

#fit kmean
kmeans.fit(X)

#plot points
plt.scatter(X[:,0],X[:,1], c=kmeans.labels_, cmap='rainbow')


boundingboxes = []

#print(kmeans.cluster_centers_)

# iterate over all clusters
for numbclust in range(number_of_clusters):

    x_coordinates = []
    y_coordinates = []

    #print("number of cluster "+str(numbclust))

    for i in range (len(kmeans.labels_)):

        #print(i)

        if numbclust == kmeans.labels_[i]:
            #print(X[i])
            #print(X[i][0])
            x_coordinates.append(X[i][0])
            y_coordinates.append(X[i][1])

    maximum_x = max(x_coordinates)
    minimum_x = min(x_coordinates)

    maximum_y = max(y_coordinates)
    minimum_y = min(y_coordinates)

    #print("bounding box ["+str(minimum_x)+" "+str(maximum_x) +" "+str(minimum_y)+" "+str(maximum_y)+"]")
    boundingboxes.append([minimum_x,minimum_y,maximum_x-minimum_x,maximum_y-minimum_y])



print(boundingboxes)
print(len(boundingboxes))

for i in boundingboxes:
    #print(i[0])
    plt.gca().add_patch(Rectangle((i[0], i[1]), i[2], i[3], linewidth=1, edgecolor='r', facecolor='none'))

print(kmeans.labels_)

#print(kmeans.cluster_centers_)

#print(kmeans.cluster_centers_[0])




plt.show()