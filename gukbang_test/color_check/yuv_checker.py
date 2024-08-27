import cv2
import numpy as np
import pyrealsense2 as rs


img_size_x = 848
img_size_y = 480
depth_size_x = 848
depth_size_y = 480

### realsense setting ###

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
hole_filling_filter = rs.hole_filling_filter()\

#########################


lower_bound = np.array((17, 10, 10)) # 너무 많이 인식하면 20으로, 인식을 잘 못 하면 15로 (혹은 16)
upper_bound = np.array((130, 255, 255))
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)) ## 추가된 부분

U_detection_threshold = 140



def yuv_detection(img) :
    y, x, c = img.shape
    
    yuv_img = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    Y_img, U_img, V_img = cv2.split(yuv_img)
    display = np.zeros_like(U_img)
    
    # rescale = np.clip(U_img - V_img, 0, 255).astype(np.uint8)
    ret,U_img_treated = cv2.threshold(U_img, U_detection_threshold, 255, cv2.THRESH_BINARY)
    if ret :
        # filterd = cv2.bitwise_and(img, img, mask=U_img_treated)
        # cv2.imshow("UUUU", filterd)
        
        contours, _ = cv2.findContours(U_img_treated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        max_area = 0
        max_contour = None
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                max_contour = contour

        if max_contour is not None:
            max_contour_mask = np.zeros_like(U_img_treated)
            cv2.drawContours(max_contour_mask, [max_contour], -1, (255, 255, 255), thickness=cv2.FILLED)
            
        
            filterd = cv2.bitwise_and(img, img, mask=max_contour_mask)
            return filterd
            # cv2.imshow("UUUU", filterd)
            # cv2.waitKey(1)
        else :
            print("passed")
            return display
            # cv2.imshow("UUUU", display)
            # cv2.wait
    

def main() :
    
    
    while True :
        
        frames          = pipeline.wait_for_frames()
        aligned_frames  = align.process(frames)
        
        color_frame            = aligned_frames.get_color_frame()
        aligned_depth_frame    = aligned_frames.get_depth_frame()
        filled_depth_frame     = hole_filling_filter.process(aligned_depth_frame)
        
        depth_intrinsics = aligned_depth_frame.profile.as_video_stream_profile().intrinsics
        
        depth_img = np.asanyarray(filled_depth_frame.get_data())
        color_img = np.asanyarray(color_frame.get_data())
        
        
        
        color_blurd = cv2.GaussianBlur(color_img, (5, 5), 0) # 블러 처리. 홀수만 가능.
        color_open = cv2.morphologyEx(color_blurd, cv2.MORPH_OPEN, kernel) ### 추가된 부분
        color_close = cv2.morphologyEx(color_open, cv2.MORPH_CLOSE, kernel) ### 추가된 부분
        
        ######## HSV
        yuv = yuv_detection(color_close)
        
        
        
        
        
        
        cv2.imshow("color", color_img)
        cv2.imshow("color_close", color_close)
        cv2.imshow('yuv', yuv)
        key = cv2.waitKey(1) 
        if key == ord('q') :
            break
    
    cv2.destroyAllWindows
    



if __name__ == "__main__" :
    main()