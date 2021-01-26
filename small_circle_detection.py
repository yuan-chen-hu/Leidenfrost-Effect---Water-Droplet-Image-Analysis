
import cv2 
import numpy as np 
import time 
import mahotas
last_frame_count=650
last_count=0
last_location_y=0
last_location_x=0
last_v_y=0
last_v_x=0
for frame_count in range(last_frame_count+1,25000):
	print(frame_count)
	start_time=time.time()
	input_image_name='cut'+str(frame_count) 
	input_image_name_without_droplets='cut650'
	# Read image. 
	img = cv2.imread(input_image_name+'.jpg', cv2.COLOR_BGR2GRAY) 
	img0= cv2.imread(input_image_name_without_droplets+'.jpg', cv2.COLOR_BGR2GRAY)
	"""
	print("y=")
	y=len(img)
	print(y)
	print("x=")
	x=len(img[0])
	print(x)
	print("bgr=")
	bgr=len(img[0,0])
	print(bgr)  
	print(type(img[0][0][0]))
	"""

	#subtract
	img=cv2.subtract(img,img0,cv2.COLOR_BGR2GRAY)
	#thresholding
	ret,img = cv2.threshold(img,50,255,cv2.THRESH_BINARY)  
	#cv2.imwrite("./frame_file/subtracted of "+str(frame_count)+".jpg",img)
	"""
	for i  in range (y):
		for j in range (x):
			for k in range (bgr):
				temp =int(img[i][j][k])-int(img0[i][j][k])
				if temp<30:
					temp=0
				img[i][j][k]=temp	
	cv2.imwrite("subtracted.jpg",img)
	"""
	# Convert to grayscale. 
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 


	# Blur using 13 * 13 kernel. 
	kernel=17
	gray_blurred = cv2.blur(gray, (kernel,kernel)) 
	  
	# Apply Hough transform on the blurred image. ma

	for p1 in range(30,100,100):#for big droplet =30
		for p2 in range(38,44,20):#for big droplet =38
			print("")
			#Param1: Canny edge detection requires two parameters — minVal and maxVal. Param1 is the higher threshold of the two. The second one is set as Param1/2. By increasing this threshold=>clear edge
			#Param2: This is the accumulator threshold for the candidate detected circles. By increasing this threshold value, we can ensure that only the best circles, corresponding to larger accumulator values, are returned.
			#detected_circles = cv2.HoughCircles(gray_blurred,cv2.HOUGH_GRADIENT, 1, 20, param1 = p1,param2 = p2, minRadius = int((kernel-1)/2), maxRadius = 70) 
			detected_circles = cv2.HoughCircles(gray_blurred,cv2.HOUGH_GRADIENT, 1, 20, param1 = p1,param2 = p2, minRadius = 1, maxRadius = 70)   
			# Draw circles that are detected. 
			count=0
			if detected_circles is not None: 
			
				# Convert the circle parameters a, b and r to integers. 
				detected_circles = np.int32(np.around(detected_circles)) 
				output_img=cv2.imread(input_image_name+'.jpg', cv2.IMREAD_COLOR) 
				for pt in detected_circles[0,:]: 
					a, b, r = pt[0], pt[1], pt[2] 
					#if int(x/2)-size_of_heat_metal<a and a<int(x/2)+size_of_heat_metal and int(y/2)-size_of_heat_metal<b and b<int(y/2)+size_of_heat_metal:
					# Draw the circumference of the circle. 
					cv2.circle(output_img, (a, b), r, (0, 255, 0), 2) 

					# Draw a small circle (of radius 1) to show the center. 
					cv2.circle(output_img, (a, b), 1, (0, 0, 255), 3) 
					count+=1
					#print("there are",count,"circles")
					
					if count>=1000:
						print("too many circles")
						break
				if count ==1:
					time_difference=frame_count-last_frame_count
					print("time_difference=",time_difference)
					v_y=(b-last_location_y)*30/time_difference
					v_x=(a-last_location_x)*30/time_difference
					v=(v_x**2+v_y**2)**(1/2)
					a_y=(v_y-last_v_y)*30/time_difference
					a_x=(v_x-last_v_x)*30/time_difference
					acc=(a_x**2+a_y**2)**(0.5)
					print("v_x=",v_x)
					print("v_y=",v_y)
					print("a_x=",a_x)
					print("a_y=",a_y)
					print("last_location_y=",last_location_y)
					print("last_location_x=",last_location_x)
					print("a=",a)
					print("b=",b)
					last_location_y=b
					last_location_x=a	
					last_v_y=v_y
					last_v_x=v_x
					last_frame_count=frame_count
				else:					
					break

				"""
				if count==last_count:
					status="maintain"		
				if count>last_count:
					status="split"
				if count< last_count:
					status="merge"	
				if count == 0:
					status ="no droplet"	
				last_count=count	
				"""

				#print text 				
				# font 
				font = cv2.FONT_HERSHEY_SIMPLEX 
				  
				# org 
				org = (50,100) 
				  
				# fontScale 
				fontScale = 3
				   
				# Blue color in BGR 
				color = (0, 0, 255) 
				  
				# Line thickness of 2 px 
				thickness = 2
				radius_list=""
				for i in range(len(detected_circles[0])):
					radius_list+=str(detected_circles[0][i][2])
					radius_list+=" "
				#print("radius_list=",radius_list)	
				# Using cv2.putText() method 

				output_img = cv2.putText(output_img, "count="+str(count)+"  p1="+str(p1)+"  p2="+str(p2)+"  kernel="+str(kernel), org, font,fontScale, color, thickness, cv2.LINE_AA)
				fontScale=2
				org=(50,1900)
				output_img = cv2.putText(output_img, "time_difference="+str(time_difference), org, font,fontScale, color, thickness, cv2.LINE_AA)
				org=(50,2000)				
				output_img = cv2.putText(output_img, "radius_list="+radius_list+"  v_x="+str(int(v_x))+" v_y="+str(int(v_y))+"  v="+str(int(v)), org, font,fontScale, color, thickness, cv2.LINE_AA)   
				org=(50,2100)
				output_img = cv2.putText(output_img, "a="+str(a)+" b="+str(b)+" a_x="+str(int(a_x))+"   a_y="+str(int(a_y))+"  a="+str(int(acc)), org, font,fontScale, color, thickness, cv2.LINE_AA)   
				#org=(450,750)
				#output_img = cv2.putText(output_img, " status="+status, org, font,fontScale, color, thickness, cv2.LINE_AA)               	
				cv2.imwrite("./frame_file/Detected Circle of"+input_image_name+" p1="+str(p1)+"p2="+str(p2)+"count="+str(count)+"kernel="+str(kernel)+".jpg", output_img) 
				import csv
				print("csv start")
				with open('temp.csv', 'a', newline='') as csvfile:    
					writer = csv.writer(csvfile, delimiter=',')
					writer.writerow([frame_count,count,p1,p2,kernel,time_difference,radius_list,v_x,v_y,v,a,b,a_x,a_y,acc])
					print("csv done")    
			"""
			print("p1=",p1,"p2=",p2)
			print("circles=",count)
			print("detected_circles=")
			print(detected_circles)
			"""
			"""
			print("test")
			print(detected_circles[0,1,2])
			print(detected_circles[0,0,2])
			"""
			"""
			for ii in range(count):
				haralick_glcm_target_area=np.zeros((2*detected_circles[0,ii,2]+5,2*detected_circles[0,ii,2]+5),dtype=int)
				for i in range (2*detected_circles[0,ii,2]+5):
					for j in range(2*detected_circles[0,ii,2]+5):
						haralick_glcm_target_area[i][j]=int(gray_blurred[detected_circles[0,ii,1]-detected_circles[0,ii,2]-2+i][detected_circles[0,ii,0]-detected_circles[0,ii,2]-2+j] )
				print("haralick glcm of circle#",ii,"=")
				#print(type(haralick_glcm_target_area))
				print(mahotas.features.haralick(haralick_glcm_target_area).mean(axis=0))
			"""
			end_time=time.time()
			total_time=end_time-start_time
			print('total_time=',total_time)
			start_time=time.time()
			cv2.waitKey(0) 
