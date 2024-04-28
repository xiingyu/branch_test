import cv2
import numpy as np
import math

def pre_treatment_img(origin_img) :
    gray = cv2.cvtColor(origin_img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (0,0),1)
    
    Y, X = gray.shape
    
    ### color match
    ### hsv or histogram
    ###
    
    
    ###low light improvement
    Flatten_gray = np.array(gray).flatten()
    mean = np.mean(Flatten_gray)
    
    if mean >= 70 : 
        gray = gray
    elif mean >= 50 :
        gray = np.clip(gray + 15., 0, 255).astype(np.uint8)
    elif mean >= 40 : 
        gray = cv2.medianBlur(gray,3)
        gray = np.clip(gray + 35., 0, 255).astype(np.uint8)
    else :
        gray = cv2.medianBlur(gray,5)
        gray = np.clip(gray + 60., 0, 255).astype(np.uint8)
        
    ### end   ###
    ### slice ###
    sliced_img = gray.copy()
    
    sliced_img[:int(Y/2)+int(Y*0.1) ,:]= 0
    sliced_img[int(Y*0.9):,:] = 0
    sliced_img[:,:int(X*0.1)] = 0
    sliced_img[:,int(X*0.9):] = 0
    
    
    _, thresh = cv2. threshold(sliced_img, 90, 255, cv2.THRESH_BINARY)
    # athresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    # result = np.hstack((gray,thresh, athresh))
    
    
    ### canny
    canny_img = cv2.Canny(sliced_img, 200, 360)
    
    ###hough
    lines = cv2.HoughLinesP(canny_img, 1, np.pi/180, 25, None, 40, 5)
    print(len(lines))
    for line in lines :
        x1, y1, x2, y2 = line[0]
        cv2.line(origin_img, (x1,y1), (x2,y2), (0,255,0), 1)
    
    
    result0 = np.hstack((gray, thresh, canny_img))
    result1 = origin_img
    
    
    
        
    return result0, result1
        
    
    


def main() :
    cap = cv2.VideoCapture(0)
    
    while True :
        ret, img = cap.read()
        
        Y, X, _ = img.shape
        
        # print(img.shape) 480 640 3
        
        if not ret :
            print("fail")
            
        else :
            
            
            test0, test1 = pre_treatment_img(img)
            cv2.rectangle(img, (int(X*0.1),int(Y/2 + Y*0.1)),(int(X*0.9),int(Y*0.9)),(255,0,0), 2)
            
            
            
            cv2.imshow('Origin',img)
            cv2.imshow('Test0', test0)
            cv2.imshow('Test1', test1)
            
            key = cv2.waitKey(1)
            if key == ord('q') :
                break
    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__" :
    main()