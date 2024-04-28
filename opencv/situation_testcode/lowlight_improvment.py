import cv2
import pyrealsense2 as rs
import numpy as np


def main() :
    pipeline = rs.pipeline()
    config = rs.config()

    config.enable_stream(rs.stream.color, 1280, 720,rs.format.bgr8, 30)
    pipeline.start(config)
    
    while True :
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        
        color_image = np.asanyarray(color_frame.get_data())
        
        ##opencv 시작
        median_img = cv2.medianBlur(color_image,5)
        upscale = np.clip(median_img + 60., 0, 255).astype(np.uint8)
        # contrast = np.clip(upscale+(upscale - 128)*0.1, 0, 255).astype(np.uint8)
        
        
        cv2.imshow("origin", color_image)
        cv2.imshow("median", median_img)
        cv2.imshow("upscale", upscale)
        # cv2.imshow("contrast", contrast)
        
        key = cv2.waitKey(1)
        if (key == ord('q')) or (key == 27) :
            break
        
    cv2.destroyAllWindows()

        

if __name__ == "__main__" :
    main()
