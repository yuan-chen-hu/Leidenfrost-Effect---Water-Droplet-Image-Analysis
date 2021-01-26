import cv2
import numpy as np 
vidcap = cv2.VideoCapture('20201102_中心溫度_275_230_212_40_水.mp4')
success,img = vidcap.read()
count = 0
size_of_heat_metal=1080
while success:
	print("count: ",count)



	#if(count>-1):
	print('Read a new frame: ',success)			
	#print("y=")
	y=len(img)
	#print(y)
	#print("x=")
	x=len(img[0])
	#print(x)
	#print("bgr=")
	#bgr=len(img[0,0])
	#print(bgr)  
	tempi=int(y/2)-size_of_heat_metal
	tempj=int(x/2)-size_of_heat_metal


	crop_img = img[tempi:tempi+2*size_of_heat_metal, tempj:tempj+2*size_of_heat_metal]
	"""
	for i in range(0,2*size_of_heat_metal):
		for j in range(0,2*size_of_heat_metal):
			output_img[i][j]=img[tempi+i][tempj+j]
	"""
	cv2.imwrite('cut'+str(count)+'.jpg', crop_img)

	

	success,img = vidcap.read()	
	count += 1