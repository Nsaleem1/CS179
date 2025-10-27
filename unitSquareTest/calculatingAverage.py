
total = 0
with open("usEA1_10sec.txt", "r") as f:
    for line in f:
        total += int(line)

average = total / 100
print(average)