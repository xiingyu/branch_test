import cv2
import numpy as np
import pyrealsense2 as rs
import os

img_size_x = 640
img_size_y = 480

path = '/home/skh/testing_folder/trash_sort/image_folder/images/'

def main() :
    
    # pipeline = rs.pipeline()
    # config = rs.config()

    # config.enable_stream(rs.stream.color,img_size_x,img_size_y, rs.format.bgr8, 30)
    
    # profile = pipeline.start(config)    
    
    cap = cv2.VideoCapture(4)
    
    while True :
        ret, image= cap.read()
        # frames = pipeline.wait_for_frames()
        # color_frame = frames.get_color_frame()
        if not ret :
            print("connection fail")
        else :
        
            # image = np.asanyarray(color_frame.get_data())
            
            cv2.imshow("Title", image)
            
            
            files = os.listdir(path)
            # counts = 0
            counts = sum(1 for file in files if 'img' in file)
            
            key = cv2.waitKey(1)
            if key == ord('q') :
                break
            elif key == ord('s') :
                cv2.imwrite(f'{path}img{counts+1}.png', image)
                print(f"image saved! {counts+1}")
            
    cv2.destroyAllWindows()
        

if __name__ == "__main__" :
    main()