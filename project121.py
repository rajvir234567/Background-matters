import cv2
import time
import numpy as np

code_4cc = cv2.VideoWriter_fourcc(*'XVID')
output_video = cv2.VideoWriter('output.avi', code_4cc, 20.0, (640, 480))

cam_object = cv2.VideoCapture(0)

time.sleep(2)

bg = 0
img = 0
for i in range(60):
    ret, bg = cam_object.read()

bg = np.flip(bg,axis = 1)   

while(cam_object.isOpened()):
    ret, img = cam_object.read()

    img = np.flip(img,axis = 1)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 120, 50])
    upper_red = np.array([10, 255,255])

    mask_1 = cv2.inRange(hsv, lower_red, upper_red)


    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255,255])

    mask_2 = cv2.inRange(hsv, lower_red, upper_red)

    mask_1 = mask_1 + mask_2

    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask_1 = cv2.morphologyEx(mask_1, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

    mask_2 = cv2.bitwise_not(mask_1)
    
    #Keeping only the part of the images without the red color 
    res_1 = cv2.bitwise_and(img ,img ,mask = mask_2)
    #Keeping only the part of the images with the red color 
    res_2 = cv2.bitwise_and(bg ,bg ,mask = mask_1)

    
    final_output = cv2.addWeighted(res_1,1, res_2, 1, 0)

    output_video.write(final_output)

    #Displaying the output to the user
    cv2.imshow("magic", final_output)
    cv2.waitKey(1)


cam_object.release()

cv2.destroyAllWindows()