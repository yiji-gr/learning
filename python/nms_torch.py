import torch

def nms(bboxes, nms_thresh):
	'''
		bboxes: Tensor x1, y1, x2, y2, score (n, 5)
	'''
	x1 = bboxes[:, 0]
	y1 = bboxes[:, 1]
	x2 = bboxes[:, 2]
	y2 = bboxes[:, 3]
	score = bboxes[:, 4]

	area = (x2 - x1 + 1) * (y2 - y1 + 1)
	_, score_idx = score.sort(0, descending=True)
	keep = []

	while score_idx.numel() > 0:
		if score_idx.numel() == 1:
			keep.append(score_idx.item())
			break
		keep.append(score_idx[0].item())

		xx1 = x1[score_idx[1:]].clamp(min=x1[score_idx[0]])
		yy1 = y1[score_idx[1:]].clamp(min=y1[score_idx[0]])
		xx2 = x2[score_idx[1:]].clamp(max=x2[score_idx[0]])
		yy2 = y2[score_idx[1:]].clamp(max=y2[score_idx[0]])

		w = torch.clamp(xx2 - xx1 + 1, min=0)
		h = torch.clamp(yy2 - yy2 + 1, min=0)

		inter = w * h
		union = area[score_idx[0]] + area[score_idx[1:]] - inter
		iou = inter / union

		idx = (iou < nms_thresh).nonzero().squeeze()
		score_idx = score_idx[idx + 1]

	return torch.LongTensor(keep)

n = 10
print(nms(torch.randn(n, 5), 0.5))
