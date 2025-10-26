#Convert .tsp file to .txt (x,y) coordinates
import tsplib95

problem = tsplib95.load('/Users/salmakorashy/Desktop/CS179/tsp files/xit1083.tsp') #tsp file path

with open('1083coords.txt', 'w') as f:
    for node, (x, y) in problem.node_coords.items():
        f.write(f"{x} {y} \n")
