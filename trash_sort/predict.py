from ultralytics import YOLO
import cv2

### parameter setting ###
img_size_x = 640
img_size_y = 480

frame_rate = 10
#########################
        
        
model = YOLO('/home/skh/testing_folder/trash_sort/deneme-3/runs/detect/train2/weights/best.pt')
cap0 = cv2.VideoCapture('/dev/video0')  #cam0
# cvbrid = CvBridge()

cap0.set(cv2.CAP_PROP_FRAME_WIDTH, img_size_x)
cap0.set(cv2.CAP_PROP_FRAME_HEIGHT, img_size_y)
cap0.set(cv2.CAP_PROP_FPS, frame_rate)
        

# result = self.model.predict(frame, conf = 0.5, verbose=False)

while True :
    ret, img = cap0.read()
    
    if not ret :
        print('camera connection fail')
        
    else :
        results = model.predict(img)
        annotated_img = results[0].plot()
        
        cv2.imshow("img", annotated_img)
        
        
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls)  # 클래스 ID
                confidence = box.conf  # 신뢰도 (0~1 사이 값)
                class_name = model.names[class_id]  # 클래스 이름
                
                print(f"Class: {class_name}, Confidence: {confidence:.2f}")
        key = cv2.waitKey(1)
        if key == ord('q') :
            break
        
    
cv2.destroyAllWindows
cap0.release