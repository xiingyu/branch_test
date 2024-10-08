import cv2
import numpy as np
import pyrealsense2 as rs

import matplotlib.pyplot as plt


###################################
# ideas...
# two roi set. -> track roi, mission roi.
# finite state machine by mission roi.
##################################


########### parameters ###########

cam_num = 4
U_detection_threshold = 140 ## 0~255
img_size_x = 1280
img_size_y = 720

#################################

def hsv_detection(img, lower=(100,20,20), upper=(130,255,255)) :
    gaussian = cv2.GaussianBlur(img, (0, 0), 1)
    hsv_img = cv2.cvtColor(gaussian, cv2.COLOR_BGR2HSV)
    
    hsv_lower = np.array(lower)
    hsv_upper = np.array(upper)
    
    hsv_mask = cv2.inRange(hsv_img, hsv_lower, hsv_upper)
    
    filterd = cv2.bitwise_and(hsv_img, hsv_img, mask=hsv_mask)
    filterd_img = cv2.cvtColor(filterd, cv2.COLOR_HSV2BGR)
    
    return filterd_img

def yuv_detection(img) :
    gaussian = cv2.GaussianBlur(img, (3, 3), 1)
    yuv_img = cv2.cvtColor(gaussian, cv2.COLOR_BGR2YUV)
    Y_img, U_img, V_img = cv2.split(yuv_img)
    
    # rescale = np.clip(U_img - V_img, 0, 255).astype(np.uint8)
    ret,U_img_treated = cv2.threshold(U_img, U_detection_threshold, 255, cv2.THRESH_BINARY)
    if ret :
        filterd = cv2.bitwise_and(img, img, mask=U_img_treated)
        cv2.imshow("UUUU", filterd)
        
        
##무쓸모... 내 아이디어지만 병신임 그냥
def yuv_hsv_collabo(img) :
    gaussian = cv2.GaussianBlur(img, (3, 3), 1)
    
    hsv_img = cv2.cvtColor(gaussian, cv2.COLOR_BGR2HSV)
    hsv_lower = np.array((100,20,20))
    hsv_upper = np.array((130,255,255))
    hsv_mask = cv2.inRange(hsv_img, hsv_lower, hsv_upper)
    ret, hsv_mask = cv2.threshold(hsv_mask, U_detection_threshold, 255, cv2.THRESH_BINARY_INV)
    hsv_mask = hsv_mask.astype(np.int16)
    
    yuv_img = cv2.cvtColor(gaussian, cv2.COLOR_BGR2YUV)
    Y_img, U_img, V_img = cv2.split(yuv_img)
    ret, U_img_treated = cv2.threshold(U_img, U_detection_threshold, 255, cv2.THRESH_BINARY)
    U_img_treated = U_img_treated.astype(np.int16)
    
    rescale = np.clip(U_img_treated - hsv_mask, 0, 255).astype(np.uint8)
    filterd = cv2.bitwise_and(img, img, mask=rescale)
    cv2.imshow("improved filterd color", filterd)
    
    
def get_histo(image) :
    return 0
    


def main() :
    
    cap = cv2.VideoCapture(cam_num)
    
    print(f'set resolution width {img_size_x} height {img_size_y}')
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, img_size_x)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, img_size_y)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f'changed resolution width {width} height {height}')
    
    while True :
        ret, image = cap.read()
        
        if not ret :
            print("fail")
            
        else :
            
            yuv_detection(image)
            yuv_hsv_collabo(image)
            hsv = hsv_detection(image)
            
            cv2.imshow("hsv", hsv)
            
            
            # Y_img = np.clip(Y_img* 1.5, 0 ,255).astype(np.uint8)
            # up_scale = cv2.merge([Y_img,U_img,V_img])
            
            
            cv2.imshow("origin_img", image)
            
            
            key = cv2.waitKey(1)
            if key == ord('q') :
                break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__" :
    main()