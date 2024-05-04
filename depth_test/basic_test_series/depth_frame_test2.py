import pyrealsense2 as rs
import numpy as np
import cv2
import time
import math


pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth,rs.format.z16, 30)
config.enable_stream(rs.stream.color,rs.format.bgr8, 30)
config.enable_stream(rs.stream.accel)
config.enable_stream(rs.stream.gyro)

profile = pipeline.start(config)

###0.0010000000474974513
###fuxking this scale value means, pixel number per 1m
depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()
# print(profile.get_device().first_depth_sensor().get_depth_scale())

clipping_distance_in_meters = 1 #1 meter
clipping_distance = clipping_distance_in_meters / depth_scale
align_to = rs.stream.color
align = rs.align(align_to)


try:
    while True:
        
        frames = pipeline.wait_for_frames()
        
        aligned_frames = align.process(frames)
        
        color_frame = frames.get_color_frame()
        color_img = np.asanyarray(color_frame.get_data())

        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        # ret, img = color_image.read()
        
        print(f'depth_image : {depth_image.shape}')
        print(f'color_image : {color_image.shape}')
        print(f'depth data type : {type(depth_image)}')
        print(f'dtype : {depth_image.dtype}')
        
        cv2.imshow("color_frame", color_image)
        cv2.imshow("depth_frame", depth_image)
        
        # print(f'depth_image : {depth_image.shape}')

        key = cv2.waitKey(1)
        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break
finally:
    pipeline.stop()
    