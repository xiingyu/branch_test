import pyrealsense2 as rs
import numpy as np
import cv2
import time

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

profile = pipeline.start(config)

###0.0010000000474974513
###fuxking this scale value means, pixel number per 1m
print(profile.get_device().first_depth_sensor().get_depth_scale())

# Getting the depth sensor's depth scale (see rs-align example for explanation)
# depth_sensor = profile.get_device().first_depth_sensor()
# depth_scale = depth_sensor.get_depth_scale()
# print("Depth Scale is: " , depth_scale)

for i in range(0,100) :
    print(profile.get_device().first_depth_sensor().get_depth_scale())
    time.sleep(0.01)
    
