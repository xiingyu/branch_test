import pyrealsense2 as rs
import numpy as np
import cv2

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.infrared, 1, 640, 480, rs.format.y8, 30)  # 적외선 스트림 1 설정
config.enable_stream(rs.stream.infrared, 2, 640, 480, rs.format.y8, 30)  # 적외선 스트림 1 설정

pipeline.start(config)

try:
    while True:
        frames = pipeline.wait_for_frames()
        ir_frame1 = frames.get_infrared_frame(1)
        ir_frame2 = frames.get_infrared_frame(2)
        
        if ir_frame1 and ir_frame2:
            # 적외선 프레임의 데이터를 가져옵니다.
            ir_data1 = np.asanyarray(ir_frame1.get_data())
            ir_data2 = np.asanyarray(ir_frame2.get_data())
            
            # 적외선 데이터는 8비트 단일 채널 이미지입니다.
            img1 = cv2.cvtColor(ir_data1, cv2.COLOR_GRAY2BGR)
            img2 = cv2.cvtColor(ir_data2, cv2.COLOR_GRAY2BGR)
            
            cv2.imshow("Infrared1", img1)
            cv2.imshow("Infrared2", img2)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break

    cv2.destroyAllWindows()

finally:
    pipeline.stop()
