import cv2
import numpy as np
import pyrealsense2 as rs
import math

import matplotlib.pyplot as plt


img_size_x = 1280
img_size_y = 720   
thresh_value = 120
thresh_max = 160
thresh_min = 50
thresh_weight = 1
camera_HFOV = 69
camera_VFOV = 72


def warp(img):
    img_size = (img.shape[1], img.shape[0])
    
    src = np.float32([[int(img_size_y * math.tan(camera_VFOV/180*math.pi/2)*3/4), 3*img_size_y/4],   ##  1 2 
                    [img_size_x - int(img_size_y * math.tan(camera_VFOV/180*math.pi/2)*3/4), 3*img_size_y/4],     ## 4   3
                    [img_size_x,img_size_y],
                    [0, img_size_y]    ## (x, y)
                    ])
    dst = np.float32([[0, 0],
                    [img_size_x, 0],
                    [img_size_x, img_size_y],
                    [0, img_size_y]])
    
    M = cv2.getPerspectiveTransform(src, dst)
    print(src)
    Minv = cv2.getPerspectiveTransform(dst, src)
    binary_warped = cv2.warpPerspective(img, M, img_size, flags=cv2.INTER_LINEAR)
    
   
    return binary_warped


# def warp(img):
#     global fig, ax
#     img_size = (img.shape[1], img.shape[0])
    
#     src = np.float32([[int(img_size_x * 0.2), int(img_size_y * 0.7)],   ##  1 2 
#                     [int(img_size_x * 0.8), int(img_size_y * 0.7)],     ## 4   3
#                     [int(img_size_x * 0.9), int(img_size_y * 0.9)],     ## (x, y)
#                     [int(img_size_x * 0.1), int(img_size_y * 0.9)]
#                     ])
#     dst = np.float32([[0, 0],
#                     [img_size_x, 0],
#                     [img_size_x, img_size_y],
#                     [0, img_size_y]])
    
#     M = cv2.getPerspectiveTransform(src, dst)
#     # Minv = cv2.getPerspectiveTransform(dst, src)
#     binary_warped = cv2.warpPerspective(img, M, img_size, flags=cv2.INTER_LINEAR)
    
   
#     return binary_warped



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
        
        warped_color = warp(image)
        
        cv2.imshow("origin", image)
        cv2.imshow("warped", warped_color)
        
        key = cv2.waitKey(1)
        if key == ord('q') :
            break
        
    
    cv2.destroyAllWindows()
    
    
    

if __name__ == "__main__" :
    main()