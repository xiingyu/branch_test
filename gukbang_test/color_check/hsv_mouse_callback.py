import cv2
import numpy as np
import pyrealsense2 as rs


img_size_x = 848
img_size_y = 480
depth_size_x = 848
depth_size_y = 480

### realsense setting ###

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.color, img_size_x,     img_size_y,    rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, depth_size_x,   depth_size_y,  rs.format.z16, 30)
depth_profile = pipeline.start(config)

depth_sensor = depth_profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()

clipping_distance_in_meters = 1 #1 meter
clipping_distance = clipping_distance_in_meters / depth_scale

align_to = rs.stream.color
align = rs.align(align_to)
hole_filling_filter = rs.hole_filling_filter()\

#########################


lower_bound = np.array((17, 10, 10)) # 너무 많이 인식하면 20으로, 인식을 잘 못 하면 15로 (혹은 16)
upper_bound = np.array((130, 255, 255))
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)) ## 추가된 부분

# HSV 값을 저장할 변수를 선언합니다.
hsv_value = None

# 마우스 콜백 함수
def get_hsv_value(event, x, y, flags, param):
    global hsv_value
    if event == cv2.EVENT_MOUSEMOVE:  # 마우스가 움직일 때
        hsv_value = copy_hsv[y, x]
    elif event == cv2.EVENT_LBUTTONDOWN:  # 마우스를 클릭할 때
        print(f"Clicked HSV: {copy_hsv[y, x]}")  # 클릭한 위치의 HSV 값을 출력


while True :
    
    frames          = pipeline.wait_for_frames()
    aligned_frames  = align.process(frames)
    
    color_frame            = aligned_frames.get_color_frame()
    aligned_depth_frame    = aligned_frames.get_depth_frame()
    filled_depth_frame     = hole_filling_filter.process(aligned_depth_frame)
    
    depth_intrinsics = aligned_depth_frame.profile.as_video_stream_profile().intrinsics
    
    depth_img = np.asanyarray(filled_depth_frame.get_data())
    color_img = np.asanyarray(color_frame.get_data())
    
    
    
    color_blurd = cv2.GaussianBlur(color_img, (5, 5), 0) # 블러 처리. 홀수만 가능.
    color_open = cv2.morphologyEx(color_blurd, cv2.MORPH_OPEN, kernel) ### 추가된 부분
    color_close = cv2.morphologyEx(color_open, cv2.MORPH_CLOSE, kernel) ### 추가된 부분
    
    ######## HSV
    copy_close = color_close.copy()
    hsv_img = np.zeros_like(copy_close)
    
    copy_hsv = cv2.cvtColor(copy_close, cv2.COLOR_BGR2HSV)
    hsv_mask = cv2.inRange(copy_hsv, lower_bound, upper_bound)
    hsv_img = cv2.bitwise_and(copy_hsv, copy_hsv ,mask=hsv_mask)
    
    filterd = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)
    
    
    
    
    
    
    
    cv2.imshow("color", color_img)
    cv2.imshow("color_close", color_close)
    # cv2.imshow("hsv", hsv_mask)
    cv2.imshow("hsv", filterd)
    
    cv2.setMouseCallback('color', get_hsv_value)
    
    key = cv2.waitKey(1) 
    if key == ord('q') :
        break

cv2.destroyAllWindows
    
