import cv2
import numpy as np
import pyrealsense2 as rs
import math

img_size_x = 1280
img_size_y = 720   
thresh_value = 120
thresh_max = 160
thresh_min = 50
thresh_weight = 1


def pre_treatment_img(origin_img) :
    global thresh_value, thresh_max, thresh_min, thresh_weight
    
    ### color match
    hsv_color = cv2.cvtColor(origin_img, cv2.COLOR_BGR2HSV)
    hsv_lower = np.array([10,20,20])
    hsv_upper = np.array([35,255,255])
    
    hsv_mask = cv2.inRange(hsv_color, hsv_lower, hsv_upper)
    
    
    # erosion0 = cv2.erode(hsv_mask, (3,3), iterations=5)
    # dilation0 = cv2.dilate(erosion0, (5,5), iterations=5)
    # morphologed_mask = cv2.erode(dilation0, (3,3), iterations=2)
    
    hsv_filterd = cv2.bitwise_and(hsv_color, hsv_color, mask=hsv_mask)
    color_filterd = cv2.cvtColor(hsv_filterd, cv2.COLOR_HSV2BGR)
    cv2.imshow("filterd",color_filterd)

    ### hsv or histogram
    ###
    
    gray = cv2.cvtColor(color_filterd, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (0,0),1)
    
    Y, X = gray.shape
    
    
    ###low light improvement
    Flatten_gray = np.array(gray).flatten()
    mean = np.mean(Flatten_gray)
    # print(mean)
    if mean >= 150 : 
        gray = np.clip(gray - 30., 0, 255).astype(np.uint8)
    elif mean >= 100 :
        gray = gray
    elif mean >= 75 :
        gray = np.clip(gray + 15., 0, 255).astype(np.uint8)
    elif mean >= 45 : 
        gray = cv2.medianBlur(gray,3)
        gray = np.clip(gray + 35., 0, 255).astype(np.uint8)
    else :
        gray = cv2.medianBlur(gray,5)
        gray = np.clip(gray + 60., 0, 255).astype(np.uint8)
        
    ### end   ###
    ### slice ###
    sliced_img = gray[int(Y*0.7):int(Y*0.9),int(X*0.1):int(X*0.9)]
    
    
    _, thresh = cv2. threshold(sliced_img, thresh_value, 255, cv2.THRESH_BINARY)
    # athresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    # result = np.hstack((gray,thresh, athresh))
    
    
    ### canny
    canny_img = cv2.Canny(sliced_img, 200, 360)
    
    ###hough
    lines = cv2.HoughLinesP(canny_img, 1, np.pi/360, 50, None, 50, 5)
    # lines = cv2.HoughLines(canny_img, 1, np.pi/180, 25)
    if lines is not None :    
        print(len(lines))
        for line in lines :
            x1, y1, x2, y2 = line[0]
            cv2.line(origin_img, (x1 + int(X*0.1),y1 + int(Y*0.7)), (x2 + int(X*0.1),y2 + int(Y*0.7)), (0,255,0), 3)
            
            # if (thresh_value < thresh_max) and (thresh_weight < 10) :
            #     thresh_value = thresh_value +1
            #     thresh_weight = thresh_weight +1
            # else :
            #     thresh_weight = thresh_weight +1
    # else :
        # if (thresh_value > thresh_min)  and (thresh_weight < 100):
        #     thresh_value = thresh_value - 1
        # else : 
        #     thresh_weight = thresh_weight - 1
    
    # result0 = np.hstack((gray, thresh, canny_img))
    # result1 = origin_img
    
    
    
        
    return thresh, origin_img
        
    
    


def main() :
    
    pipeline = rs.pipeline()
    config = rs.config()

    config.enable_stream(rs.stream.depth,img_size_x,img_size_y, rs.format.z16, 30)
    config.enable_stream(rs.stream.color,img_size_x,img_size_y, rs.format.bgr8, 30)
    
    profile = pipeline.start(config)    
    # cap = cv2.VideoCapture(8)
    
    while True :
        
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_img = np.asanyarray(color_frame.get_data())
        
        # ret, color_img = cap.read()
        
        Y, X, _ = color_img.shape
        
        # print(color_img.shape) 480 640 3
        
        
        test0, test1 = pre_treatment_img(color_img)
        cv2.rectangle(color_img, (int(X*0.1),int(Y*0.7)),(int(X*0.9),int(Y*0.9)),(255,0,0), 2)
        cv2.line(color_img, (int(X*0.1),int(Y*0.8)),(int(X*0.9),int(Y*0.8)),(255,0,0), 2)
        
        
        cv2.imshow('Origin',color_img)
        cv2.imshow('Test0', test0)
        cv2.imshow('Test1', test1)
        
        key = cv2.waitKey(1)
        if key == ord('q') :
            break
    cv2.destroyAllWindows()
    # cap.release()

if __name__ == "__main__" :
    main()