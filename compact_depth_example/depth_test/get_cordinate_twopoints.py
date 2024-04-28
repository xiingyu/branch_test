import pyrealsense2 as rs
import numpy as np
import cv2
import time
import math

### parameter init
img_size_x = 1280
img_size_y = 720
x_d_value = ( img_size_x / 2 ) / math.tan(34.5/180 * np.pi)
y_d_value = ( img_size_y / 2 ) / math.tan(21/180 * np.pi)

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth,img_size_x,img_size_y, rs.format.z16, 30)
config.enable_stream(rs.stream.color,img_size_x,img_size_y, rs.format.bgr8, 30)

profile = pipeline.start(config)

###0.0010000000474974513
###fuxking this scale value means, pixel number per 1m
depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()
# print(profile.get_device().first_depth_sensor().get_depth_scale())

clipping_distance_in_meters = 1 #1 meter
clipping_distance = clipping_distance_in_meters / depth_scale
align_to = rs.stream.color
align = rs.align(align_to)



cam_num = 0
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
        
        start_time = time.time()
        frames = pipeline.wait_for_frames()
        
        aligned_frames = align.process(frames)
        
        color_frame = frames.get_color_frame()
        color_img = np.asanyarray(color_frame.get_data())

        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        # ret, img = color_image.read()

        # Remove background - Set pixels further than clipping_distance to grey
        # depth_image  is 480 by 640 scale.
        grey_color = 0
        depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) #depth image is 1 channel, color is 3 channels
        bg_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), grey_color, color_image)
        
        #640 by 360   xy
        color_img = cv2.circle(color_img,(int(img_size_x/2),int(img_size_y/2)),5,(0,0,255), -1, cv2.LINE_AA)
        
        # print(f'distance between cam and object is {depth_image[object_xy[1]][object_xy[0]]}')
        # print(f'distance between cam and object is {distance:.4f} meters')
            
            
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.05), cv2.COLORMAP_JET)
        
        images = np.hstack((bg_removed, depth_colormap))
        
        
        end_time = time.time()
        during_time = end_time - start_time
        # print(during_time, f'{1/during_time} frames')
        # print(depth_image.shape) ### 480 by 640
        
        
        center_distance = depth_image[int(img_size_y/2)][int(img_size_x/2)] * depth_scale        
        cv2.putText(color_img, f'{center_distance:.4f} m', (30,30), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,255),2)
        
        if circles : ##maybe xy
            if len(circles) == 2 :
                for circle in circles:
                    color_img = cv2.circle(color_img, circle, 5,(0, 0, 255), -1, cv2.LINE_AA)
                first_distance = depth_image[circles[0][1]][circles[0][0]] * depth_scale
                second_distance = depth_image[circles[1][1]][circles[1][0]] * depth_scale
                
                if not (first_distance <= 0) or (second_distance <= 0) :
                    first_cordinate_x = abs(img_size_x/2 - circles[0][0]) * first_distance *(1 if circles[0][0] >= img_size_x/2 else -1) / x_d_value
                    first_cordinate_y = abs(img_size_y/2 - circles[0][1]) * first_distance * (1 if circles[0][1] >= img_size_y/2 else -1)/ y_d_value
                    second_cordinate_x = abs(img_size_x/2 - circles[1][0]) * first_distance *(1 if circles[1][0] >= img_size_x/2 else -1) / x_d_value
                    second_cordinate_y = abs(img_size_y/2 - circles[1][1]) * first_distance * (1 if circles[1][1] >= img_size_y/2 else -1)/ y_d_value
                
                    cv2.putText(color_img, f'{first_distance:.4f} m, {circles[0][0]} by {circles[0][1]} logical : {first_cordinate_x:.4f} {first_cordinate_y:.4f}', (30,60), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,255),2)
                    cv2.putText(color_img, f'{second_distance:.4f} m {circles[1][0]} by {circles[1][1]} logical : {second_cordinate_x:.4f} {second_cordinate_y:.4f}', (30,90), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,255),2)
                    
            elif len(circles) == 1 :
                for circle in circles:
                    color_img = cv2.circle(color_img, circle, 5,(0, 0, 255), -1, cv2.LINE_AA) 
                first_distance = depth_image[circles[0][1]][circles[0][0]] * depth_scale
                cv2.putText(color_img, f'{first_distance:.4f} m, {circles[0][0]} by {circles[0][1]}', (30,60), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,255),2)    
        
                
                
        # cv2.namedWindow('Align Example', cv2.WINDOW_NORMAL)
        cv2.imshow('Align Example', images)
        cv2.imshow('color_frame',color_img)
        cv2.setMouseCallback("color_frame", mouse_callback)
        
        key = cv2.waitKey(1)
        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break
finally:
    pipeline.stop()
    