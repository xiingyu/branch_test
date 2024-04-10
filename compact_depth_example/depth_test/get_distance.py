import pyrealsense2 as rs
import numpy as np
import cv2
import time
from ultralytics import YOLO

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth,640,480, rs.format.z16, 30)
config.enable_stream(rs.stream.color,640,480, rs.format.bgr8, 30)

profile = pipeline.start(config)

###0.0010000000474974513
###fuxking this scale value means, pixel number per 1m
depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()
# print(profile.get_device().first_depth_sensor().get_depth_scale())


clipping_distance_in_meters = 1 #1 meter
clipping_distance = clipping_distance_in_meters / depth_scale
align_to = rs.stream.color
align = rs.align(align_to)


###yolo setting###
model = YOLO('yolov8n.yaml')
model = YOLO('yolov8n.pt')

try:
    while True:
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)

        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        
        result = model.predict(color_image, classes=[0., 67.], conf= 0.25)
        annotated_img = result[0].plot()

        # Remove background - Set pixels further than clipping_distance to grey
        grey_color = 0
        depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) #depth image is 1 channel, color is 3 channels
        bg_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), grey_color, color_image)

        # Render images:
        #   depth align to color on left
        #   depth on right
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.05), cv2.COLORMAP_JET)
        
        images = np.hstack((bg_removed, depth_colormap))
        
        # cv2.namedWindow('Align Example', cv2.WINDOW_NORMAL)
        cv2.imshow('Align Example', images)
        cv2.imshow('depth_image_3d',depth_image)
        cv2.imshow('yolo',annotated_img)
        # print(depth_image.shape)
        # print(depth_image.dtype)##uint16 data type.
        
        # depth_image_uint8 = (depth_image/256).astype(np.uint8)
        # cv2.imshow('depth_image_uint8',depth_image_uint8)
        # print(depth_image_uint8)
        
        
        # cv2.imshow('align',bg_removed)
        # cv2.imshow('color', depth_colormap)
        
        
        key = cv2.waitKey(1)
        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break
finally:
    pipeline.stop()
    