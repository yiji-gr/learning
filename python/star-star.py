flag = False

def search(game_list, sub_list, size, start_list, end_list, index, x1, y1):
    global flag
    if x1 == end_list[index][0] and y1 == end_list[index][1]:
        if index == len(end_list) - 1:
            for each in game_list:
                print(each)
            flag = True
        else:
            search(game_list, sub_list, size, start_list, end_list, index + 1, start_list[index + 1][0], start_list[index + 1][1])
        return

    if flag:
        return

    for i in range(len(end_list)):
        if game_list[end_list[i][0]][end_list[i][1]] != 0 and game_list[end_list[i][0]][end_list[i][1]] != i + 1:
            return

    direction_list = [[-1, 0], [1, 0], [0, -1], [0, 1]]
    for x0, y0 in direction_list:
        x = x1 + x0
        y = y1 + y0
        if 0 <= x < size and 0 <= y < size and not game_list[x][y]:
            sub_list[index].append((x, y))
            game_list[x][y] = index + 1
            search(game_list, sub_list, size, start_list, end_list, index, x, y)
            sub_list[index].pop()
            game_list[x][y] = 0


if __name__ == '__main__':
    size = 6
    game_list = [[0 for _ in range(size)] for _ in range(size)]
    start_list = [(3, 0), (4, 0), (1, 1), (1, 2), (1, 3), (0, 3)]
    end_list = [(0, 2), (5, 5), (4, 5), (3, 5), (2, 5), (0, 5)]

    sub_list = [[] for i in range(len(start_list))]
    for i in range(len(start_list)):
        sub_list[i].append(start_list[i])
        game_list[start_list[i][0]][start_list[i][1]] = i + 1

    search(game_list, sub_list, size, start_list, end_list, 0, start_list[0][0], start_list[0][1])
