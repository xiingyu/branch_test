import cv2
import numpy as np
import pyrealsense2 as rs

import matplotlib.pyplot as plt


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
        image = np.asanyarray(color_frame.get_data())
        
        yuv_image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
        print(f'shape : {yuv_image.shape}')
        
        Y_img, U_img, V_img = cv2.split(yuv_image)
        
        Y_img = np.clip(Y_img* 1.5, 0 ,255).astype(np.uint8)
        up_scale = cv2.merge([Y_img,U_img,V_img])
        
        
        cv2.imshow("origin_img", image)
        cv2.imshow("yuv", yuv_image)
        cv2.imshow("bright", up_scale)
        # cv2.imshow("Y", Y_img)
        # cv2.imshow("U", U_img)
        # cv2.imshow("V", V_img)
        
        
        key = cv2.waitKey(1)
        if key == ord('q') :
            break
    cv2.destroyAllWindows()

if __name__ == "__main__" :
    main()