def show(list):
	d_list = [['×' for i in range(len(list))] for j in range(len(list))]
	for i in range(len(list)):
		d_list[i][list[i] - 1] = '○'
	for row in d_list:
		print(row)
def queen(list, col):
	if col == len(list):
		show(list)
		print('**********************')
		return
	length = len(list)
	for i in range(1, length + 1):
		list[col], flag = i, True
		for j in range(col):
			if list[j] == i or abs(i - list[j]) == abs(j - col):
				flag = False
				break
		if flag:
			queen(list, col + 1)

n = int(input("请输入n的值："))
list = [0 for _ in range(n)]
queen(list, 0)			
