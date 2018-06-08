import numpy
import cv2

for folder in os.listdirs('val'):
	for im in os.listdirs(folder):
		img = cv2.imread(abspath(join('val', join(folder, im))))
		img = cv2.resize(img, (256, 256))
		cv2.imwrite(abspath(join('val', join(folder, im))), img)