import cv2
import random
import numpy as np
from copy import deepcopy

col, row = 15, 23
block_size = 40
cols, rows = col * block_size, row * block_size
bg = [[0 for i in range(row + 1)] for j in range(col + 1)]
for i in range(row):	# 右边加一层方便判断越界
	bg[col][i] = 1
for i in range(col):	# 下边加一层方便判断越界
	bg[i][row] = 1
wait_time = 500
game_over = False

#https://baike.baidu.com/pic/%E4%BF%84%E7%BD%97%E6%96%AF%E6%96%B9%E5%9D%97/535753/0/64380cd7912397dd96df99415982b2b7d1a287d4
tetrominos = [
	[[0, 0], [0, 1], [0, 2], [0, 3]],
	[[0, 0], [1, 0], [1, 1], [1, 2]],
	[[1, 0], [1, 1], [1, 2], [0, 2]],
	[[0, 0], [0, 1], [1, 0], [1, 1]],
	[[1, 0], [1, 1], [0, 1], [0, 2]],
	[[1, 0], [1, 1], [1, 2], [0, 1]],
	[[0, 0], [0, 1], [1, 1], [1, 2]],
]
idx = 0
widths = [4, 3, 3, 2, 3, 3, 3]	# 7种方块的宽度

def show():
	img = np.zeros((cols, rows, 3)) + 255
	for i in range(col):
		for j in range(row):
			if bg[i][j]:
				img[i*block_size+1:(i+1)*block_size-1, j*block_size+1:(j+1)*block_size-1] = (0, 255, 0)
	for i in range(1, row):
		cv2.line(img, (i*block_size, 0), (i*block_size, col*block_size), (0, 0, 0), 1)
	for i in range(1, col):
		cv2.line(img, (0, i*block_size), (row*block_size, i*block_size), (0, 0, 0), 1)
	for x, y in tetromino:
		img[x*block_size+1:(x+1)*block_size-1, y*block_size+1:(y+1)*block_size-1] = (255, 0, 255)
	return img

def move(key):	# 左移右移
	global tetromino
	step = 1 if key == 100 else -1
	tmp = deepcopy(tetromino)
	for i in range(len(tmp)):
		x, y = tmp[i]
		y += step
		if y < 0 or bg[x][y]:	#越界或者无法移动
			return
		tmp[i][1] = y

	tetromino = deepcopy(tmp)

def down1():	# 下移
	if down_distance() == 0:
		merge()
		return
	global tetromino
	for i in range(len(tetromino)):
		tetromino[i][0] += 1

def down_distance():	# 计算可以下降的距离
	min_len = col
	for x, y in tetromino:	# 从当前方块的下一行开始往下计算距离， 因为有些情况可以从下面穿过去
		for i in range(x + 1, col + 1):
			if bg[i][y]:
				min_len = min(min_len, i - x - 1)
	return min_len

def clear():	# 消除填满的行
	global bg
	full_rows = []
	for i in range(col - 1, -1, -1):
		flag = True
		for j in range(row):
			if not bg[i][j]:
				flag = False
				break
		if flag:
			full_rows.append(i)
			for j in range(row):
				bg[i][j] = 0

	if full_rows:
		for i in range(full_rows[0], -1, -1):	# 一定是从下往上处理
			for j in range(row):
				if bg[i][j] and i not in full_rows:
					bg[i][j] = 0
					bg[i + len(full_rows)][j] = 1

def merge():	# 当前下落方块与场上方块合并
	global tetromino, bg
	for x, y in tetromino:
		if bg[x][y]:	# 到顶了
			game_over = True
			return
		bg[x][y] = 1

	tetromino = random_gen()
	clear()

def down2():	# 直接下降到最下面
	min_len = down_distance()
	for i in range(len(tetromino)):
		tetromino[i][0] += min_len
	merge()

