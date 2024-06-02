import cv2
import numpy as np
import pyrealsense2 as rs
import math


################### const parameter init ####################
img_size_x = 640
img_size_y = 480

thresh_value = 120
thresh_max = 160
thresh_min = 50
thresh_weight = 1   

HFOV = 69   #degree
VFOV = 42
DFOV = 77
focal_length = 1.93 #mm
pixel_size_color = 0.0014 #mm
pixel_size_depth = 0.003 #mm

x_d_value = ( img_size_x / 2 ) / math.tan(HFOV/2/180 * np.pi)
y_d_value = ( img_size_y / 2 ) / math.tan(VFOV/2/180 * np.pi)

color_format = rs.format.bgr8
depth_format = rs.format.z16



#################  find good parameters ###################

W_H_ratio = 0.75
height_ratio = 2 # i used 1~4

###########################################################
################# setting parameter init ##################

camera_height = 115 #mm



###########################################################
##################### depth setting  ######################

    
pipeline = rs.pipeline()
config = rs.config()
context = rs.context()
devices = context.query_devices()

config.enable_stream(rs.stream.color,img_size_x,img_size_y, color_format, 30)

profile = pipeline.start(config)    

color_profile = profile.get_stream(rs.stream.color)
color_intrinsics_object = color_profile.as_video_stream_profile().get_intrinsics()
## [ x,  y,  ppx,  ppy,  fx,  fy]
color_intrinsics = {'ppx' : color_intrinsics_object.ppx, 'ppy' : color_intrinsics_object.ppy, 'fx' : color_intrinsics_object.fx, 'fy' : color_intrinsics_object.fy}
print(color_intrinsics['ppy'])

###########################################################
################### pyramid calculate  ####################
pixel_y = (abs(img_size_y*(W_H_ratio) - color_intrinsics['ppy'])) /img_size_y * 1080
D_dist = (camera_height * focal_length) / (pixel_y * pixel_size_color)
d_dist = camera_height / math.tan(VFOV/2 /180 * np.pi)
W_H = 2 * D_dist * math.tan(HFOV/2 / 180 * np.pi)

slant_height_L = math.sqrt(d_dist **2 + camera_height **2)
# h_H = (D_dist * focal_length / ((img_size_y - color_intrinsics['fy'])/img_size_y * 1080 * pixel_size_color))
h_H = D_dist * math.tan(VFOV/2 /180 * np.pi)
slant_height_H = math.sqrt(D_dist **2 + h_H **2)
slant_HFOV = math.atan2((W_H/2) , slant_height_H)

W_L = 2 * slant_height_L * math.tan(slant_HFOV)

print(f'slant_height_L  : {slant_height_L }   slant_height_H: {slant_height_H}')
print(f'D_dist : {D_dist}   d_dist : {d_dist}')
print(f'W_H : {W_H}   W_L : {W_L}')

###########################################################

