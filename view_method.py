import pyrealsense2 as rs
import time

import numpy as np

pipeline = rs.pipeline()
config = rs.config()

# config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
# config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.accel)
# config.enable_stream(rs.stream.gyro)
# config.enable_stream(rs.stream.any)
# config.enable_stream(rs.stream.confidence)
# config.enable_stream(rs.stream.fisheye)
# config.enable_stream(rs.stream.gpio)
# config.enable_stream(rs.stream.infrared, 1, 640, 480, rs.format.y8, 30)  # 적외선 스트림 1 설정
# config.enable_stream(rs.stream.name)
# config.enable_stream(rs.stream.pose)
# config.enable_stream(rs.stream.value)

pipeline.start(config)

try:
    # frames = pipeline.wait_for_frames()
    # print(len(frames))
    
    while True :
        frames = pipeline.wait_for_frames()
        accel_frame = frames[0].as_motion_frame()
        if accel_frame:
            accel_data = accel_frame.get_motion_data()
            print("Accel Data:", accel_data)
        
            time.sleep(0.05)
    # motion_data = motion_frame.get_motion_data()
    # print(dir(frames.as_pose_frame))
    # print(dir(motion_data))
        
finally:
    pipeline.stop()
