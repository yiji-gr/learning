import time

dict1 = {}	# 空间换时间


def hailstone(n):
    count = 0
    while n > 1:
        count += 1
        if n % 2 == 0:
            n /= 2
        else:
            n = 3 * n + 1

        if n in dict1:
            return dict1[n] + count

    count += 1
    return count

time1 = time.time()
max = 0
for i in range(1, 5000000):
    num = hailstone(i)
    dict1[i] = num
    if num > max:
        max = num
        index = i

time2 = time.time()
print(index, hailstone(index))
print("it cost {0} seconds".format(time2 - time1))