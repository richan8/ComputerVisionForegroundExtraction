#!/usr/bin/env python
# coding: utf-8

import cv2
import time
import numpy as np
import os

imgSize = 64
processedImg = np.array([([0]*imgSize)]*imgSize)
mask = np.array([([False]*imgSize)]*imgSize)
diff = np.array([([0,0,0]*imgSize)]*imgSize)
backgroundImg = np.array([([0,0,0]*160)]*120)
maskSizeSet = False
maskThreshold = 171
quantizeVal = 105
imgIndex = 0
imgClass = 'Five'

def preProcessImg(img, verbose = False):
	global mask
	global diff
	global maskThreshold
	global backgroundImg
	global processedImg

	tempImg = cv2.resize(img,(int(img.shape[0]/6), int(img.shape[1]/6)))[0:imgSize, 0:imgSize]
	tempBgImg = cv2.resize(backgroundImg,(int(img.shape[0]/4), int(img.shape[1]/4)))[0:imgSize, 0:imgSize]

	tempImg = tempImg.astype(np.int32)
	tempBgImg = tempBgImg.astype(np.int32)

	tempImg[:,:,0] = tempImg[:,:,0]-(tempImg[:,:,0]%quantizeVal)
	tempImg[:,:,1] = tempImg[:,:,1]-(tempImg[:,:,1]%quantizeVal)
	tempImg[:,:,2] = tempImg[:,:,2]-(tempImg[:,:,2]%quantizeVal)

	tempBgImg[:,:,0] = tempBgImg[:,:,0]-(tempBgImg[:,:,0]%quantizeVal)
	tempBgImg[:,:,1] = tempBgImg[:,:,1]-(tempBgImg[:,:,1]%quantizeVal)
	tempBgImg[:,:,2] = tempBgImg[:,:,2]-(tempBgImg[:,:,2]%quantizeVal)

	diff = abs((tempImg[:,:,0] - tempBgImg[:,:,0]))		\
			 + abs((tempImg[:,:,1] - tempBgImg[:,:,1]))		\
			 + abs((tempImg[:,:,2] - tempBgImg[:,:,2]))

	mask = diff > maskThreshold
	processedImg = np.zeros((imgSize, imgSize))
	processedImg[mask] = [255]

class Camera:
	def __init__(self, width, height):
		self.width = width
		self.height = height

	def webcam(self):
		global maskSizeSet
		global mask
		global backgroundImg
		global maskThreshold
		global diff
		global quantizeVal
		global processedImg
		global imgIndex
		global imgClass

		cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

		if not cam.isOpened():
			raise IOError("Unable to open webcam")

		cam.set(3, self.width)
		cam.set(4, self.height)

		while True:
			tStart = int(round(time.time() * 1000))
			
			ret, frame = cam.read()

			if(not maskSizeSet):
				backgroundImg = np.array(frame)
				maskSizeSet = True

			preProcessImg(img = frame)
			
			k = cv2.waitKey(33)
			if k == ord('q'):
				break
			elif k == ord('z'):
				backgroundImg = np.array(frame)
				print('Background Updated')
			elif k == ord('w'):
				maskThreshold += 3
				print('Mask Threshold: ',maskThreshold)
			elif k == ord('s'):
				maskThreshold -= 3
				print('Mask Threshold: ',maskThreshold)
			elif k == ord('a'):
				quantizeVal -= 5
				print('Quantize Val: ',quantizeVal)
			elif k == ord('d'):
				quantizeVal += 5
				print('Quantize Val: ',quantizeVal)
			elif k == ord('i'):
				print('Input index to start with:')
				imgIndex = int(input())
				print('Start Idex with: ',imgIndex)
			elif k == ord('c'):
				print('Input class:')
				imgClass = str(input())
				print('Class: ',imgClass)
			elif k == 32:
				name = str(imgIndex)+'-'+imgClass+'.png'
				cv2.imwrite('data\\test\\'+name, processedImg)
				imgIndex += 1
				print('Image saved: ',name)
		
			cv2.imshow('Img', cv2.resize(cv2.flip(processedImg,1), (800,800)))

		cam.release()
		cv2.destroyAllWindows()


if __name__ == "__main__":
    video = Camera(720, 1280)
    video.webcam()