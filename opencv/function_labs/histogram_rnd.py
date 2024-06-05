import cv2
import numpy as np
import pyrealsense2 as rs

import matplotlib.pyplot as plt

img_size_x = 640
img_size_y = 480   
thresh_value = 120
thresh_max = 160
thresh_min = 50
thresh_weight = 1

plt.ion()
fig, ax = plt.subplots()



def get_histogram(image):
    histogram = np.sum(image, axis=0).sum(axis=1)
    ax.clear()
    ax.plot(histogram)
    ax.set_title("Vertical Sum Histogram")
    plt.draw()
    plt.pause(0.001)
    return histogram



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
        get_histogram(image)
        
    
        
        key = cv2.waitKey(1)
        if key == ord('q') :
            break
    cv2.destroyAllWindows()

if __name__ == "__main__" :
    main()