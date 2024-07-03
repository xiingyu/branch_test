import cv2
import numpy as np

import matplotlib.pyplot as plt

plt.ion()
fig, ax = plt.subplots()

###################################
# ideas...
# two roi set. -> track roi, mission roi.
# finite state machine by mission roi.
##################################


########### parameters ###########

cam_num = 4
U_detection_threshold = 140 ## 0~255
img_size_x = 1280
img_size_y = 720
ROI_ratio = 0.2

#################################

def hsv_detection(img, lower=(110,50,50), upper=(130,255,255)) :
    gaussian = cv2.GaussianBlur(img, (0, 0), 1)
    hsv_img = cv2.cvtColor(gaussian, cv2.COLOR_BGR2HSV)
    
    hsv_lower = np.array(lower)
    hsv_upper = np.array(upper)
    
    hsv_mask = cv2.inRange(hsv_img, hsv_lower, hsv_upper)
    
    filterd = cv2.bitwise_and(hsv_img, hsv_img, mask=hsv_mask)
    filterd_img = cv2.cvtColor(filterd, cv2.COLOR_HSV2BGR)
    
    return filterd_img

def yuv_detection(img) :
    gaussian = cv2.GaussianBlur(img, (3, 3), 1)
    yuv_img = cv2.cvtColor(gaussian, cv2.COLOR_BGR2YUV)
    Y_img, U_img, V_img = cv2.split(yuv_img)
    
    # rescale = np.clip(U_img - V_img, 0, 255).astype(np.uint8)
    ret,U_img_treated = cv2.threshold(U_img, U_detection_threshold, 255, cv2.THRESH_BINARY)
    histogram = get_histo(U_img_treated)
    L_end, R_end = end_point_finder(U_img_treated,histogram)
    if ret :
        filterd = cv2.bitwise_and(img, img, mask=U_img_treated)
        cv2.imshow("UUUU", filterd)
        
        
    
def get_histo(image) :
    histogram = np.sum(image, axis=0 )
    plt.plot(histogram)
    # plt.imshow(output)
    plt.show()
    plt.pause(0.1)
    ax.clear()
    return histogram

def end_point_finder(binary_image,histogram) :
    y,x = binary_image.shape
    midpoint = int(x/2)
    
    L_histo = histogram[:midpoint]
    R_histo = histogram[midpoint:]
    
    L_end = np.argmax(L_histo)
    R_end = img_size_x - np.argmax(R_histo[::-1])
    # print(L_end, R_end)
    print(f'L-diff {midpoint - L_end}   / R-diff{R_end - midpoint}')
    return L_end, R_end
    


def main() :
    global cam_num
    
    cap = cv2.VideoCapture(cam_num)
    
    print(f'set resolution width {img_size_x} height {img_size_y}')
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, img_size_x)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, img_size_y)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f'changed resolution width {width} height {height}')
    
    while True :
        ret, image = cap.read()
        
        if not ret :
            print("fail")
            break
            
        else :
            ######## ROI ########
            ROI = image[int(img_size_y * (1-ROI_ratio)):,:].copy()
            cv2.rectangle(image,(0,int(img_size_y * (1-ROI_ratio))),(img_size_x, img_size_y),(255,0,0),2)
            
            
            ########     ########
            
            yuv_detection(ROI)
            hsv = hsv_detection(image)
            
            cv2.imshow("hsv", hsv)
            
            
            # Y_img = np.clip(Y_img* 1.5, 0 ,255).astype(np.uint8)
            # up_scale = cv2.merge([Y_img,U_img,V_img])
            
            
            cv2.imshow("origin_img", image)
            
            
            key = cv2.waitKey(1)
            if key == ord('q') :
                break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__" :
    main()