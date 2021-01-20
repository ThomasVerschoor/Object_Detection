from PreProcessor import PreProcessor
from Processor_Clustering import Processor_Clustering
from postprocess_lidar import postprocess_lidar

scaling = 100

# define preprocessor to get lidar data
prep = PreProcessor(scaling)

#prep.sendUsingDust()
prep.receiveUsingDust()

"""
# get range and data
ranges_data = prep.processCSV('/home/thomas/Github/Object_Detection/lidar/lidar_data/2020-12-03-17-26-18/scan.csv')



# convert to euclidean notation
ranges_data_euclidean = prep.convertToEuclidean(ranges_data)

# get the array to apply clustering
ranges_data3 = prep.prepareArray(ranges_data_euclidean)

# apply the clustering algorithm
clustering = Processor_Clustering(ranges_data3,scaling)




# depending on the chosen algorithm the second parameter will be number of clusters or theshold
model = clustering.applyClustering("kmeans",8)
#model = clustering.applyClustering("agglomerative",20)
#model = clustering.applyClustering("agglomerative2",30)

# calculate the bounding boxes
bb = clustering.calculate(model)

# start postprocessing of data
plot = postprocess_lidar()

# plot the data
plot.plot(ranges_data3,model,bb)
"""