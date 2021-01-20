import numpy as np
import json
f = open('input.txt')
triplets=f.read().split()
for i in range(0,len(triplets)): triplets[i]=triplets[i].split(',')
A=np.array(triplets, dtype=np.uint8)




#get number of elements
number_of_elements = A.size

#get number of elements in row
number_of_rows = A[0].size

#get number of columns
number_of_columns = int(A.size/A[0].size)

#check whether the matrix was initialized well

if(number_of_columns*number_of_rows == number_of_elements):
    pass
    #print("OK")
else:
    pass
    #print("error")

#print(A[9][9])



with open("data.json","r") as fp:#r - open file in read mode
 data = json.load(fp)
#print(data)

# create a simple JSON array

jsonString = '{"person": [{"x":1}, {"y":1},{"width":3},{"height":3}],"table": [{"x":4}, {"y":8},{"width":2},{"height":3}]}'
#jsonString = '{"person": [{"x":1}, {"y":2},{"width":3},{"height":2}]}'

# change the JSON string into a JSON object
jsonObject = json.loads(jsonString)

objectlist = []


# print the keys and values
for objects in jsonObject:
    objectdescription = []
    value = jsonObject[objects]
    #print(objects)
    objectdescription.append(objects)

    #print(value[0])
    #print(value[0]["x"])
    objectdescription.append(value[0]["x"])
    #print(value[1]["y"])
    objectdescription.append(value[1]["y"])
    #print(value[2]["width"])
    objectdescription.append(value[2]["width"])
    #print(value[3]["height"])
    objectdescription.append(value[3]["height"])
    objectlist.append(objectdescription)
    #print(value)
    #print("The key and value are ({}) = ({})".format(key, value))
#print (objectlist)

#iterate over objects
for object in objectlist:
    #print(object[0] + " detected")



    x_coord_start = object[1]
    x_coord_end = object[3] + x_coord_start -1

    #print("x_coord_start" + str(x_coord_start))
    #print("x_coord_end" + str(x_coord_end))

    y_coord_start = object[2]
    y_coord_end = object[4] + y_coord_start -1


    #print("y_coord_start" + str(y_coord_start))
    #print("y_coord_end" + str(y_coord_end))

    counterx = x_coord_start -1


    distances_object = []

    #while (countery < y_coord_end):
    #    print(countery)
    while (counterx <x_coord_end):
        #print(counterx)

        countery = y_coord_start - 1
        while (countery < y_coord_end):
            distances_object.append(A[countery][counterx])
            countery = countery +1



        counterx = counterx +1

        #counterx = counterx+1
    #    countery = countery + 1
    print(distances_object)

    minimum_distance_object = min(distances_object)
    mean_distance_object = sum(distances_object)/len(distances_object)
    maximal_distance_object = max(distances_object)
    print("minimum distance to object "+ object[0]+ " :" + str(minimum_distance_object))
    print("mean distance to object "+ object[0]+ " :"+ str(mean_distance_object))
    print("maximal distance to object "+ object[0]+ " :"+str(maximal_distance_object))



