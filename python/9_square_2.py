# -*- coding: utf-8 -*-

from __future__ import print_function
import cv2
import numpy as np

NAME_WINDOW = "show"
each_column_num = np.random.randint(0, 101, 9)

def in_which_part(img, x, y):
	w, h = img.shape[0], img.shape[1]
	return x / (w / 3), y / (h / 3)

def onmouse(event, x, y, flags, param):
	if event == cv2.EVENT_LBUTTONDOWN:
		col, row = in_which_part(img, x, y)

		if each_column_num[row * 3 + col] == 0:
			pass
		else:
			each_column_num[row * 3 + col] -= 1

		img_new = np.zeros(img.shape).astype(np.uint8)
		for i in range(3):
			for j in range(3):
				img_new[(i*100):(i*100+100), (j*100):(j*100+100)] = img[i*100+1][j*100+1]

		img_new[(row*100):(row*100+100), (col*100):(col*100+100)] = get_random_color()

		img_new = draw_img(img_new)

		cv2.imshow(NAME_WINDOW, img_new)
		cv2.waitKey(0)

def get_random_color():
	return np.random.randint(0, 256, 3)

def init_img(img):
	for i in range(3):
		for j in range(3):
			img[(i*100):(i*100+100), (j*100):(j*100+100)] = get_random_color()

	return img


def draw_img(img):
	for i in range(3):
		for j in range(3):
			cv2.putText(img, str(each_column_num[i+j*3]), (i*100+50, j*100+50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 1)

	return img

if __name__ == "__main__":
	img = np.zeros((300, 300, 3)).astype(np.uint8)
	img = init_img(img)
	img = draw_img(img)

	cv2.namedWindow(NAME_WINDOW)
	cv2.setMouseCallback(NAME_WINDOW, onmouse)
	cv2.imshow(NAME_WINDOW, img)
	cv2.waitKey(0)