def pre_treatment_img(origin_img) :
    global thresh_value, thresh_max, thresh_min, thresh_weight
    
    ### color match
    hsv_color = cv2.cvtColor(origin_img, cv2.COLOR_BGR2HSV)
    hsv_lower = np.array([80,40,40])
    hsv_upper = np.array([100,230,230])
    
    hsv_mask = cv2.inRange(hsv_color, hsv_lower, hsv_upper)
    
    hsv_filterd = cv2.bitwise_and(hsv_color, hsv_color, mask=hsv_mask)
    color_filterd = cv2.cvtColor(hsv_filterd, cv2.COLOR_HSV2BGR)
    cv2.imshow("filterd",color_filterd)

    ### hsv or histogram
    ###
    
    gray = cv2.cvtColor(color_filterd, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (0,0),1)
    
    Y, X = gray.shape
    
    
    ###low light improvement
    Flatten_gray = np.array(gray).flatten()
    mean = np.mean(Flatten_gray)
    # print(mean)
    if mean >= 150 : 
        gray = np.clip(gray - 30., 0, 255).astype(np.uint8)
    elif mean >= 100 :
        gray = gray
    elif mean >= 75 :
        gray = np.clip(gray + 15., 0, 255).astype(np.uint8)
    elif mean >= 45 : 
        gray = cv2.medianBlur(gray,3)
        gray = np.clip(gray + 35., 0, 255).astype(np.uint8)
    else :
        gray = cv2.medianBlur(gray,5)
        gray = np.clip(gray + 60., 0, 255).astype(np.uint8)
        
    ### end   ###
    ### slice ###
    sliced_img = gray[int(Y*0.7):int(Y*0.9),int(X*0.1):int(X*0.9)]
    
    
    _, thresh = cv2. threshold(sliced_img, thresh_value, 255, cv2.THRESH_BINARY)
    # athresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    # result = np.hstack((gray,thresh, athresh))
    
    
    ### canny
    canny_img = cv2.Canny(sliced_img, 200, 360)
    
    ###hough
    lines = cv2.HoughLinesP(canny_img, 1, np.pi/360, 50, None, 50, 5)
    # lines = cv2.HoughLines(canny_img, 1, np.pi/180, 25)
    if lines is not None :    
        print(len(lines))
        for line in lines :
            x1, y1, x2, y2 = line[0]
            cv2.line(origin_img, (x1 + int(X*0.1),y1 + int(Y*0.7)), (x2 + int(X*0.1),y2 + int(Y*0.7)), (0,255,0), 3)
            
            # if (thresh_value < thresh_max) and (thresh_weight < 10) :
            #     thresh_value = thresh_value +1
            #     thresh_weight = thresh_weight +1
            # else :
            #     thresh_weight = thresh_weight +1
    # else :
        # if (thresh_value > thresh_min)  and (thresh_weight < 100):
        #     thresh_value = thresh_value - 1
        # else : 
        #     thresh_weight = thresh_weight - 1
    
    # result0 = np.hstack((gray, thresh, canny_img))
    # result1 = origin_img
    
    return thresh, origin_img
        

def warp(img):
    
    
    src = np.float32([[0, 0],   ##  1 2 
                    [int(W_H), 0],     ## 4   3
                    [int(W_H - (W_H-W_L)/2), int(img_size_y * (1-W_H_ratio))*height_ratio],
                    [int((W_H-W_L)/2), int(img_size_y * (1-W_H_ratio))*height_ratio]     ## (x, y)
                    ])
    dst = np.float32([[0, int(img_size_y * W_H_ratio)],
                    [img_size_x, int(img_size_y * W_H_ratio)],
                    [img_size_x, img_size_y],
                    [0, img_size_y]])
    # print(src)
    M = cv2.getPerspectiveTransform(src, dst)
    Minv = cv2.getPerspectiveTransform(dst, src)
    binary_warped = cv2.warpPerspective(img, Minv, (int(W_H), int(img_size_y * (1-W_H_ratio)*height_ratio)), flags=cv2.INTER_LINEAR)
    
   
    return binary_warped
    


def main() :
    while True :
        
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_img = np.asanyarray(color_frame.get_data())
        
        half_img = color_img.copy()
        half_img[:int(img_size_y*W_H_ratio),:] = 0
        
        warped = warp(color_img)
        
        
        # test0, test1 = pre_treatment_img(half_img)
        
        
        
        cv2.rectangle(color_img, (0,int(img_size_y*W_H_ratio)),(img_size_x,int(img_size_y)),(255,0,0), 2)
        # cv2.line(color_img, (0,int(img_size_y/2)),(img_size_x,int(img_size_y/2)),(255,0,0), 2)
        
        
        cv2.imshow('Origin',color_img)
        cv2.imshow('warp', warped)
        # cv2.imshow('Test0', test0)
        # cv2.imshow('Test1', test1)
        
        key = cv2.waitKey(1)
        if key == ord('q') :
            break
    cv2.destroyAllWindows()

if __name__ == "__main__" :
    main()