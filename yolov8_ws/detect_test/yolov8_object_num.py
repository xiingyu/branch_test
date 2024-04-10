import cv2
import numpy as np
from ultralytics import YOLO

###without depth,    0 is color, 2 is gray
###wth depth,        3 4

def apply_yolo(image) :
    result = model.predict(image, classes=[0., 67.], conf= 0.25)
    annotated_img = result[0].plot()
    
    
    for r in result :
        print(r.boxes)
    
    return annotated_img


def main() :
    cam_number = 0
    cap = cv2.VideoCapture(cam_number)
    
    while True :
        ret, img = cap.read()
        
        if not ret : 
            print(f'fail to connect to {cam_number}')
            
        else :
            yoloed = apply_yolo(img)            
            
            cv2.imshow('origin', img)
            cv2.imshow('yolov8 [0]', yoloed)
            
            key = cv2.waitKey(1)
            if key == ord('q') :
                break
            
    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__" :
    model = YOLO('yolov8n.yaml')
    model = YOLO('yolov8n.pt')
    main()