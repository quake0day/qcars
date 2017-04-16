import cv2
vidcap = cv2.VideoCapture('./IMG_0972.MOV')
success, image = vidcap.read()
count = 0
success = True

while success:
	success, image = vidcap.read()
	print "Read a new frame: ", success
	# rotate the frame
	(h, w) = image.shape[:2]
	center = (w/2, h/2)
	M = cv2.getRotationMatrix2D(center, 270, 1.0)
	rotated = cv2.warpAffine(image, M, (w, h))
	# save it..
	cv2.imwrite('frame%d.jpg' % count, rotated )
	count += 1
