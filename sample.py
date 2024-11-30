import random


arr = [0, 2, 4, 7, 9, 27, 32, 36, 38, 39, 40, 43, 47, 50, 53, 55, 56, 64, 66, 76]
arr.sort()

pairs = []
for i in range(80):
    num1 = 0
    num2 = 0
    while num1 == num2:
        num1 = random.randint(0,4)
        num2 = random.randint(0,4)
    pairs.append([num1,num2])

for i in range(80):
    if i in arr:
        pairs[i][1] = pairs[i][0]
x = 0
for i in range(80):
    if pairs[i][1] == pairs[i][0]:
        x +=1
print(pairs)