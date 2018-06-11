import numpy as np
import matplotlib.pyplot as plt
import time

M = 1000
N = 2


def createdata():
    data = np.zeros((M, N))
    for i in range(M):
        for j in range(N):
            data[i][j] = np.random.rand()
    return data


def caldistance(x, y):
    return np.sqrt(np.sum(np.power(x - y, 2)))


def kmeans(data, k):
    center = initcenter(data, k)
    cluster = np.zeros((M, 2))
    flag = True
    t1 = time.time()
    while flag:
        flag = False
        for i in range(M):
            min_distance = np.inf
            min_index = -1
            for j in range(k):
                distance = caldistance(center[j, :], data[i, :])
                if distance < min_distance:
                    min_distance = distance
                    min_index = j
            if int(cluster[i, 0]) != min_index:
                flag = True
            cluster[i, :] = min_index, min_distance ** 2
        for i in range(k):
            pointincluster = data[np.nonzero(cluster[:, 0] == i)[0]]
            center[i, :] = np.mean(pointincluster, axis=0)
    t2 = time.time()
    print("{0}-means cost {1} second".format(k, t2 - t1))
    return center, cluster


def initcenter(data, k):
    center = np.zeros((k, N))
    for i in range(N):
        min = np.min(data[:, i])
        max = np.max(data[:, i])
        for j in range(k):
            center[j, i] = min + (max - min) * np.random.rand()
    return center


if __name__ == '__main__':
    data = createdata()
    for k in range(2, 11):
        center, cluster = kmeans(data, k)
        print(center.shape)

        mark1 = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
        for i in range(M):
            plt.plot(data[i, 0], data[i, 1], mark1[int(cluster[i, 0])])
        mark2 = ['Db', 'Dr', 'Dk', 'Dg', '^b', '+b', 'sb', 'db', '<b', 'pb']
        for i in range(k):
            plt.plot(center[i, 0], center[i, 1], mark2[i])
        plt.show()
