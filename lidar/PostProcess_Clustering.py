import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


class PostProcessor_Clustering:

    def __init__(self):
        pass

    def plot(self,plotlistArray,clustermodel,boundingboxes):
        # plot points
        plt.scatter(plotlistArray[:, 0], plotlistArray[:, 1], c=clustermodel.labels_, cmap='rainbow')

        for i in boundingboxes:
            # print(i[0])
            plt.gca().add_patch(Rectangle((i[1], i[2]), i[3], i[4], linewidth=1, edgecolor='r', facecolor='none'))
            plt.text(i[1], i[2], 'number of cluster ' + str(i[0]))

        plt.show()

