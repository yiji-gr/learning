import cv2
import random
import numpy as np


wait_time = 1
time_step = 100
stop = False
def random_create():
	sudoku = [
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0]
	]
	sudoku = [
		[8, 9, 0, 6, 0, 0, 7, 0, 4],
		[3, 0, 0, 8, 0, 0, 0, 0, 0],
		[0, 0, 7, 9, 0, 0, 8, 0, 2],
		[0, 0, 8, 0, 7, 0, 0, 0, 3],
		[9, 0, 0, 0, 0, 0, 0, 7, 0],
		[0, 5, 0, 0, 0, 0, 6, 0, 0],
		[4, 0, 1, 0, 0, 8, 2, 9, 0],
		[0, 0, 0, 0, 0, 4, 3, 0, 0],
		[2, 0, 3, 0, 0, 9, 0, 0, 8]
	]
	return sudoku

def valid(num, row, col, sudoku):
	for i in range(len(sudoku)):
		if i != col and sudoku[row][i] == num:
			return False
		if i != row and sudoku[i][col] == num:
			return False

	row_num, col_num = row // 3, col // 3
	for i in range(3):
		for j in range(3):
			ii, jj = row_num * 3 + i, col_num * 3 + j
			if ii != row and jj != col and sudoku[ii][jj] == num:
				return False
	return True

def get_blank(sudoku):
	size = len(sudoku)
	blank = []
	for i in range(size):
		for j in range(size):
			if sudoku[i][j] == 0:
				blank.append([i, j])
	return blank

def print_sudoku(sudoku):
	for each in sudoku:
		print(each)

def dfs(blank, sudoku, idx):
	if idx == len(blank):
		print_sudoku(sudoku)
		save(sudoku, blank)
		return True

	row, col = blank[idx][0], blank[idx][1]
	for i in range(1, 10):
		sudoku[row][col] = i
		if not stop:
			show(sudoku, blank)
		if not valid(i, row, col, sudoku):
			continue
		if dfs(blank, sudoku, idx + 1):
			return True
		sudoku[row][col] = 0
		if not stop:
			show(sudoku, blank)
	sudoku[row][col] = 0
	return False

def show(sudoku, blank, name="sudoku"):
	img = draw(sudoku, blank)
	cv2.imshow(name, img)

	global wait_time, stop
	key = cv2.waitKey(wait_time)
	if key == ord('w'):
		wait_time += time_step
	elif key == ord('s'):
		wait_time -= time_step
	elif key == 27:
		stop = True
	wait_time = max(wait_time, 0)

def save(sudoku, blank, img_name="sudoku.jpg"):
	img = draw(sudoku, blank)
	cv2.imwrite(img_name, img)

def draw(sudoku, blank):
	size = len(sudoku)
	block_size = 40
	img = np.zeros(((size + 1) * block_size, (size + 1) * block_size, 3)) + 255
	for i in range(size + 1):
		cv2.line(img, (block_size//2 + block_size*i, block_size//2), (block_size//2 + block_size*i, block_size//2 + block_size*size), (0,0,0))
		cv2.line(img, (block_size//2, block_size//2 + block_size*i), (block_size//2 + block_size*size, block_size//2 + block_size*i), (0,0,0))
	for i in range(size):
		for j in range(size):
			if sudoku[j][i] == 0:
				continue
			if [j, i] in blank:
				cv2.putText(img, str(sudoku[j][i]), ((i+1)*block_size-block_size//4, 
					(j+1)*block_size+block_size//4), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
			else:
				cv2.putText(img, str(sudoku[j][i]), ((i+1)*block_size-block_size//4, 
					(j+1)*block_size+block_size//4), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
	return img

def test():
	sudoku = random_create()
	blank = get_blank(sudoku)
	sudoku_copy = sudoku.copy()
	dfs(blank, sudoku_copy, 0)

test()
