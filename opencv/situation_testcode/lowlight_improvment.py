import cv2
import pyrealsense2 as rs
import numpy as np

"""
###low light improvement
Flatten_gray = np.array(gray).flatten()
mean = np.mean(Flatten_gray)

if mean >= 100 : 
    gray = gray
elif mean >= 75 :
    gray = np.clip(gray + 15., 0, 255).astype(np.uint8)
elif mean >= 45 : 
    gray = cv2.medianBlur(gray,3)
    gray = np.clip(gray + 35., 0, 255).astype(np.uint8)
else :
    gray = cv2.medianBlur(gray,5)
    gray = np.clip(gray + 60., 0, 255).astype(np.uint8)
"""

def improve_light(img) :
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    Flatten_gray = np.array(gray).flatten()
    mean = np.mean(Flatten_gray)

    if mean >= 100 : 
        upscale = img
        pass
        
    elif mean >= 80 :
        median_img = cv2.medianBlur(img,5)
        upscale = np.clip(median_img + 15., 0, 255).astype(np.uint8)
    elif mean >= 60 : 
        median_img = cv2.medianBlur(img,5)
        upscale = np.clip(median_img + 30., 0, 255).astype(np.uint8)
    else :
        median_img = cv2.medianBlur(img,7)
        upscale = np.clip(median_img + 45., 0, 255).astype(np.uint8)
    
    # median_img = cv2.medianBlur(img,5)
    # upscale = np.clip(median_img + 60., 0, 255).astype(np.uint8)
    # contrast = np.clip(upscale+(upscale - 128)*0.1, 0, 255).astype(np.uint8)
    print(mean)
    
    return upscale


def improve_color(img) :
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    saturation_param = 1.5
    hsv_img[:,:,1] = np.clip(hsv_img[:,:,1] * saturation_param ,0,255).astype(np.uint8)
    
    result = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)
    
    return result
    
    



def main() :
    pipeline = rs.pipeline()
    config = rs.config()

    config.enable_stream(rs.stream.color, 1280, 720,rs.format.bgr8, 30)
    pipeline.start(config)
    
    while True :
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        
        color_image = np.asanyarray(color_frame.get_data())
        
        # upscale = improve_light(color_image)
        
        median_img = cv2.medianBlur(color_image,3)
        upscale = np.clip(median_img + 40., 0, 255).astype(np.uint8)
        
        improved_color = improve_color(upscale)
        
        
        cv2.imshow("origin", color_image)
        cv2.imshow("upscale", upscale)
        cv2.imshow("improve_color",improved_color)
        # cv2.imshow("contrast", contrast)
        
        key = cv2.waitKey(1)
        if (key == ord('q')) or (key == 27) :
            break
        
    cv2.destroyAllWindows()

        

if __name__ == "__main__" :
    main()
