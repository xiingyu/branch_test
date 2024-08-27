import cv2
import pyrealsense2 as rs
import os
import numpy as np

folder_path = '/home/skh/testing_folder/gukbang_test/depth_learning/images'
img_num = len

def main() :
    
    img_size_x = 1280
    img_size_y = 720
    depth_size_x = 1280
    depth_size_y = 720
    
    pipeline = rs.pipeline()
    config = rs.config()

    config.enable_stream(rs.stream.color, img_size_x,     img_size_y,    rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, depth_size_x,   depth_size_y,  rs.format.z16, 30)
    depth_profile = pipeline.start(config)
    
    depth_sensor = depth_profile.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()
    
    clipping_distance_in_meters = 1 #1 meter
    clipping_distance = clipping_distance_in_meters / depth_scale
    
    align_to = rs.stream.color
    align = rs.align(align_to)
    
    num = len(os.listdir(folder_path))
    print(f'{num} of images detected.')
    
    while True :
        frames          = pipeline.wait_for_frames()
        aligned_frames  = align.process(frames)
        
        color_frame                 = aligned_frames.get_color_frame()
        aligned_depth_frame    = aligned_frames.get_depth_frame()
        depth_intrinsics = aligned_depth_frame.profile.as_video_stream_profile().intrinsics
        
        depth_img = np.asanyarray(aligned_depth_frame.get_data())
        color_img = np.asanyarray(color_frame.get_data())
        cv2.imshow("realtime", color_img)
        key = cv2.waitKey(1)
        
        if key == ord('q') :
            break
        elif key == ord('s') :
            cv2.imwrite(f'/home/skh/testing_folder/gukbang_test/depth_learning/images/img{num+1}.png', img)
            num = num+1
            print(f'saved as img{num}.png !!')
    
    cv2.destroyAllWindows
    
if __name__ == "__main__" :
    main()
        