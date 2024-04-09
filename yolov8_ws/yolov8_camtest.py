import cv2
from ultralytics import YOLO

###without depth,    0 is color, 2 is gray
###wth depth,        3 4


def main() :
    cam_number = 0
    
    cap = cv2.VideoCapture(cam_number)
    
    while True :
        ret, img = cap.read()
        
        if not ret : 
            print(f'fail to connect to {cam_number}')
            
        else :
            cv2.imshow('Title', img)
            
            key = cv2.waitKey(1)
            if key == ord('q') :
                break
            
    cv2.destroyAllWindows()
    cap.release()


if __name__ == "__main__" :
    main()