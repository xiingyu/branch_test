import cv2
import pyrealsense2 as rs
import numpy as np
from ultralytics import YOLO

chess_model = YOLO('/home/skh/robot_ws/src/gukbang/gukbang/common/chess.pt')



# 클릭 이벤트에 대한 콜백 함수
def get_hsv_value(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # 마우스 왼쪽 버튼 클릭 이벤트
        # 현재 프레임에서 클릭한 지점의 색상 가져오기
        bgr_color = frame[y, x]
        
        # BGR을 HSV로 변환
        hsv_color = cv2.cvtColor(bgr_color.reshape(1, 1, 3), cv2.COLOR_BGR2HSV)
        yuv_color = cv2.cvtColor(bgr_color.reshape(1, 1, 3), cv2.COLOR_BGR2YUV)
        
        # HSV 값 출력
        print(f"Clicked at ({x}, {y}), HSV: {hsv_color[0][0]}   YUV: {yuv_color[0][0]}")
        

# 카메라 초기화
### realsense setting ###
img_size_x = 848
img_size_y = 480
depth_size_x = 848
depth_size_y  = 480

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.color, img_size_x,     img_size_y,    rs.format.bgr8, 15)
config.enable_stream(rs.stream.depth, depth_size_x,   depth_size_y,  rs.format.z16, 15)


depth_profile = pipeline.start(config)
device = depth_profile.get_device()
color_sensor = device.query_sensors()[1]  # Color sensor 사용

# 수동 화이트밸런스 값 설정 (기본값: 4600, 범위: 2800 ~ 6500)
color_sensor.set_option(rs.option.white_balance, 3500)  # 원하는 값으로 설정

depth_sensor = depth_profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()

clipping_distance_in_meters = 1 #1 meter
clipping_distance = clipping_distance_in_meters / depth_scale

align_to = rs.stream.color
align = rs.align(align_to)
hole_filling_filter = rs.hole_filling_filter()



#########################

# 창에 콜백 함수 설정
cv2.namedWindow('Camera')
cv2.setMouseCallback('Camera', get_hsv_value)

# 실시간 영상 처리
while True:
        
    frames          = pipeline.wait_for_frames()
    aligned_frames  = align.process(frames)
    
    color_frame                 = aligned_frames.get_color_frame()
    aligned_depth_frame    = aligned_frames.get_depth_frame()
    filled_depth_frame     = hole_filling_filter.process(aligned_depth_frame)
    
    depth_intrinsics = aligned_depth_frame.profile.as_video_stream_profile().intrinsics
    
    depth_img = np.asanyarray(filled_depth_frame.get_data())
    frame = np.asanyarray(color_frame.get_data())
    
    result = chess_model.predict(frame, conf = 0.6, verbose=False,max_det=1)
    plot_img = result[0].plot()
    
     
    # 영상 출력
    cv2.imshow('Camera', frame)
    cv2.imshow('plot_img', plot_img)
    
    if cv2.waitKey(1) & 0xFF == 27:  # ESC 키를 누르면 종료
        break

# 자원 해제
cv2.destroyAllWindows()


