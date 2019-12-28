import os
import cv2
from serial import SerialNumber

class Camera:
	def __init__(self,capture=0,save_path="./camera_image/",img_size=(600,400)):
		self.camera = cv2.VideoCapture(capture)
		self.img_size = img_size
		self.save_path = save_path
		self.__serial = SerialNumber.get_instance()
		if not os.path.exists(self.save_path) :
			os.mkdir(self.save_path)
	
	def __check_difference(self,imgs):
		grayScaleImages = []
		for img in imgs :
			grayScaleImages.append(cv2.cvtColor(img,cv2.COLOR_RGB2GRAY))
		# 絶対差分を調べる
		diff1 = cv2.absdiff(grayScaleImages[0],grayScaleImages[1])
		diff2 = cv2.absdiff(grayScaleImages[1],grayScaleImages[2])
		# 論理積を調べる
		diff_and = cv2.bitwise_and(diff1, diff2)
		# 白黒二値化
		_, diff_wb = cv2.threshold(diff_and, 30, 255, cv2.THRESH_BINARY)
		# ノイズの除去
		diff = cv2.medianBlur(diff_wb, 5)
		return cv2.countNonZero(diff)

	def check_motion(self,imgs,threshold=300):
		diff = self.__check_difference(imgs)
		filename = None
		if diff > threshold :
			print("動きを検出しました")
			filename = self.save_path + str(self.__serial.get_next_serial()) + ".jpg"
			cv2.imwrite(filename, imgs[2])
		return imgs[1],imgs[2],self.get_image(),filename

	def get_alteranation_image_path(self):
		img1 = img2 = img3 = self.get_image()
		while True :
			if self.waitkey(1) == 13:
				break
			imgs = [img1,img2,img3]
			img1,img2,img3,image_path = self.check_motion(imgs)
			if image_path != None :
				return image_path

	def get_image(self):
		img = self.camera.read()[1]
		img = cv2.resize(img,self.img_size)
		return img

	def waitkey(self,num):
		return cv2.waitKey(num)