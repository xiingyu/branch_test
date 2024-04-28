import cv2
import pyrealsense2 as rs
import numpy as np


def main() :
    pipeline = rs.pipeline()
    config = rs.config()

    config.enable_stream(rs.stream.depth, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, rs.format.bgr8, 30)
    pipeline.start(config)
    
    while True :
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue
        
        
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        
        # print(depth_image.shape)
        # print(color_image.shape)
        # print("--------------------")
        
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        
        cv2.imshow("depth_image", depth_image)
        cv2.imshow("color_image", color_image)
        # cv2.imshow("depth_colormap", depth_colormap)
        
        key = cv2.waitKey(1)
        if (key == ord('q')) or (key == 27) :
            break
        
    cv2.destroyAllWindows()

        

if __name__ == "__main__" :
    main()
