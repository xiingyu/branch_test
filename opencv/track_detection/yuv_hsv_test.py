import cv2
import numpy as np
import pyrealsense2 as rs

import matplotlib.pyplot as plt

cam_num = 4

def hsv_detection(img, upper=(), lower) :




def main() :
    
    cap = cv2.VideoCapture(cam_num)
    
    while True :
        ret, image = cap.read()
        
        if not ret :
            print("fail")
            
        else :
            yuv_image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
            print(f'shape : {yuv_image.shape}')
            
            Y_img, U_img, V_img = cv2.split(yuv_image)
            
            Y_img = np.clip(Y_img* 1.5, 0 ,255).astype(np.uint8)
            up_scale = cv2.merge([Y_img,U_img,V_img])
            
            
            cv2.imshow("origin_img", image)
            cv2.imshow("yuv", yuv_image)
            cv2.imshow("Y", Y_img)
            cv2.imshow("U", U_img)
            cv2.imshow("V", V_img)
            
            
            key = cv2.waitKey(1)
            if key == ord('q') :
                break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__" :
    main()