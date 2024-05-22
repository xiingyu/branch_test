import pyrealsense2 as rs
import numpy as np
import cv2
import time

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth, rs.format.z16, 30)
config.enable_stream(rs.stream.color, rs.format.bgr8, 30)

profile = pipeline.start(config)

###0.0010000000474974513
###fuxking this scale value means, pixel number per 1m
depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()


clipping_distance_in_meters = 1 #1 meter
clipping_distance = clipping_distance_in_meters / depth_scale


try:
    while True:
        
        start_time = time.time()
        frame = pipeline.wait_for_frames()
        color_frame = frame.get_color_frame()
        depth_frame = frame.get_depth_frame()


        color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())
        
        
        
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.05), cv2.COLORMAP_JET)
        
        
        cv2.imshow("color", color_image)
        cv2.imshow("depth", depth_image)
        cv2.imshow("depth_map", depth_colormap)
        
        print(depth_image.shape)
        
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break
finally:
    pipeline.stop()
    