import math
import random
import matplotlib.pyplot as plt
import os
import threading

def euclideanDistance(loc1, loc2):
    return math.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)

#reading the file and storing coordinates into locations array
locations = []
route_x = []
route_y = []
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

#thread to detect 'enter' click
interrupt = False
def enterClick():
    input()
    global interrupt
    interrupt = True
t1 = threading.Thread(target=enterClick)
t1.start()

#random order run 
#for run in range(100):
while not interrupt:
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
        route = order[:]
if bestSoFar >= 6000: 
    raise Exception("No route found below 6000 meter constraint")

# making the plot after best route has been found
route_x = [locations[i][0] for i in route]
route_y = [locations[i][1] for i in route]

plt.figure(figsize=(10, 6))
plt.plot(route_x, route_y, 'b-', marker='o', markersize=2)
plt.title(f"Best Route Found (Distance = {bestSoFar} units)")
plt.xlabel("X")
plt.ylabel("Y")

# make launch pad bigger/red
landing_site = route[0]
plt.scatter(locations[landing_site][0], locations[landing_site][1],
            color='red', s=90)

plt.grid(True)
plt.tight_layout()
#plt.savefig(f"{fileName}_SOLUTION_{bestSoFar}.jpeg") 

# save path to the desktop
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
image_path = os.path.join(desktop, f"{fileName}_SOLUTION_{bestSoFar}.jpeg")
file_path = os.path.join(desktop, f"{fileName}_SOLUTION_{bestSoFar}.txt")
plt.savefig(image_path, dpi=300)


# Write route to file
with open(file_path, "w") as f:
    f.write(f"{1}\n")
    for node in route:
        f.write(f"{node}\n")
    f.write(f"{1}\n")

print(f"Route image written to desk as {fileName}_SOLUTION_{bestSoFar}.jpeg\n")
print(f"Route file written to desk as {fileName}_SOLUTION_{bestSoFar}.txt\n")

# should allow for second input- interruption (pretty much works now)
# must add error handling (file DNE, file in wrong format, ) error message and abort 
# fix the 6000 meter limit error: must give warning but still create all outputs 
# double check the logic behind the location nums because why does the route include 0 twice? or even at all?
# ran it, and the image shows that the algorithm did not start and end at the same node??
# should only visit each node exactly once 
# should get an answer in 1/4 of a second
# must return the distance as nearest integer 
# 10-pixel buffer between any point and an edge