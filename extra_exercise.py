import random

n = input("Enter size n of array (n % 2= 0): ")
sum = int(n)

arr = [i for i in range(sum)]
x = 2
sum_one = 0

while True:
    i = 0
    while i < sum:
        arr[i] = random.randrange(0, 3, 1)
        i += 1
        if arr[i-1] == 1 and x == 2:
            i -= 1
        if arr[i-1] == 2 and x == 2:
            x = 3

    for i in range(0, sum):
        if arr[i] == 1:
            sum_one += 1

    if sum_one == float(sum/2):
        break
    else:
        sum_one = 0
        x = 2

print(arr)
