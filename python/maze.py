import numpy as np
import cv2
import os


def create_maze_mat(width, height, pixel):  # create maze in while block
    maze = np.zeros((height * pixel, width * pixel, 3)) + 255

    for i in range(1, width):
        cv2.line(maze, (i * pixel, 0), (i * pixel, height * pixel), (0, 0, 0))
    for i in range(1, height):
        cv2.line(maze, (0, i * pixel), (width * pixel, i * pixel), (0, 0, 0))
    return maze


def maze_block(maze, num, pixel):   #random generate black block
    row_list = []
    col_list = []
    index_list = []

    for i in range(num):
        row_list.append(np.random.randint(int(maze.shape[0]) / pixel))
        col_list.append(np.random.randint(int(maze.shape[1]) / pixel))

    for row, col in zip(row_list, col_list):
        if (row or col) and (row != int(maze.shape[0] / pixel) - 1 or col != int(maze.shape[1] / pixel) - 1):
            if (row, col) not in index_list:
                index_list.append((row, col))
            row *= pixel
            col *= pixel
            maze[row:row + pixel, col: col + pixel] = 0
    # index_list = sorted(index_list, key=lambda x: x[1])
    # index_list = sorted(index_list, key=lambda x: x[0])
    return maze, index_list


def bfs(maze, l, empty_l):
    while True:
        x, y = l[0]
        if x == len(maze) - 1 and y == len(maze[0]) - 1:
            return empty_l

        direction_l = [[-1, 0], [1, 0], [0, 1], [0, -1]]
        for x0, y0 in direction_l:
            x1 = x + x0
            y1 = y + y0
            if (x1 or y1) and 0 <= x1 < len(maze) and 0 <= y1 < len(maze[0]) and not maze[x1][y1]:
                maze_list[x1][y1] = 'x'
                l.append([x1, y1])
                empty_l[x1][y1] = empty_l[x][y] + 1

        del l[0]


def get_bfs_path(l1, x, y, l):  # get shortest path
    l.append([x, y])
    if l1[x][y] == 1:
        return l

    direction_l = [[0, -1], [-1, 0], [1, 0], [0, 1]]
    for x0, y0 in direction_l:
        x1 = x0 + x
        y1 = y0 + y
        if 0 <= x1 < len(l1) and 0 <= y1 < len(l1[0]) and l1[x1][y1] == l1[x][y] - 1:
            return get_bfs_path(l1, x1, y1, l)


def dfs(maze_list, l, visited, path):
    if not l:
        return False

    x, y = l[-1]
    if x == len(maze_list) - 1 and y == len(maze_list[0]) - 1:
        return True

    direction_l = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    for x0, y0 in direction_l:
        x_ = x + x0
        y_ = y + y0
        if 0 <= x_ < len(maze_list) and 0 <= y_ < len(maze_list[0]) and not maze_list[x_][y_] and [x_, y_] not in visited:
            path.append({(x_, y_): (x, y)})
            l.append((x_, y_))
            visited.append([x_, y_])
            if dfs(maze_list, l, visited, path):
                return l
            l.pop()


def get_dfs_path(path, point):
    l = []
    while point != (0, 0):
        l.append(point)
        for each in path:
            if point == list(each.keys())[0]:
                point = list(each.values())[0]
    return l


