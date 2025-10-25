import random


nodeNum = int(input("Insert # of Nodes to be included: "))
locations = []

for i in range(nodeNum):
    x = random.uniform(-1,1)
    y = random.uniform(-1,1)
    while not ((float(x).is_integer() or float(y).is_integer()) and (x != 0 or y != 0)):
        j = random.choice([True, False])
        if(j):
            x = random.choice([-1,1])
        else:
            y = random.choice([-1,1])
    locations.append((x,y))

with open("unitSquare.txt", "w") as file:
    for x, y in locations:
        file.write(f"{x}\t{y}\n")



