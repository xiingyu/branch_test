import cv2
import numpy as np
from ultralytics import YOLO

###without depth,    0 is color, 2 is gray
###wth depth,        3 4

def apply_yolo(image) :
    model = YOLO('yolov8n.pt')
    result = model(image)
    
    # for r in result :
    #     print(f'{r.boxes}')
    
    ### numpy().tolist() mean, array to python list. array의 차원을 그대로 가져감.
    
    object_xywh = np.array(result[0].boxes.xywh.detach().numpy().tolist()[0], dtype='int')
    object_xywhn = np.array(result[0].boxes.xywhn.detach().numpy().tolist()[0], dtype='int')
    object_xyxy = np.array(result[0].boxes.xyxy.detach().numpy().tolist()[0], dtype='int')
    object_xyxyn = np.array(result[0].boxes.xyxyn.detach().numpy().tolist()[0], dtype='int')
    print(object_xywh)
    print(object_xywhn)
    print(object_xyxy)
    print(object_xyxyn)
    # for r in result :
    #     print(r.boxes.xywh.detach().numpy().tolist())
    #     print(r.boxes.xywhn.detach().numpy().tolist())
    #     print(r.boxes.xyxy.detach().numpy().tolist())
    #     print(r.boxes.xyxyn.detach().numpy().tolist())
    
    
    annotated_img = result[0].plot()
    
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
            
            key = cv2.waitKey(1000)
            if key == ord('q') :
                break
            
    cv2.destroyAllWindows()
    cap.release()


if __name__ == "__main__" :
    main()