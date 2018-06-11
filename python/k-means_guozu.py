import numpy as np


def normalized(array):
    m, n = array.shape
    array1 = array[:, 1:].astype(np.float64)

    min = np.min(array1, axis=0)
    max = np.max(array1, axis=0)

    for i in range(m):
        for j in range(n - 1):
            array1[i][j] = (array1[i][j] - min[j]) / (max[j] - min[j])

    return array1


def get_init_center(k, array):
    m, n = array.shape
    center = np.zeros((k, n))

    first_index = np.random.choice(m, 1)[0]

    distance_list = []
    index_list = [first_index]
    for i in range(m):
        distance_list.append(distance(array[i], array[first_index]))

    while len(index_list) < 3:
        random = np.random.rand() * sum(distance_list)
        for i in range(len(distance_list)):
            if random - distance_list[i] < 0:
                break
            else:
                random -= distance_list[i]
        if i not in index_list:
            index_list.append(i)
        #else:
            #print(i)

    for i in range(k):
        center[i] = array[index_list[i]]

    return center


def distance(vector_a, vector_b):
    return np.sqrt(np.sum((vector_a - vector_b) ** 2))


def kmeans(array, k):
    m, n = array.shape
    center = get_init_center(k, normalized_grade)
    cluster_list = np.zeros((m, 1))
    flag = True
    while flag:
        flag = False
        for i in range(m):
            min_distance = np.inf
            min_index = -1
            for j in range(k):
                cur_distance = distance(center[j], array[i])
                if cur_distance < min_distance:
                    min_distance = cur_distance
                    min_index = j
            if cluster_list[i] != min_index:
                flag = True
            cluster_list[i] = min_index

        for i in range(k):
            new_center = array[np.nonzero(cluster_list[:, 0] == i)[0]]
            center[i, :] = np.mean(new_center, axis=0)

    return cluster_list


if __name__ == '__main__':
    grade = np.array([
        ['中国', 50, 50, 9],
        ['日本', 28, 9, 4],
        ['韩国', 17, 15, 3],
        ['伊朗', 25, 40, 5],
        ['沙特', 28, 40, 2],
        ['伊拉克', 50, 50, 1],
        ['卡塔尔', 50, 40, 9],
        ['阿联酋', 50, 50, 9],
        ['乌兹别克斯坦', 40, 40, 5],
        ['泰国', 50, 50, 9],
        ['越南', 50, 50, 5],
        ['阿曼', 50, 50, 9],
        ['巴林', 40, 40, 9],
        ['朝鲜', 40, 32, 17],
        ['印尼', 50, 50, 9],
    ])
    normalized_grade = normalized(grade)

    k = 3
    cluster_result = kmeans(normalized_grade, k)

    for i in range(k):
        print("Class {0}: ".format(i), end='')
        for j in range(len(cluster_result)):

            if cluster_result[j] == i:
                print(grade[j][0], end=' ')
        print()
