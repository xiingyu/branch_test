import cv2
import numpy as np


cam_num = 0


def main() :
    
    
    cap = cv2.VideoCapture(cam_num)
    
    while True :
        ret, img = cap.read()
        
        if not ret :
            print(f'fail to connect {cam_num}')
            
        else :
            result = cv2.resize(img, (28,28) ,cv2.INTER_CUBIC)
            print(img.shape)
            print(f'img[0] is {img[0]}')
            print(f'img[0][0] is {img[0][0]}')
            print(f'img[0][0][0] is {img[0][0][0]}')
            
            result[14][:][:] = 0
            cv2.imshow('origin', result)
            
            key = cv2.waitKey(1000)
            if key == ord('q') :
                break
    
    cv2.destroyAllWindows()
    cap.release()
    
if __name__ == "__main__" :
    main()