def random_gen():	# 在顶部随机位置随机生成方块
	global idx
	idx = random.randint(0, len(tetrominos) - 1)
	tmp = deepcopy(tetrominos)[idx]
	x = random.randint(0, row - widths[idx])
	for i in range(len(tmp)):
		tmp[i][1] += x
	return tmp

def rotate():	# 每次顺时针旋转90°
	global tetromino
	if idx == 0:
		if tetromino[0][0] == tetromino[1][0]:
			x, y = tetromino[1]
			if bg[x][y] or bg[x + 1][y] or bg[x + 2][y] or bg[x + 3][y]:
				return
			tetromino = [[x, y], [x + 1, y], [x + 2, y], [x + 3, y]]
		elif tetromino[0][1] == tetromino[1][1]:
			x, y = tetromino[0]
			if bg[x][y - 1] or bg[x][y] or bg[x][y + 1] or bg[x][y + 2]:
				return
			tetromino = [[x, y - 1], [x, y], [x, y + 1], [x, y + 2]]
	elif idx == 1:
		if tetromino[0][1] == tetromino[1][1] and tetromino[0][0] < tetromino[1][0]:
			x, y = tetromino[2]
			if x < 1 or bg[x - 1][y + 1] or bg[x - 1][y] or bg[x][y] or bg[x + 1][y]:
				return
			tetromino = [[x - 1, y + 1], [x - 1, y], [x, y], [x + 1, y]]
		elif tetromino[0][1] > tetromino[1][1] and tetromino[0][0] == tetromino[1][0]:
			x, y = tetromino[2]
			if bg[x + 1][y + 1] or bg[x][y + 1] or bg[x][y] or y < 1 or bg[x][y - 1]:
				return
			tetromino = [[x + 1, y + 1], [x, y + 1], [x, y], [x, y - 1]]
		elif tetromino[0][1] == tetromino[1][1] and tetromino[0][0] > tetromino[1][0]:
			x, y = tetromino[2]
			if y < 1 or bg[x + 1][y - 1] or bg[x + 1][y] or bg[x][y] or x < 1 or bg[x - 1][y]:
				return
			tetromino = [[x + 1, y - 1], [x + 1, y], [x, y], [x - 1, y]]
		elif tetromino[0][1] < tetromino[1][1] and tetromino[0][0] == tetromino[1][0]:
			x, y = tetromino[2]
			if x < 1 or y < 1 or bg[x - 1][y - 1] or bg[x][y - 1] or bg[x][y] or bg[x][y + 1]:
				return
			tetromino = [[x - 1, y - 1], [x, y - 1], [x, y], [x, y + 1]]
	elif idx == 2:
		if tetromino[0][0] == tetromino[1][0] and tetromino[0][1] < tetromino[1][1]:
			x, y = tetromino[1]
			if x < 1 or bg[x - 1][y] or bg[x][y] or bg[x + 1][y] or bg[x + 1][y + 1]:
				return
			tetromino = [[x - 1, y], [x, y], [x + 1, y], [x + 1, y + 1]]
		elif tetromino[0][0] < tetromino[1][0] and tetromino[0][1] == tetromino[1][1]:
			x, y = tetromino[0]
			if bg[x][y + 1] or bg[x][y] or y < 1 or bg[x][y - 1] or bg[x + 1][y - 1]:
				return
			tetromino = [[x, y + 1], [x, y], [x, y - 1], [x + 1, y - 1]]
		elif tetromino[0][0] == tetromino[1][0] and tetromino[0][1] > tetromino[1][1]:
			x, y = tetromino[0]
			if bg[x + 2][y] or bg[x + 1][y] or bg[x][y] or y < 1 or bg[x][y - 1]:
				return
			tetromino = [[x + 2, y], [x + 1, y], [x, y], [x, y - 1]]
		elif tetromino[0][0] > tetromino[1][0] and tetromino[0][1] == tetromino[1][1]:
			x, y = tetromino[3]
			if y < 1 or bg[x + 1][y - 1] or bg[x + 1][y] or bg[x + 1][y + 1] or bg[x][y + 1]:
				return
			tetromino = [[x + 1, y - 1], [x + 1, y], [x + 1, y + 1], [x, y + 1]]
	elif idx == 4:
		if tetromino[0][0] == tetromino[1][0]:
			x, y = tetromino[0]
			if x < 1 or bg[x - 1][y] or bg[x][y] or bg[x][y + 1] or bg[x + 1][y + 1]:
				return
			tetromino = [[x - 1, y], [x, y], [x, y + 1], [x + 1, y + 1]]
		elif tetromino[0][1] == tetromino[1][1]:
			x, y = tetromino[2]
			if y < 1 or bg[x][y - 1] or bg[x][y] or x < 1 or bg[x - 1][y] or bg[x - 1][y + 1]:
				return
			tetromino = [[x, y - 1], [x, y], [x - 1, y], [x - 1, y + 1]]
	elif idx == 5:
		if tetromino[0][0] == tetromino[1][0] and tetromino[0][1] < tetromino[1][1]:
			x, y = tetromino[3]
			if bg[x][y] or bg[x + 1][y] or bg[x + 2][y] or bg[x + 1][y + 1]:
				return
			tetromino = [[x, y], [x + 1, y], [x + 2, y], [x + 1, y + 1]]
		elif tetromino[0][0] < tetromino[1][0] and tetromino[0][1] == tetromino[1][1]:
			x, y = tetromino[1]
			if bg[x][y + 1] or bg[x][y] or y < 1 or bg[x][y - 1] or bg[x + 1][y]:
				return
			tetromino = [[x, y + 1], [x, y], [x, y - 1], [x + 1, y]]
		elif tetromino[0][0] == tetromino[1][0] and tetromino[0][1] > tetromino[1][1]:
			x, y = tetromino[2]
			if bg[x + 1][y + 1] or bg[x][y + 1] or x < 1 or bg[x - 1][y + 1] or bg[x][y]:
				return
			tetromino = [[x + 1, y + 1], [x, y + 1], [x - 1, y + 1], [x, y]]
		elif tetromino[0][0] > tetromino[1][0] and tetromino[0][1] == tetromino[1][1]:
			x, y = tetromino[2]
			if y < 1 or bg[x + 1][y - 1] or bg[x + 1][y] or bg[x + 1][y + 1] or bg[x][y]:
				return
			tetromino = [[x + 1, y - 1], [x + 1, y], [x + 1, y + 1], [x, y]]
	elif idx == 6:
		if tetromino[0][0] == tetromino[1][0]:
			x, y = tetromino[1]
			if bg[x][y] or bg[x + 1][y] or y < 1 or bg[x + 1][y - 1] or bg[x + 2][y - 1]:
				return
			tetromino = [[x, y], [x + 1, y], [x + 1, y - 1], [x + 2, y - 1]]
		elif tetromino[0][1] == tetromino[1][1]:
			x, y = tetromino[0]
			if y < 1 or bg[x][y - 1] or bg[x][y] or bg[x + 1][y] or bg[x + 1][y + 1]:
				return
			tetromino = [[x, y - 1], [x, y], [x + 1, y], [x + 1, y + 1]]

def show_tip():
	im = np.zeros((130, 310, 3)) + 255
	im = cv2.putText(im, "w:rotate, s:down", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 1)
	im = cv2.putText(im, "a:left, d:right", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 1)
	im = cv2.putText(im, "space: direct drop", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 1)
	im = cv2.putText(im, "esc or q:quit", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 1)
	return im

if __name__ == '__main__':
	tetromino = random_gen()
	tip = show_tip()
	while not game_over:
		img = show()
		cv2.imshow("tip", tip)
		cv2.imshow("Tetris", img)
		key = cv2.waitKey(wait_time)
		if key == 27 or key == ord('q'):
			break
		elif key == ord('a') or key == ord('d'):
			move(key)
			continue
		elif key == ord('s'):
			down1()
		elif key == ord('w'):
			rotate()
			continue
		elif key == 32:
			down2()
		down1()
