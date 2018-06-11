import math
from matplotlib import pyplot as plt
import numpy as np
import warnings

warnings.filterwarnings("ignore",".*GUI is implemented.*")
for n in range(2, 57):
	if n != 56:
		dict1 = {'a' + str(i) : 0 for i in range(n + 1)}
		dict1['a0'] = 1

		cos_gradient = [0, -1, 0, 1]

		
		for i in range(1, n + 1):
			index = i % 4 - 1
			dict1['a' + str(i)] = cos_gradient[index] * 1.0 / math.factorial(i)


		x_cood = np.arange(0, 20, 0.01)
		y1_cood = np.cos(x_cood)

		y_result = ''
		for i in range(1, n + 1):
			if dict1['a' + str(i)] != 0.0:
				y_result += 'x_cood ** ' + str(i) + ' * ' +str(dict1['a' + str(i)]) + ' + '
		y_result = y_result[:-2]

		plt.ylim(ymin=-2, ymax=2)
		plt.plot(x_cood, y1_cood, label='cos(x)')
		plt.plot(x_cood, eval(y_result) + 1, label='fitting')
		plt.legend(loc='upper left',frameon=False) 
		plt.pause(0.01) 
		plt.clf()
	else:
		plt.ylim(ymin=-2, ymax=2)
		plt.plot(x_cood, y1_cood, label='cos(x)')
		plt.plot(x_cood, eval(y_result) + 1, label='fitting')
		plt.legend(loc='upper left',frameon=False) 
		plt.pause(0.01) 
		plt.show()
