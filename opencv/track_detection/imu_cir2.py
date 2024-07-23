import pyrealsense2 as rs
import time

import numpy as np
import math

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.accel)
pipeline.start(config)


time_period = 0.05

tilt_array = []
def initialize() :
    global tilt_array
    
    frames = pipeline.wait_for_frames()
    accel_frame = frames[0].as_motion_frame()
    if accel_frame:
        accel_data = accel_frame.get_motion_data()
    
    for i in range(5) :
        tilt_array.append([accel_data.x,accel_data.y,accel_data.z])
        

try:
    initialize()
    
    while True :
        start = time.time()
        frames = pipeline.wait_for_frames()
        accel_frame = frames[0].as_motion_frame()
        if accel_frame:
            accel_data = accel_frame.get_motion_data()
            
            tilt_array.pop(0)
            tilt_array.append([accel_data.x,accel_data.y,accel_data.z])
            
            avg_tilt_array = np.mean(tilt_array, axis=0)
            print(avg_tilt_array)
                
            tilted_roll_angle = math.atan2(-avg_tilt_array[0], -avg_tilt_array[1]) /math.pi * 180
            
        print(tilted_roll_angle)
        print("Accel Data:", accel_data)

        end = time.time()
        time.sleep(max(0, time_period - (end-start)))
        
finally:
    pipeline.stop()