def draw_way(maze_mat, l, pixel):   # draw the whole path
    for x, y in l:
        x *= pixel
        y *= pixel
        # cv2.circle(maze_mat, (y + int(pixel / 2), x + int(pixel / 2)), 1, (0, 255, 255))
        # a = np.random.randint(0, 256, 3)
        a = [(0, 255, 255), (255, 255, 0), (255, 0, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
        b = np.random.randint(0, len(a), 1)[0]
        maze_mat[x:x+pixel, y:y+pixel] = a[b]  # (0, 0, 255)
        # np.random.randint(0, 256, 3)
        cv2.imshow("1", maze_mat)
        cv2.waitKey(100)
    return maze_mat


def is_blocked1(maze, x, y, l):  # test whether there is a way from start to the end
    if not x or y == len(maze[0]) - 1:
        return True
    direction_l = [[-1, 0], [-1, 1], [0, 1], [1, 0], [1, 1], [0, -1], [-1, -1], [1, -1]]
    for x0, y0 in direction_l:
        x1 = x + x0
        y1 = y + y0
        if 0 <= x1 < len(maze) and 0 <= y1 < len(maze[0]) and maze[x1][y1] and [x1, y1] not in l:
            l.append([x1, y1])
            if is_blocked1(maze, x1, y1, l):
                return True
    return False


def is_blocked(maze, l):    # from left/bottom to top/right
    for i in range(1, len(maze)):
        if maze[i][0]:
            if is_blocked1(maze, i, 0, l):
                return True
    for i in range(1, len(maze[0]) - 1):
        if maze[len(maze) - 1][i]:
            if is_blocked1(maze, len(maze) - 1, i, l):
                return True
    return False


def meet_block(point1, point2, maze_list):
    x1, y1 = point1
    x2, y2 = point2
    if maze_list[x1 + x2][y1] == 1 and maze_list[x1][y1 + y2] == 1:
        return True
    return False


def a_start(open_list, close_list, maze_list, start, end, path):
    while len(open_list):
        open_list = sorted(open_list, key=lambda x: list(x.values())[0][-1])

        x1, y1 = list(open_list[0].keys())[0]
        x1_y1_g = open_list[0][(x1, y1)][0]
        if (x1, y1) == end:
            return path

        direction_list = [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [-1, 1], [1, -1], [1, 1]]
        for x2, y2 in direction_list:
            x = x1 + x2
            y = y1 + y2
            if x < 0 or x >= len(maze_list) or y < 0 or y >= len(maze_list[0]) or maze_list[x][y] == 1 or (x, y) in close_list:
                continue

            if [x2, y2] in [[-1, -1], [-1, 1], [1, -1], [1, 1]] and meet_block((x1, y1), (x2, y2), maze_list):
                continue

            if not point_in_list((x, y), open_list):
                x_y_g = get_g((x, y), (x1, y1)) + x1_y1_g
                x_y_h = get_h((x, y), end)
                x_y_f = x_y_g + x_y_h

                temp_dict = {(x, y): [x_y_g, x_y_h, x_y_f]}
                open_list.append(temp_dict)
                path.append({(x, y): (x1, y1)})
            else:
                if get_g((x, y), start) < get_g((x, y), (x1, y1)) + x1_y1_g:
                    x_y_g = get_g((x, y), start)
                    x_y_h = get_h((x, y), end)
                    x_y_f = x_y_g + x_y_h

                    temp_dict = {(x, y): [x_y_g, x_y_h, x_y_f]}
                    open_list.append(temp_dict)
                    path.append({(x, y): get_father_node((x1, y1), path)})

            maze_list[x][y] = 2

        close_list.append((x1, y1))
        del open_list[0]


def get_h(point, end):
    return (abs(point[0] - end[0]) + abs(point[1] - end[1])) * 10


def get_g(start, point):
    m = abs(start[0] - point[0])
    n = abs(start[1] - point[1])
    return min(m, n) * 14 + (max(m, n) - min(m, n)) * 10


def point_in_list(point, l):
    for each in l:
        if point == list(each.keys())[0]:
            return True
    return False


def get_a_start_way(path, end):
    l = [end]
    point = get_father_node(end, path)
    while point != start:
        l.append(point)
        point = get_father_node(point, path)

    return l


def get_father_node(point, l):
    for i in range(len(l)):
        if point == list(l[i].keys())[0]:
            return list(l[i].values())[0]


if __name__ == '__main__':
    pixel = 20  # pixel of each block
    width = 50  # maze width
    height = 50  # maze height
    block_num = width * height - 1300    # the block num of maze
    count = 1

    total = 10  # get total num of maze picture
    whole_num = 1000    # loop num of each block_num

    start = (0, 0)
    end = (height - 1, width - 1)

    while count < whole_num:
        print("block_num %d, search num %d" %(block_num, count))
        count += 1

        maze_mat = create_maze_mat(width, height, pixel)
        maze_mat, index_list = maze_block(maze_mat, block_num, pixel)
        maze_list = [[0 for _ in range(width)] for _ in range(height)]
        for x, y in index_list:
            maze_list[x][y] = 1

        if not is_blocked(maze_list, []):
            # dfs method -------------------------------------------
            path = []
            dfs(maze_list, [start], [], path)
            l = get_dfs_path(path, (height - 1, width - 1))
            # dfs method -------------------------------------------

            # bfs method --------------------------------------------------------------
            # empty_list = [[0 for _ in range(width)] for _ in range(height)]
            # l = get_bfs_path(bfs(maze_list, [start], empty_list),
            #                  len(maze_list) - 1, len(maze_list[0]) - 1, [])
            # bfs method --------------------------------------------------------------

            # the a* method have bug, not finished
            # a* method ---------------------------------------------------- 
            # start_end_g = 0
            # start_end_h = get_h(start, end)
            # start_end_f = start_end_g + start_end_h
            # open_list = [{start: [start_end_g, start_end_h, start_end_f]}]
            # 
            # a = a_start(open_list, [], maze_list, start, end, [])
            # l = get_a_start_way(a, end)
            # a* method ----------------------------------------------------

            l.append([0, 0])
            l.reverse()

            # draw and save
            maze_mat = draw_way(maze_mat, l, pixel)
            if not os.path.exists('maze_img'):
                os.mkdir('maze_img')
            cv2.imwrite('maze_img/'+str(block_num) + '_' + str(count) + '_' + str(len(l)) + ".jpg", maze_mat)

            total -= 1
            if not total:
                break

        if count == whole_num - 1:
            block_num -= 100    # next block_num
            count = 0
