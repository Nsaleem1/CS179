import math
import random
import matplotlib.pyplot as plt

def euclideanDistance(loc1, loc2):
    return math.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)

#reading the file and storing coordinates into locations array
locations = []
locationNum = 0
fileName = input("Insert file name: ")

with open(fileName, "r") as text:
    for line in text:
        #split the x and y value and map them from string to float
        x, y = map(float, line.split())
        locations.append([x,y])
        locationNum += 1
        #ensuring nodes do not exceed limit
        if locationNum > 256:
            raise Exception("Max amount of Nodes in file reached")
        
#creating matrix
distanceMatrix = [[0] * locationNum for x in range(locationNum)]

#computing values inside matrix 
for i in range(locationNum):
    for j in range(locationNum):
        distanceMatrix[i][j] = round(euclideanDistance(locations[i], locations[j]),1)

print(f"There are {locationNum} nodes, computing route ...")
print("\tShortest Route Discovered So Far\n")
bestSoFar = 6000

#random order run 
for run in range(100):

    #creating an array with a random order of numbers 
    order = list(range(locationNum))
    random.shuffle(order)
    order.append(0)

    #computing total distance with that order
    totalDistance = 0
    for i in range(locationNum):
        totalDistance += distanceMatrix[order[i]][order[i + 1]]

        #early abandoning 
        if totalDistance > bestSoFar:
            break

    #updating BSF 
    if totalDistance < bestSoFar:
        bestSoFar = round(totalDistance,1)
        print(f"\t\t{bestSoFar}\n")


# should allow for second input- interruption 
# must output image and file
# 256cashew file does not return a distance 