import numpy as np


def test(X, Y):
    size = X.shape[0]
    precision = 0.1 ** 6
    for i in range(size ** 2):
        m = np.random.randint(0, N)
        n = np.random.randint(0, N)
        num = X[m, :].dot(Y[:, n])
        if m == n and float(num - 1) > precision:
            return 0
        elif m != n and float(num) > precision:
            return 0
    return 1

N = 10
A = np.mat(np.random.random_sample((N, N)))
B = np.mat(np.random.random_sample((N, N)))
flag = test(A, B)
if flag == 0:
    print("这两个矩阵不互为逆矩阵！")
else:
    print("这两个矩阵互为逆矩阵")