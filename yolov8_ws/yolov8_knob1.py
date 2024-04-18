from ultralytics import YOLO
import cv2
import time

cam_num = 0


def main() :
    cap = cv2.VideoCapture(cam_num)
    # model = YOLO('door_knob.yaml')
    model = YOLO('best.pt')

    while True :
        start_time = time.time()
        ret, img = cap.read()
        
        if not ret :
            print(f'fail to connect cam to {cam_num}')
        else :
            result = model.predict(img, classes=[0., 1.], conf= 0.6 ) 
            annotated_img = result[0].plot()
            cv2.imshow('real', img)
            cv2.imshow('yolo',annotated_img)

            key = cv2.waitKey(1)
            end_time = time.time()
            during_time = end_time - start_time
            print(1/during_time)
            if key == ord('q') :
                break
            
    cv2.destroyAllWindows()
    cap.release()


if __name__ == "__main__" :
    main()