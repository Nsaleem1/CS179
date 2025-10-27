import math
import random
import matplotlib.pyplot as plt
import os
import threading
import time

def euclideanDistance(loc1, loc2):
    return math.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)

#reading the file and storing coordinates into locations array
locations = []
route_x = []
route_y = []
fileName = input("Insert file name: ")

with open(fileName, "r") as text:
    for line in text:
        #split the x and y value and map them from string to float
        x, y = map(float, line.split())
        locations.append([x,y])
        #ensuring nodes do not exceed limit
        if len(locations) > 256:
            raise Exception("Max amount of Nodes in file reached")

# start timer
start_time = time.perf_counter()

#creating matrix
distanceMatrix = [[0] * len(locations) for x in range(len(locations))]

#computing values inside matrix 
for i in range(len(locations)):
    for j in range(len(locations)):
        distanceMatrix[i][j] = euclideanDistance(locations[i], locations[j])

print(f"There are {len(locations)} nodes, computing route ...")
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

# implement nearest neighbor
# initialize variables and arrays
unvisited = []
visited = []
for i in range(1, len(locations)):
    unvisited.append(i)
visited.append(0)

totalDistance = 0
current = 0
next = 0

# keep iterating until all nodes have been visited
while (len(unvisited) > 0):
    smallestDist = float('inf')

    # find nearest neighbor 
    for i in (unvisited):
        if (distanceMatrix[current][i] < smallestDist):
            smallestDist = distanceMatrix[current][i]
            next = i

    # update distance, arrays, and current node
    totalDistance += smallestDist
    unvisited.remove(next)
    visited.append(next) 
    current = next

# back to the first location 
totalDistance += distanceMatrix[current][visited[0]]  
visited.append(visited[0])  

# update bsf
if (totalDistance < bestSoFar):
    bestSoFar = int(totalDistance)
    bsfRoute = visited[:]
    print(f"\t\t{bestSoFar}\n")

# stop timer
end_time = time.perf_counter()    # high-resolution timer end
elapsed = end_time - start_time

print(f"Nearest Neighbor route generated in {elapsed:.6f} seconds.")

# after finding NN route, keep trying to optimize
# by uncrossing intersecting edges
while not interrupt:

    # check all edges to see if swapping nodes lessens distance
    for i in range(1, len(bsfRoute)-2):
        for j in range(i+2, len(bsfRoute)-1):

            # skip edges that share a point
            if j - i == 1:
                continue  
            
            # create edges 
            a, b = bsfRoute[i-1], bsfRoute[i]
            c, d = bsfRoute[j-1], bsfRoute[j]
            
            # compute distances 
            currDist = distanceMatrix[a][b] + distanceMatrix[c][d]
            newDist = distanceMatrix[a][c] + distanceMatrix[b][d]

            # compare distances
            if (newDist < currDist):
                bsfRoute[i:j] = reversed(bsfRoute[i:j])
    
    # recompute final distance after swaps 
    totalDistance = 0
    for k in range(len(bsfRoute) - 1):
        totalDistance += distanceMatrix[bsfRoute[k]][bsfRoute[k + 1]]           
    
    # update bsf
    if (totalDistance < bestSoFar):
        bestSoFar = int(totalDistance)
        print(f"\t\t{bestSoFar}\n")

if bestSoFar >= 6000: 
    print("Warning! The route found has reached or exceeded the 6000 meter constraint")

# making the plot after best route has been found
route_x = [locations[i][0] for i in bsfRoute]
route_y = [locations[i][1] for i in bsfRoute]

plt.figure(figsize=(10, 6))
plt.plot(route_x, route_y, 'b-', marker='o', markersize=4)
plt.title(f"Best Route Found (Distance = {bestSoFar} units)")
plt.xlabel("X")
plt.ylabel("Y")

# make launch pad bigger/red
landing_site = bsfRoute[0]
plt.scatter(locations[landing_site][0], locations[landing_site][1],
            color='red', s=90)

plt.grid(True)
plt.tight_layout()

# save path to the desktop
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
image_path = os.path.join(desktop, f"{fileName}_SOLUTION_{bestSoFar}.jpeg")
file_path = os.path.join(desktop, f"{fileName}_SOLUTION_{bestSoFar}.txt")
plt.savefig(image_path, dpi=300)

# Write route to file
with open(file_path, "w") as f:
    for i in bsfRoute:
        f.write(f"{i + 1}\n")

print(f"Route image written to desktop as {fileName}_SOLUTION_{bestSoFar}.jpeg\n")
print(f"Route file written to desktop as {fileName}_SOLUTION_{bestSoFar}.txt\n")

# must add error handling (file DNE, file in wrong format, ) error message and abort 
# should get an answer in 1/4 of a second
