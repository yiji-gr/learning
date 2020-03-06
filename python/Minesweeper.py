import cv2
import random
import numpy as np
from copy import deepcopy
import os

col, row = 10, 10	# 行列数
block_size = 30	# 每个格子的大小
mine_num = 20	# 地雷数量
bg = [[0 for i in range(row)] for j in range(col)]
mines = deepcopy(bg)	# 地雷位置
around = [[-1, -1], [-1, 0], [-1, 1], [1, -1], [1, 0], [1, 1], [0, 1], [0, -1]]	# 周围8个位置
img = np.zeros((block_size*col, block_size*row, 3)).astype(np.uint8) + 255 # np.zeros类型是np.float64，cv2.imread类型是np.uint8
wait_time = 100
game_over = False
win = False
cur_idx = [-1, -1, -1]	# 当前点击位置(x, y, 0:左键点击1:右键点击)

flags = []	# 旗子位置
clicked = []	# 已经点过的非旗子位置
mine_img = (0, 0, 255)
flag_img = (0, 0, 0)
if os.path.exists("Minesweeper_min1e.png"):
	mine_img = cv2.imread("Minesweeper_mine.png")
	mine_img = cv2.resize(mine_img, (block_size-2, block_size-2))
if os.path.exists("Minesweeper_fl1ag.png"):
	flag_img = cv2.imread("Minesweeper_flag.png")
	flag_img = cv2.resize(flag_img, (block_size-2, block_size-2))

def OnMouseAction(event, x, y, flags, param):
	global cur_idx
	if event == cv2.EVENT_LBUTTONDOWN:
		cur_idx = [y // block_size, x // block_size, 0]
	elif event == cv2.EVENT_RBUTTONDOWN:
		cur_idx = [y // block_size, x // block_size, 1]

def draw_lines():
	for i in range(1, row):
		cv2.line(img, (i*block_size, 0), (i*block_size, block_size*col), (0, 0, 0), 1)
	for i in range(1, col):
		cv2.line(img, (0, i*block_size), (block_size*row, i*block_size), (0, 0, 0), 1)

def around_0(x0, y0):	# bfs
	l = [[x0, y0]]
	res = [[x0, y0]]
	while l:
		x1, y1 = l[0]
		for x2, y2 in around:
			x, y = x1 + x2, y1 + y2
			if x < 0 or y < 0 or x >= col or y >= row or mines[x][y] or [x, y] in res or bg[x1][y1] != 0:
				continue
			l.append([x, y])
			if [x, y] not in res:
				res.append([x, y])

		del l[0]
	return res

def show1():
	global cur_idx, clicked
	if cur_idx == [-1, -1, -1] or (cur_idx[2] == 0 and cur_idx[:2] in flags):	# 初始状态或者左键点击旗子直接返回
		return
	x, y, flag = cur_idx
	if not flag:	# 左键
		if mines[x][y]:	# 点到地雷，游戏结束
			global game_over
			game_over = True
			return

		if bg[x][y] == 0:
			safe = around_0(x, y)
			for x, y in safe:
				if [x, y] not in clicked:
					clicked.append([x, y])
				img[x*block_size+2:(x+1)*block_size-1, y*block_size+2:(y+1)*block_size-1] = (255, 0, 0)
				if bg[x][y] > 0:
					cv2.putText(img, str(bg[x][y]), (y*block_size+5, x*block_size+25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 1)
		else:
			if [x, y] not in clicked:
				clicked.append([x, y])
			img[x*block_size+2:(x+1)*block_size-1, y*block_size+2:(y+1)*block_size-1] = (255, 0, 0)
			if bg[x][y] > 0:
				cv2.putText(img, str(bg[x][y]), (y*block_size+5, x*block_size+25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 1)

		if len(clicked) == col * row - mine_num:	# 所有非地雷区域都点完了，胜利
			global win
			win = True
			return

	else:	# 右键
		if [x, y] in flags:	# 点到旗子，复原
			flags.remove([x, y])
			img[x*block_size+1:(x+1)*block_size-1, y*block_size+1:(y+1)*block_size-1] = (255, 255, 255)
		else:
			if [x, y] not in clicked:
				flags.append([x, y])
				img[x*block_size+1:(x+1)*block_size-1, y*block_size+1:(y+1)*block_size-1] = flag_img
	cur_idx = [-1, -1, -1]	# 恢复初始状态

def show2():
	for i in range(col):
		for j in range(row):
			if mines[i][j]:
				img[i*block_size+1:(i+1)*block_size-1, j*block_size+1:(j+1)*block_size-1] = mine_img
			else:
				img[i*block_size+1:(i+1)*block_size-1, j*block_size+1:(j+1)*block_size-1] = (255, 0, 0)
				if bg[i][j] > 0:
					cv2.putText(img, str(bg[i][j]), (j*block_size+5, i*block_size+25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 1)

def init_mines():	# 随机位置生成地雷
	for i in range(mine_num):
		while True:
			x, y = random.randint(0, col - 1), random.randint(0, row - 1)
			if not mines[x][y]:
				mines[x][y] = 1
				break

def get_num():	# 计算每个非地雷位置周围8格地雷的个数
	for i in range(col):
		for j in range(row):
			if mines[i][j]:
				bg[i][j] = -1
				continue
			for x_, y_ in around:
				x, y = x_ + i, y_ + j
				if x < 0 or y < 0 or x >= col or y >= row:
					continue
				if mines[x][y]:
					bg[i][j] += 1

def show_tip():
	im = np.zeros((80, 250, 3)) + 255
	if game_over:
		im = cv2.putText(im, "game over!", (25, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1)
	elif win:
		im = cv2.putText(im, "you win!", (45, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 1)
	else:
		im = cv2.putText(im, f"mines num:{mine_num}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 1)
		im = cv2.putText(im, f"res num:{row * col - mine_num - len(clicked)}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 1)
	return im

if __name__ == '__main__':
	init_mines()
	# for each in mines:	# 打开作弊器
	# 	print(each)
	get_num()
	draw_lines()
	while True:
		tip_img = show_tip()
		if win:
			wait_time = 0
		if game_over:
			show2()
			wait_time = 0
		show1()
		cv2.namedWindow("mines")
		cv2.setMouseCallback("mines", OnMouseAction)
		cv2.imshow("tip", tip_img)
		cv2.imshow("mines", img)
		key = cv2.waitKey(wait_time)
		if key == 27 or key == ord('q'):
			break
