import numpy as np
import cv2
from matplotlib import pyplot as plt



class watershed_segmentation():


	def __init__(self,img):
		self.img = img

	def segment(self):
		b,g,r = cv2.split(self.img)
		rgb_img = cv2.merge([r,g,b])

		gray = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
		ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

		plt.subplot(121),plt.imshow(rgb_img)
		plt.title('Input Image'), plt.xticks([]), plt.yticks([])
		plt.subplot(122),plt.imshow(thresh, 'gray')
		plt.title("Otus's binary threshold"), plt.xticks([]), plt.yticks([])
		plt.show()

img = cv2.imread('/home/thomas/Downloads/cat.jpg')

test = watershed_segmentation(img)
test.segment()