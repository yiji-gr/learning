import numpy as np

def nms(bboxes, nms_thresh):
	'''
		bboxes: x1, y1, x2, y2, score   shape:(n, 5)
	'''
	x1 = bboxes[:, 0]
	y1 = bboxes[:, 1]
	x2 = bboxes[:, 2]
	y2 = bboxes[:, 3]
	score = bboxes[:, 4]

	area = (x2 - x1 + 1) * (y2 - y1 + 1)		# 3-5 是3,4,5三个像素点 所以要+1
	keep = []
	score_idx = np.argsort(score)[::-1]

	while score_idx.size > 0:
		keep.append(score_idx[0])
		xx1 = np.maximum(x1[score_idx[1:]], x1[score_idx[0]])
		yy1 = np.maximum(y1[score_idx[1:]], y1[score_idx[0]])
		xx2 = np.minimum(x2[score_idx[1:]], x2[score_idx[0]])
		yy2 = np.minimum(y2[score_idx[1:]], y2[score_idx[0]])

		w = np.maximum(0, xx2 - xx1 + 1)
		h = np.maximum(0, yy2 - yy1 + 1)

		inter = w * h
		union = area[score_idx[0]] + area[score_idx[1:]] - inter
		iou = inter / union

		idx = np.where(iou < nms_thresh)[0]
		score_idx = score_idx[idx + 1]		# iou_idx 索引是从0开始的 所以这个要+1

	return keep

n = 10
print(nms(np.random.randn(n, 5), 0.3))
