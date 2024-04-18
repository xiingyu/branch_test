import cv2
import numpy as np

cam_num = 0
circles = []
def mouse_callback(event, x, y, flags, param):
    global circles

    if event == cv2.EVENT_LBUTTONDOWN:
        if len(circles) < 2:
            circles.append((x, y))
            print("클릭한 좌표:", (x, y))

    elif event == cv2.EVENT_RBUTTONDOWN:
        if len(circles) > 0:
            circles.pop()
                  
        

def main() :
    cap = cv2.VideoCapture(cam_num)

    while True:
        ret, img = cap.read()
        if not ret :
            print(f"fail to connect to {cam_num}")
        else :
            
            if circles :
                for circle in circles:
                    img = cv2.circle(img, circle, 20, (255, 0, 0), -1)  # 파란색 원 그리기
                    
            cv2.imshow("image", img)
            cv2.setMouseCallback("image", mouse_callback)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC 키 누르면 종료
            break

    cv2.destroyAllWindows()
    
if __name__ == "__main__" :
    main()