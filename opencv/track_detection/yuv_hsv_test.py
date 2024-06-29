import cv2
import numpy as np
import pyrealsense2 as rs

import matplotlib.pyplot as plt

cam_num = 5

def hsv_detection(img, lower=(110,50,50), upper=(130,255,255)) :
    gaussian = cv2.GaussianBlur(img, (0, 0), 1)
    hsv_img = cv2.cvtColor(gaussian, cv2.COLOR_BGR2HSV)
    
    hsv_lower = np.array(lower)
    hsv_upper = np.array(upper)
    
    hsv_mask = cv2.inRange(hsv_img, hsv_lower, hsv_upper)
    
    filterd = cv2.bitwise_and(hsv_img, hsv_img, mask=hsv_mask)
    filterd_img = cv2.cvtColor(filterd, cv2.COLOR_HSV2BGR)
    
    return filterd_img

def yuv_detection(img) :
    gaussian = cv2.GaussianBlur(img, (0, 0), 1)
    yuv_img = cv2.cvtColor(gaussian, cv2.COLOR_BGR2YUV)
    Y_img, U_img, V_img = cv2.split(yuv_img)
    
    rescale = np.clip(U_img - V_img, 0, 255).astype(np.uint8)
    ret,U_img_treated = cv2.threshold(U_img, 140, 255, cv2.THRESH_BINARY)
    if ret :
        filterd = cv2.bitwise_and(img, img, mask=U_img_treated)
        # cv2.imshow("U_img", U_img)
        # cv2.imshow("V_img", V_img)
        cv2.imshow("rescale",rescale)
        cv2.imshow("UUUU", filterd)
    
    


def main() :
    
    cap = cv2.VideoCapture(cam_num)
    
    while True :
        ret, image = cap.read()
        
        if not ret :
            print("fail")
            
        else :
            
            yuv_detection(image)
            hsv = hsv_detection(image)
            
            cv2.imshow("hsv", hsv)
            
            
            # Y_img = np.clip(Y_img* 1.5, 0 ,255).astype(np.uint8)
            # up_scale = cv2.merge([Y_img,U_img,V_img])
            
            
            cv2.imshow("origin_img", image)
            # cv2.imshow("yuv", yuv_image)
            # cv2.imshow("Y", Y_img)
            # cv2.imshow("U", U_img)
            # cv2.imshow("V", V_img)
            
            
            key = cv2.waitKey(1)
            if key == ord('q') :
                break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__" :
    main()