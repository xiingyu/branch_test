import pyrealsense2 as rs
import numpy as np
import cv2
import time
import math

# Parameter initialization
img_size_x = 1280
img_size_y = 720

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, img_size_x, img_size_y, rs.format.z16, 30)
config.enable_stream(rs.stream.color, img_size_x, img_size_y, rs.format.bgr8, 30)

profile = pipeline.start(config)
depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()

clipping_distance_in_meters = 1  # 1 meter
clipping_distance = clipping_distance_in_meters / depth_scale
align_to = rs.stream.color
align = rs.align(align_to)

circles = []

def mouse_callback(event, x, y, flags, param):
    global circles
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(circles) < 2:
            circles.append((x, y))
            print("클릭한 좌표:", (x, y))
    elif event == cv2.EVENT_RBUTTONDOWN:
        if len(circles) > 0:
            circles.pop()

try:
    while True:
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        color_frame = aligned_frames.get_color_frame()
        depth_frame = aligned_frames.get_depth_frame()

        color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())

        if circles:
            for circle in circles:
                cv2.circle(color_image, circle, 5, (0, 0, 255), -1, cv2.LINE_AA)
                depth = depth_frame.get_distance(circle[0], circle[1])
                depth_intrinsics = depth_frame.profile.as_video_stream_profile().intrinsics
                depth_point = rs.rs2_deproject_pixel_to_point(depth_intrinsics, [circle[0], circle[1]], depth)
                print(f"3D coordinates at pixel {circle}: {depth_point}")

        cv2.imshow('color_frame', color_image)
        cv2.setMouseCallback("color_frame", mouse_callback)

        key = cv2.waitKey(1)
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break
finally:
    pipeline.stop()
