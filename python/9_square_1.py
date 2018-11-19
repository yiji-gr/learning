# -*- coding: utf-8 -*-
'''
1.新建M*N的零矩阵
2.分9宫格随机分配颜色,并记录颜色值
3.显示图片及单元格颜色数值
4.单击某格颜色-1,并记录颜色值
5.新建相同大小零矩阵,分9宫格分配上次颜色,并记录颜色值
重复345
'''
from __future__ import print_function

import cv2
import numpy as np

NAME_WINDOW = "show"

def onmouse(event, x, y, flags, param):
	if event == cv2.EVENT_LBUTTONDOWN:
		i, j = in_which_part(img, x, y)

		#	4.单击某格颜色-1,并记录颜色值
		if img[j*100+1][i*100+1] == 0:
			img[(j*100):(j*100+100), (i*100):(i*100+100)] = 255
		else:
			img[(j*100):(j*100+100), (i*100):(i*100+100)] -= 1

		
		#	5.新建相同大小零矩阵,分9宫格分配上次颜色,并记录颜色值
		img_new = np.zeros(img.shape).astype(np.uint8)
		for i in range(3):
			for j in range(3):
				img_new[(i*100):(i*100+100), (j*100):(j*100+100)] = img[i*100+1][j*100+1]

		#	3.显示图片及单元格颜色数值
		img_new = draw_img(img_new)

		cv2.imshow(NAME_WINDOW, img_new)
		cv2.waitKey(0)

def get_random_color():
	return np.random.randint(0, 256)

def init_img(img):
	for i in range(3):
		for j in range(3):
			img[(i*100):(i*100+100), (j*100):(j*100+100)] = get_random_color()

	return img

def draw_img(img):
	for i in range(3):
		for j in range(3):
			# print(i, j, img[i*100+1][j*100+1])
			cv2.putText(img, str(img[j*100+1][i*100+1]), (i*100+50, j*100+50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 1)
	# print("------------------")
	return img

def in_which_part(img, x, y):
	w, h = img.shape[0], img.shape[1]
	return int(x / (w / 3)), int(y / (h / 3))

if __name__ == '__main__':
	#	1.新建M*N的零矩阵
	img = np.zeros((300, 300)).astype(np.uint8)
	#	2.分9宫格随机分配颜色,并记录颜色值
	img = init_img(img)

	#	3.显示图片及单元格颜色数值
	img = draw_img(img)
	
	cv2.namedWindow(NAME_WINDOW)
	cv2.setMouseCallback(NAME_WINDOW, onmouse)
	cv2.imshow(NAME_WINDOW, img)
	cv2.waitKey(0)
