import math

from sklearn.cluster import KMeans
from sklearn.cluster import OPTICS
from sklearn.cluster import DBSCAN
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import Birch

import numpy as np


class Processor_Clustering:

    def __init__(self,plotlistArray,scaling):
        self.plotlistArray = plotlistArray
        self.scaling = scaling

    def applyClustering(self,cluster_model,variable):

        # kmeans clustering
        if cluster_model == "kmeans":
            number_of_clusters = variable
            clustermodel = KMeans(n_clusters=number_of_clusters)

        # agglomerative Clustering
        elif cluster_model == "agglomerative":
            number_of_clusters = variable
            clustermodel = AgglomerativeClustering(number_of_clusters, affinity='euclidean', linkage='ward')

        # agglomerative clustering 2
        elif cluster_model == "agglomerative2":
            dist_treshold = variable
            clustermodel = AgglomerativeClustering(None, distance_threshold=dist_treshold, linkage='single')

        elif cluster_model == "DBSCAN":
            eps = variable
            clustermodel = DBSCAN(eps=eps)

        elif cluster_model == "BIRCH":
            threshold = variable
            clustermodel = Birch(threshold=threshold)

        elif cluster_model == "OPTICS":
            maxeps = variable
            clustermodel = OPTICS(max_eps=maxeps)


        else:
            print("Cluster Model Error")

        # fit
        clustermodel.fit(self.plotlistArray)

        return clustermodel

    def calculate(self,clustermodel):

        # calculate bounding boxes and centers
        boundingboxes = []
        clustercenters = []

        # iterate over all clusters
        for numbclust in range(max(clustermodel.labels_)+1):

            # have lists for coordinates and distances
            x_coordinates = []
            y_coordinates = []
            distances = []

            #print("number of cluster " + str(numbclust))

            # iterate over the clusters
            for i in range(len(clustermodel.labels_)):

                # if cluster belongs to certain cluster
                if numbclust == clustermodel.labels_[i]:

                    # append its coordinates
                    x_coordinates.append(self.plotlistArray[i][0])
                    y_coordinates.append(self.plotlistArray[i][1])

                    # calculate the total sum of coordinates
                    totalx = sum(x_coordinates)
                    totaly = sum(y_coordinates)

            # calculate the mean coordinates
            meanx = totalx / len((x_coordinates))
            meany = totaly / len((y_coordinates))

            # append the mean x and y coordinate to the clustercenters array
            clustercenters.append([meanx, meany])
            #print(clustercenters)

            # take absolute values since we do have to work with distances
            absolute_center = np.absolute(clustercenters[numbclust])
            #print(absolute_center)

            # calculate the distance to the center
            mean_distance = (math.sqrt((absolute_center[0] ** 2 + absolute_center[1] ** 2)))/self.scaling
            print("Mean distance to cluster "+str(numbclust)+" : " + str(mean_distance) + " [m]")

            # get the maximum and minimum x and y coordinates
            maximum_x = max(x_coordinates)
            minimum_x = min(x_coordinates)
            maximum_y = max(y_coordinates)
            minimum_y = min(y_coordinates)

            # loop over the points to get distances
            for i in range(len(x_coordinates)):
                distance_to_point = math.sqrt((x_coordinates[i] ** 2 + y_coordinates[i] ** 2))
                distances.append(distance_to_point)

            # calculate the minimal distance
            minimal_distance = (min(distances))/self.scaling

            # show minimal distance
            print("Minimal distance to cluster "+str(numbclust)+" : " + str(minimal_distance) + " [m]")

            # make bounding box
            boundingboxes.append([numbclust, minimum_x, minimum_y, maximum_x - minimum_x, maximum_y - minimum_y,minimal_distance,mean_distance])


        return boundingboxes

