import csv
import json
import math
import time

import numpy as np
from pydust import core

class PreProcessor:

    def __init__(self,scaling):
        self.scaling = scaling

    def sendUsingDust(self,message):


        #print("sending using dust "+str(message))

        #print(len(message))

        msgtosend = ""

        for clusters in message:
            print(clusters[0])
            numb = '{ "number_of_cluster":'+str(clusters[0])+'}'
            msg = json.loads(numb)
            x = {"x":str(clusters[1])}
            msg.update(x)
            y = {"y": str(clusters[2])}
            msg.update(y)
            w = {"w": str(clusters[3])}
            msg.update(w)
            h = {"h": str(clusters[4])}
            msg.update(h)
            distme = {"mean_distance": str(clusters[5])}
            msg.update(distme)
            distmi = {"mimimal_distance": str(clusters[6])}
            msg.update(distmi)

            msgtosend = msgtosend + json.dumps(msg)
            #jason= json.dumps(clusters)
            #print(jason)

        print(msgtosend)


        # initialises the core with the given block name and the directory where the modules are located (default "./modules")
        dust = core.Core("mqtt_publisher", "/home/thomas/Github/Object_Detection/modules")

        # start a background thread responsible for tasks that shouls always be running in the same thread
        dust.cycle_forever()

        # load the core, this includes reading the libraries in the modules directory to check addons and transports are available
        dust.setup()

        # set the path to the configuration file
        dust.set_configuration_file("/home/thomas/Github/Object_Detection/configuration.json")

        # connects all channels
        dust.connect()




        for x in range(1):
            time.sleep(1)

            # declare a bytes-like payload object
            payload = msgtosend.encode("ascii")

            # publishes the payload to the given channel (as defined by the configuration file)
            dust.publish("publish-mqtt", payload)

        time.sleep(1)

        # disconnects all channels and flushes the addon stack and transport.
        dust.disconnect()

        # stops the background thread started by cycleForever() and wait until the thread has finished its tasks before exiting the application
        dust.cycle_stop()



    def receiveUsingDust(self):
        print("Using dust to receive ")

        # initialises the core with the given block name and the directory where the modules are located (default "./modules")
        dust = core.Core("mqtt_subscriber", "/home/thomas/Github/Object_Detection/modules")

        # start a background thread responsible for tasks that shouls always be running in the same thread
        dust.cycle_forever()

        # load the core, this includes reading the libraries in the modules directory to check addons and transports are available
        dust.setup()

        # set the path to the configuration file
        dust.set_configuration_file("/home/thomas/Github/Object_Detection/configuration.json")

        # connects all channels
        dust.connect()

        # add a message listener on the subscribe-tcp channel. The callback function takes a bytes-like object as argument containing the payload of the message
        print("test2")
        #dust.register_listener("subscribe-mqtt", self.receive)
        print("test3")
        #dust.register_listener("subscribe-mqtt", lambda payload: print("Received payload with %d bytes" % len(payload)))
        dust.register_listener("subscribe-mqtt", lambda payload: print("Received payload with message: "+str(payload)))

        while True:
            time.sleep(1)


    def processCSV(self,path):

        with open(path) as csvfile:
            reader = csv.DictReader(csvfile)

            rowcounter = 0

            # to get values out of csv file
            lidarrange = "ranges_"
            # print(lidarrange)

            # number of points captured
            points = 1080

            # iterate over rows
            for row in reader:

                sweeps = []
                list = []

                # iterate over columns
                for x in range(points + 1):
                    value = lidarrange + str(x)
                    # print(lidarrange + str(x))
                    # print(value)
                    # print(row[value])
                    list.append(row[value])

                sweeps.append(list)
                # print(row['ranges_1'] +" "+ row['ranges_2'])
                rowcounter = rowcounter + 1

            #print("counted "+ str(rowcounter) + " rows")
            #print(len(list))
            #print(len(sweeps))

            return list;

    def convertToEuclidean(self,list):

        # get list for polar points
        pointlist = []

        # set starting angle to zero
        angleStart = 0

        # angle increment
        anglectr = angleStart

        # loop over list
        for r in list:

            # append coordinates
            coordinates = []

            # calculate the angle in radian
            radian = anglectr * (math.pi / 180)
            # print(str(r) +" at angle of "+str(radian))

            # increment the angle
            anglectr = anglectr + 0.25

            # calculate the x and y coordinates
            x = float(self.scaling)*float(r) * math.cos(radian)
            y = float(self.scaling)*float(r) * math.sin(radian)

            # append x and y to coorindates
            coordinates.append(x)
            coordinates.append(y)

            # append coordinates to the list
            pointlist.append(coordinates)

        # return pointlist
        return pointlist

    def prepareArray(self,pointlist):

        # start with empty list
        plotlist = []

        # loop over the list
        for point in range(len(pointlist)):

            # convert values in tuple to int
            x = int(pointlist[point][0])
            y = int(pointlist[point][1])

            # bring them back together
            intcoordinates = []

            intcoordinates.append(x)
            intcoordinates.append(y)
            # print(intcoordinates)

            # append them to the plotlist
            plotlist.append(intcoordinates)

        plotlistArray = np.asarray(plotlist)

        return plotlistArray