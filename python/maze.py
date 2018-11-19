import numpy as np
import cv2
import copy


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
            row *= pixel
            col *= pixel
            maze[row:row + pixel, col: col + pixel] = 0
            index_list.append((row, col))
    # index_list = sorted(index_list, key=lambda x: x[1])
    # index_list = sorted(index_list, key=lambda x: x[0])
    return maze, index_list


def bfs(maze, l, empty_l, num):
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
        num += 1


def get_bfs_path(l1, x, y, l):  #get shortest path
    l.append([x, y])
    if l1[x][y] == 1:
        return l

    direction_l = [[0, -1], [-1, 0], [1, 0], [0, 1]]
    for x0, y0 in direction_l:
        x1 = x0 + x
        y1 = y0 + y
        if 0 <= x1 < len(l1) and 0 <= y1 < len(l1[0]) and l1[x1][y1] == l1[x][y] - 1:
            return get_bfs_path(l1, x1, y1, l)


def dfs(maze_list, l, visited):
    global dfs_flag
    if not l:
        return False
    x, y = l[-1]
    if x == len(maze_list) - 1 and y == len(maze_list[0]) - 1:
        dfs_flag = True
        return
    if dfs_flag:
        return l
    direction_l = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    for x0, y0 in direction_l:
        x_ = x + x0
        y_ = y + y0
        if 0 <= x_ < len(maze_list) and 0 <= y_ < len(maze_list[0]) and not maze_list[x_][y_] and [x_, y_] not in visited:
            l.append((x_, y_))
            visited.append([x_, y_])
            dfs(maze_list, l, visited)
            if dfs_flag:
                return l
            l.pop()
    return l


def draw_way(maze_mat, l, pixel):   #draw the whole path
    for x, y in l:
        x *= pixel
        y *= pixel
        #cv2.circle(maze_mat, (y + int(pixel / 2), x + int(pixel / 2)), 1, (0, 255, 255))
        a = np.random.randint(0, 256, 3)
        a[a<20] = 20
        a[a>230] = 230
        maze_mat[y:y+pixel, x:x+pixel] = np.random.randint(0, 256, 3)
    return maze_mat


def is_blocked1(maze, x, y, l): #test whether there is a way from start to the end
    global can_finish_flag
    if not x or y == len(maze[0]) - 1:
        can_finish_flag = True
        return
    direction_l = [[-1, 0], [-1, 1], [0, 1], [1, 0], [1, 1], [0, -1], [-1, -1], [1, -1]]
    for x0, y0 in direction_l:
        x1 = x + x0
        y1 = y + y0
        if 0 <= x1 < len(maze) and 0 <= y1 < len(maze[0]) and maze[x1][y1] and [x1, y1] not in l:
            l.append([x1, y1])
            is_blocked1(maze, x1, y1, l)
            if can_finish_flag:
                return True
    return False


def is_blocked(maze, l):    #from left/bottom to top/right
    for i in range(1, len(maze)):
        if maze[i][0]:
            if is_blocked1(maze, i, 0, l):
                return True
    for i in range(1, len(maze[0]) - 1):
        if maze[len(maze) - 1][i]:
            if is_blocked1(maze, len(maze) - 1, i, l):
                return True
    return False


if __name__ == '__main__':
    pixel = 20  #pixel of each block
    width = 50  #maze width
    height = 50 #maze height
    block_num = width * height - 1000    #the block num of maze
    count = 1

    can_finish_flag = False #flag of whether the maze can through 

    total = 10  #get total num of maze picture
    whole_num = 2000    #loop num of each block_num
    while count < whole_num:
        print(block_num, count)
        count += 1

        maze_mat = create_maze_mat(width, height, pixel)
        maze_mat, index_list = maze_block(maze_mat, block_num, pixel)
        maze_list = [[0 for _ in range(width)] for _ in range(height)]
        for x, y in index_list:
            maze_list[int(x / pixel)][int(y / pixel)] = 1


        if not is_blocked(maze_list, []):
            # dfs method
            # dfs_flag = False
            # temp_list = copy.deepcopy(maze_list)
            # l = dfs(temp_list, [(0, 0)], [])
            # dfs_flag = False

            # bfs method
            empty_list = [[0 for _ in range(width)] for _ in range(height)]
            l = get_bfs_path(bfs(maze_list, [[0, 0]], empty_list, 0),
                             len(maze_list) - 1, len(maze_list[0]) - 1, [[0, 0]])

            maze_mat = draw_way(maze_mat, l, pixel)
            cv2.imwrite(str(block_num) + '_' + str(count) + '_' + str(len(l)) + ".jpg", maze_mat)

            total -= 1
            if not total:
                break

        can_finish_flag = False

        if count == whole_num - 1:
            block_num -= 100    #next block_num
            count = 0
