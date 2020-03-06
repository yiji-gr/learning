import cv2
import random
import numpy as np

bg_size = 400
snake_size = 10
size = bg_size // snake_size
bg = [[0 for i in range(size)] for j in range(size)]
snake = []
food = []
food_limit = 5	# 最大食物数
through_wall = True	# 是否能穿墙
game_over = False
pause = False
score = 0
direct = 119	# 当前方向
pre_direct = direct	# 上一次的方向
direction = {119: [-1, 0], 115: [1, 0], 97: [0, -1], 100: [0, 1]}	# 上下左右
wait_time = 200

def show(snake):
	img = np.zeros((bg_size, bg_size, 3)) + 255
	img1 = np.zeros((160, 230, 3)) + 255
	img1 = cv2.putText(img1, "w:up, s:down", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 1)
	img1 = cv2.putText(img1, "a:left, d:right", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 1)
	img1 = cv2.putText(img1, "space: pause", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 1)
	img1 = cv2.putText(img1, "esc or q:quit", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 1)
	img1 = cv2.putText(img1, f"score: {score}", (30, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1)

	for i in range(len(snake)):
		x, y = snake[i][0] * snake_size, snake[i][1] * snake_size
		if i == len(snake) - 1:
			img[x:x+snake_size, y:y+snake_size] = (255, 255, 0)	# 蛇头
		else:
			img[x:x+snake_size, y:y+snake_size] = (0, 0, 0)		# 蛇身

	for each in food:
		x, y = each[0] * snake_size, each[1] * snake_size
		img[x:x+snake_size, y:y+snake_size] = (255, 0, 0)

	return img, img1

def move(snake):
	global game_over, score, direct
	if len(snake) >= 2:
		if direction[direct] == [snake[-2][0] - snake[-1][0], snake[-2][1] - snake[-1][1]]:
			direct = pre_direct
			return
	x1, y1 = snake[-1]
	x2, y2 = direction[direct]
	x, y = x1 + x2, y1 + y2
	if through_wall:
		if x >= size:
			x -= size
		elif x < 0:
			x += size
		if y >= size:
			y -= size
		elif y < 0:
			y += size
	else:
		if x >= size or x < 0 or y >= size or y < 0:	# 不能穿墙时撞墙，游戏结束
			game_over = True
			return
	if [x, y] in snake:	# 撞蛇身，游戏结束
		game_over = True
		return

	# 每次加入蛇下次前进的位置
	snake.append([x, y])
	if [x, y] in food:
		food.remove([x, y])
		random_gen(random.randint(1, 3))
		score += 1
	else:	# 下次的位置不是食物则删掉最后一个
		del snake[0]

def random_init():	# 初始化蛇的位置和方向
	global direct
	x, y = random.randint(0, size - 1), random.randint(0, size - 1)
	direct = 119 if x > size // 2 else 115
	snake.append([x, y])

def random_gen(n):	# 随机生成食物
	for i in range(n):
		while True:
			if len(food) >= food_limit:
				return
			x, y = random.randint(0, size - 1), random.randint(0, size - 1)
			if [x, y] not in snake and [x, y] not in food:
				food.append([x, y])
				break

if __name__ == '__main__':
	random_init()
	random_gen(random.randint(1, 3))
	while not game_over:
		pre_direct = direct
		img, img1 = show(snake)
		cv2.imshow("snake", img)
		cv2.imshow("tip", img1)
		key = cv2.waitKey(wait_time)
		if key == 27 or key == ord('q'):
			cv2.destroyAllWindows()
			break
		elif key == ord('w') or key == ord('s') or key == ord('a') or key == ord('d'):
			direct = key
		elif key == 32:
			pause = not pause
		if not pause:
			move(snake)
