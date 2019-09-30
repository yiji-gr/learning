import random
import cv2
import numpy as np

size = 20
scale = 20
up = 2
bird_row, bird_col = random.randint(0, size - 1), 0
block1_top, block1_bottom, block1_col = 0, 0, random.randint(size//2, size//4*3)
block2_top, block2_bottom, block2_col = 0, 0, size - 1
score = 0

def draw(l, arr):
	arr[(bird_row*scale):((bird_row+1)*scale), :scale] = (255, 255, 0)

	arr[:(block1_top*scale), (block1_col*scale):((block1_col+1)*scale)] = (0, 255, 0)
	arr[(block1_bottom*scale):, (block1_col*scale):((block1_col+1)*scale)] = (0, 255, 0)

	arr[:(block2_top*scale), (block2_col*scale):((block2_col+1)*scale)] = (0, 255, 0)
	arr[(block2_bottom*scale):, (block2_col*scale):((block2_col+1)*scale)] = (0, 255, 0)
	cv2.putText(temp_fig, "score: "+str(score), (size*scale//6, size*scale//6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0))

	return arr

def draw_line(fig):
	for row in range(1, size):
		cv2.line(fig, (0,row*scale), ((size-1)*100,row*scale), (0, 0, 0))
	for col in range(1, size):
		cv2.line(fig, (col*scale, 0), (col*scale,(size-1)*100), (0, 0, 0))
	return fig

def set_zero(a):
	for each in a:
		for i in range(len(each)):
			each[i] = 0
	return a

def init_block1():
	block1_top = random.randint(1, 6)
	block1_bottom = block1_top + random.randint(2, 4)
	return block1_top, block1_bottom

def init_block2():
	block2_top = random.randint(1, 6)
	block2_bottom = block2_top + random.randint(2, 4)
	return block2_top, block2_bottom

def get_a(a):
	a[bird_row][bird_col] = 1
	a[block1_top][block1_col] = 2
	a[block1_bottom][block1_col] = 2
	a[block2_top][block2_col] = 2
	a[block2_bottom][block2_col] = 2
	return a

def test_over():
	if block1_col == 0:
		if bird_row < block1_top or bird_row > block1_bottom:
			return True
	if block2_col == 0:
		if bird_row < block2_top or bird_row > block2_bottom:
			return True
	return False


def game_over(temp_fig):
	cv2.putText(temp_fig, "Game Over!!!", (size*scale//6, size*scale//2), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0))
	cv2.imshow("show", temp_fig)
	cv2.waitKey(2000)

if __name__ == '__main__':
	a = [[0 for i in range(size)] for j in range(size)]
	fig = np.zeros((scale*size, scale*size, 3)) + 255
	fig = draw_line(fig)

	block1_top, block1_bottom = init_block1()
	block2_top, block2_bottom = init_block2()
	while True:
		get_a(a)
		temp_fig = fig.copy()
		temp_fig = draw(a, temp_fig)

		cv2.imshow("show", temp_fig)
		key = cv2.waitKey(500)
		if key == 32:
			bird_row -= up
		elif key == 27:
			break

		bird_row += 1
		block1_col -= 1
		block2_col -= 1

		if test_over():
			game_over(temp_fig)
			break

		if bird_row < 0:
			bird_row = 0
		if bird_row >= size:
			bird_row = size - 1
		if block1_col < 0:
			block1_col = random.randint(block2_col + 5, size - 1)
			block1_top, block1_bottom = init_block1()
			score += 1
		if block2_col < 0:
			block2_col = random.randint(block1_col + 5, size - 1)
			block2_top, block2_bottom = init_block2()
			score += 1

		a = set_zero(a)
