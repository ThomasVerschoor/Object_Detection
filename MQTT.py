# tutorial found on http://www.steves-internet-guide.com/into-mqtt-python-client/
# adapted

import paho.mqtt.client as mqtt
import time


class MQTT():

    def __init__(self,broker_address,topic,qos):
        print("---------------------------------------")
        print("Creating new MQTT Instance")

        # get broker address
        self.broker_address = broker_address
        print("Instance created on address of broker: " + broker_address)

        # get the topic subscribed/published to
        self.topic = topic
        print("Topic: "+topic)

        #set the qos
        self.qos = qos
        print("Quality of Service: "+str(qos))



    def sendMessage(self,message):

        print("---------------------------------------")
        client = mqtt.Client("P1")  # create new instance

        # connect to broker
        client.connect(self.broker_address)  # connect to broker

        # Publish message to:
        print("Publishing message to topic :"+ self.topic)
        client.publish(self.topic, message,self.qos)

        # wait
        time.sleep(1)



    def receiveMessage(self):
        print("---------------------------------------")
        print("Subscribed to topic: " + self.topic)

        client = mqtt.Client("P1")
        #client.subscribe(self.topic)

        # TODO write message receiving code



# syntax on how to send message on MQTT

"""
client1 = MQTT("broker.mqttdashboard.com","smartcam",2)
client1.sendMessage("test")
client1.sendMessage("test2")
client1.sendMessage("test3")
client1.sendMessage("test4")
client1.sendMessage("test5")
client1.sendMessage("test6")
"""



#client1.receiveMessage()




"""


def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
########################################


broker_address="broker.mqttdashboard.com"

print("creating new instance")
client = mqtt.Client("P1") #create new instance
#client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker
#client.loop_start() #start the loop
print("Subscribing to topic","house/bulbs/bulb1")
#client.subscribe("house/bulbs/bulb1")
print("Publishing message to topic","house/bulbs/bulb1")
client.publish("smartcam","lel")
time.sleep(4) # wait
client.loop_stop() #stop the loop
"""