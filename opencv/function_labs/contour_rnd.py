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
        # get_histogram(image)
        
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        binary = cv2.bitwise_not(binary)

        contours, hierarchy = cv2.findContours(binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

        for i in range(len(contours)):
            cv2.drawContours(image, [contours[i]], 0, (0, 0, 255), 2)
            cv2.putText(image, str(i), tuple(contours[i][0][0]), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 1)
            print(i, hierarchy[0][i])
            cv2.imshow("image", image)
            
        
    
        
        key = cv2.waitKey(1)
        if key == ord('q') :
            break
    cv2.destroyAllWindows()

if __name__ == "__main__" :
    main()