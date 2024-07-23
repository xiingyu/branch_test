import pyrealsense2 as rs
import time

import numpy as np
import math

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.accel)
pipeline.start(config)


time_period = 0.05

try:
    
    while True :
        start = time.time()
        frames = pipeline.wait_for_frames()
        accel_frame = frames[0].as_motion_frame()
        if accel_frame:
            accel_data = accel_frame.get_motion_data()
            
            if not (accel_data.y == 0) :
                tilted_roll_angle = math.atan2(-accel_data.x, -accel_data.y) /math.pi * 180
                print(tilted_roll_angle)
            print("Accel Data:", accel_data)

            end = time.time()
            time.sleep(max(0, time_period - (end-start)))
        
finally:
    pipeline.stop()
