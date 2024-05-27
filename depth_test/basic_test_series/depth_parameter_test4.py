import cv2
import numpy as np
import pyrealsense2 as rs
import math



################### const parameter init ####################
img_size_x = 640
img_size_y = 480

thresh_value = 120
thresh_max = 160
thresh_min = 50
thresh_weight = 1   

HFOV = 69   #degree
VFOV = 42
DFOV = 77
focal_length = 1.93 #mm
pixel_size_color = 0.0014 #mm
pixel_size_depth = 0.003 #mm

x_d_value = ( img_size_x / 2 ) / math.tan(HFOV/2/180 * np.pi)
y_d_value = ( img_size_y / 2 ) / math.tan(VFOV/2/180 * np.pi)

color_format = rs.format.bgr8
depth_format = rs.format.z16

###########################################################
################# setting parameter init ##################

camera_height = 67.5 #mm






###########################################################
##################### depth setting  ######################

    
pipeline = rs.pipeline()
config = rs.config()
context = rs.context()
devices = context.query_devices()

config.enable_stream(rs.stream.color,img_size_x,img_size_y, color_format, 30)

profile = pipeline.start(config)    

color_profile = profile.get_stream(rs.stream.color)
color_intrinsics_object = color_profile.as_video_stream_profile().get_intrinsics()
## [ppx,  ppy,  fx,  fy]
color_intrinsics = {'ppx' : color_intrinsics_object.ppx, 'ppy' : color_intrinsics_object.ppy, 'fx' : color_intrinsics_object.fx, 'fy' : color_intrinsics_object.fy}
print(color_intrinsics)