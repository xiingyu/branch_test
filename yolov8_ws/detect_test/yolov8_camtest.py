import cv2
from ultralytics import YOLO

###without depth,    0 is color, 2 is gray
###wth depth,        3 4


def main() :
    cam_number = 0
    
    cap = cv2.VideoCapture(cam_number)
    model = YOLO('yolov8n.pt')
    
    while True :
        ret, img = cap.read()
        
        if not ret : 
            print(f'fail to connect to {cam_number}')
            
        else :
            
            result_img = model(img)
            for r in result_img :
                print(r.boxes.cls.detach().numpy().tolist())
            
            annotated_img = result_img[0].plot()
            
            
            cv2.imshow('origin', img)
            cv2.imshow('yolov8 [0]', annotated_img)
            
            key = cv2.waitKey(1)
            if key == ord('q') :
                break
            
    cv2.destroyAllWindows()
    cap.release()


if __name__ == "__main__" :
    main()