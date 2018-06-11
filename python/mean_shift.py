import numpy as np
import math
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings("ignore", ".*GUI is implemented.*")
MIN_DISTANCE = 0.000001
NUM = 100


def group_points(mean_shift_points):
    group_assignment = []
    m, n = np.shape(mean_shift_points)
    index = 0
    index_dict = {}

    for i in range(m):
        item = []
        for j in range(n):
            item.append(str(("%5.2f" % mean_shift_points[i, j])))

        item_1 = "_".join(item)

        if item_1 not in index_dict:
            index_dict[item_1] = index
            index += 1

        group_assignment.append(index_dict[item_1])

    return group_assignment


# 计算pointA和pointB之间的欧式距离
def euclidean_dist(pointA, pointB):
    return math.sqrt((pointA - pointB) * (pointA - pointB).T)


def gaussian_kernel(distance, bandwidth):
    m = np.shape(distance)[0]
    right = np.mat(np.zeros((m, 1)))

    for i in range(m):
        right[i, 0] = np.exp((-0.5 * distance[i] * distance[i].T) / (bandwidth * bandwidth))

    left = 1 / (bandwidth * math.sqrt(2 * math.pi))

    gaussian_val = left * right
    return gaussian_val


def shift_point(point, points, kernel_bandwidth):
    points = np.mat(points)
    m, n = np.shape(points)
    points_distances = np.mat(np.zeros((m, 1)))

    # 计算距离
    for i in range(m):
        points_distances[i, 0] = np.sqrt((point - points[i]) * (point - points[i]).T)

    # 计算高斯核
    point_weights = gaussian_kernel(points_distances, kernel_bandwidth)

    # 计算分母
    all = np.sum(point_weights)

    # 均值偏移
    point_shifted = point_weights.T * points / all
    return point_shifted


def show_points(first_points, points, num):
    x0 = [first_points[i, 0] for i in range(NUM)]
    y0 = [first_points[i, 1] for i in range(NUM)]
    x = [points[i, 0] for i in range(NUM)]
    y = [points[i, 1] for i in range(NUM)]
    plt.scatter(x0, y0, label='start')
    plt.scatter(x, y, c='r', marker='x', label='move')
    plt.title('mean shift iter nums: ' + str(num))
    plt.legend(loc="best")
    plt.pause(NUM / 200)
    plt.clf()


def train_mean_shift(points, kernel_bandwidth=2):
    mean_shift_points = np.mat(points)
    first_points = np.mat(points)
    max_min_dist = 1
    iter = 0
    m, n = np.shape(mean_shift_points)
    need_shift = [True] * m

    while max_min_dist > MIN_DISTANCE:
        max_min_dist = 0
        iter += 1

        for i in range(m):
            #print(i)
            if not need_shift[i]:
                continue
            p_new = shift_point(mean_shift_points[i], points, kernel_bandwidth)
            dist = euclidean_dist(p_new, mean_shift_points[i])

            if dist > max_min_dist:
                max_min_dist = dist
            if dist < MIN_DISTANCE:
                need_shift[i] = False

            mean_shift_points[i] = p_new
        show_points(first_points, mean_shift_points, iter)

    group = group_points(mean_shift_points)

    return np.mat(points), mean_shift_points, group


def create_data():
    data = []

    for i in range(NUM):
        x0 = np.random.randn(1) * 10
        y0 = np.random.randn(1) * 10
        data.append([float(x0), float(y0)])

    return data


if __name__ == '__main__':
    data = create_data()
    points, shift_points, cluster = train_mean_shift(data, 2)

    x1 = []
    x2 = []
    y1 = []
    y2 = []

    for i in range(len(cluster)):
        x1.append(points[i, 0])
        y1.append(points[i, 1])
        x2.append(shift_points[i, 0])
        y2.append(shift_points[i, 1])

    plt.scatter(x1, y1, c='b')
    plt.scatter(x2, y2, c='r', marker='x')

    plt.savefig("result.jpg")
