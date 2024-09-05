import cv2
import pyrealsense2 as rs
import numpy as np
from ultralytics import YOLO

chess_model = YOLO('/home/skh/robot_ws/src/gukbang/gukbang/common/chess.pt')

video_path = "/home/skh/testing_folder/opencv/track_detection/last_dance/drive_video.mp4"
cap = cv2.VideoCapture(video_path)


def lab_test(img) :
    # CLAHE 적용 (명도 균일화)
    lab_image = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab_image)

    clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(8,8))
    cl = clahe.apply(l)

    limg = cv2.merge((cl, a, b))
    image_clahe = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    
    return image_clahe


def chat_gpt(img) :

    # YUV 색 공간으로 변환하여 밝기 채널을 정규화
    yuv_image = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    yuv_image[:, :, 0] = cv2.equalizeHist(yuv_image[:, :, 0])

    # 다시 BGR로 변환
    normalized_image = cv2.cvtColor(yuv_image, cv2.COLOR_YUV2BGR)

    # HSV 변환 후 동일한 색상 분류 적용 가능
    # hsv_image = cv2.cvtColor(normalized_image, cv2.COLOR_BGR2HSV)
    
    return normalized_image

def gamma(img) :
    # Gamma 값에 따른 룩업 테이블 생성
    invGamma = 1.0 / 0.7
    table = np.array([(i / 255.0) ** invGamma * 255 for i in np.arange(0, 256)]).astype("uint8")
    
    # 룩업 테이블을 이용한 Gamma 보정
    return cv2.LUT(img, table)

        


def yuv_detection_test(img) :
    # print("yuv")
    y, x, c = img.shape
    
    gaussian1 = cv2.GaussianBlur(img, (9, 9), 2)
    gaussian2 = cv2.GaussianBlur(gaussian1, (9, 9), 2)
    gaussian3 = cv2.GaussianBlur(gaussian2, (9, 9), 2)
    # wb = cv2.xphoto.createSimpleWB()
    # balanced_img = wb.balanceWhite(gaussian)
    yuv_img = cv2.cvtColor(gaussian3, cv2.COLOR_BGR2YUV)
    Y_img, U_img, V_img = cv2.split(yuv_img)
    
    uv_diff = cv2.subtract(U_img, V_img)
    
    # rescale = np.clip(U_img - V_img, 0, 255).astype(np.uint8)
    ret,U_img_treated = cv2.threshold(uv_diff, 12, 255, cv2.THRESH_BINARY)
    
    # U_img_treated = cv2.adaptiveThreshold(U_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #                                     cv2.THRESH_BINARY, 11, 2)

    
    if ret :
        
        contours, _ = cv2.findContours(U_img_treated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        max_area = 0
        max_contour = None
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                max_contour = contour

        if max_contour is not None:
            # print('max')
            max_contour_mask = np.zeros_like(U_img_treated)
            cv2.drawContours(max_contour_mask, [max_contour], -1, (255, 255, 255), thickness=cv2.FILLED)
            
        
            filterd = cv2.bitwise_and(img, img, mask=max_contour_mask)
            cv2.imshow("Camera", filterd)
            cv2.waitKey(1)
    
            histogram = np.sum(max_contour_mask, axis=0)
            midpoint = int(x / 2)
            L_histo = histogram[:midpoint]
            R_histo = histogram[midpoint:]
            
            L_sum = int(np.sum(L_histo) / 255)
            R_sum = int(np.sum(R_histo) / 255) - y
            
            # print(f'{L_sum}   {R_sum}')
            # img_publisher.publish(cvbrid.cv2_to_imgmsg(filterd))
            
            return L_sum, midpoint, R_sum
    return 1,1,1

# 클릭 이벤트에 대한 콜백 함수
def get_hsv_value(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # 마우스 왼쪽 버튼 클릭 이벤트
        # 현재 프레임에서 클릭한 지점의 색상 가져오기
        bgr_color = img[y, x]
        
        # BGR을 HSV로 변환
        hsv_color = cv2.cvtColor(bgr_color.reshape(1, 1, 3), cv2.COLOR_BGR2HSV)
        yuv_color = cv2.cvtColor(bgr_color.reshape(1, 1, 3), cv2.COLOR_BGR2YUV)
        
        # HSV 값 출력
        print(f"Clicked at ({x}, {y}), HSV: {hsv_color[0][0]}   YUV: {yuv_color[0][0]}   bgr_color: {img[y,x]}")
        
        
# 창에 콜백 함수 설정
cv2.namedWindow('Camera')
cv2.setMouseCallback('Camera', get_hsv_value)

while True :
    ret,img = cap.read()
    
    if not ret :
        print(f'fail')
    else :
        result = chess_model.predict(img, conf = 0.6, verbose=False ,max_det=1)
        plot_img = result[0].plot()
        
        
        gammad = gamma(img)
        yuv_detection_test(gammad)
        
        
        cv2.imshow("gammad", gammad)
        cv2.imshow("plot",plot_img)
        key = cv2.waitKey(1)
        if key == ord('q') :
            break
        

# 자원 해제
cv2.destroyAllWindows()
