import cv2
import pyrealsense2 as rs
import numpy as np

img_size_x = 1280
img_size_y = 720

def main() :
    
    pipeline = rs.pipeline()
    config = rs.config()

    config.enable_stream(rs.stream.depth,img_size_x,img_size_y, rs.format.z16, 30)
    config.enable_stream(rs.stream.color,img_size_x,img_size_y, rs.format.bgr8, 30)
    
    profile = pipeline.start(config)    
    
    while True :
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_img = np.asanyarray(color_frame.get_data())
        
        
        
        img = color_img[:,:,2]
        gray = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
        
        
        cv2.imshow('img', img)
        cv2.imshow('gray',gray)
        
        key = cv2.waitKey(1)
        if key == ord('q') :
            break


if __name__ == "__main__" :
    main()