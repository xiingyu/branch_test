import cv2
import numpy as np
import pyrealsense2 as rs
import math
import matplotlib.pyplot as plt


################### const parameter init ####################
img_size_x = 1280
img_size_y = 720

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

W_H_ratio = 0.7
warped_remain_ratio = 0.7
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
    # cv2.imshow("filterd",color_filterd)

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
    l_lines = cv2.HoughLinesP(canny_img, 1, np.pi/360, 50, None, 50, 5)
    # l_lines = cv2.HoughLines(canny_img, 1, np.pi/180, 25)
    if l_lines is not None :    
        print(len(l_lines))
        for line in l_lines :
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
    binary_warped = cv2.warpPerspective(img, Minv, (int(W_H), int(img_size_y * (1-W_H_ratio)*height_ratio)), flags=cv2.INTER_LINEAR)####이게 필요해 !
    
   
    return binary_warped

def warp_inv(img):
    
    
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
    binary_warped = cv2.warpPerspective(img, M, (int(W_H), int(img_size_y * (1-W_H_ratio)*height_ratio)), flags=cv2.INTER_LINEAR)####이게 필요해 !
    
   
    return binary_warped

################################# pre processing
################################# color detection

def color_detection(image, lower=[16,20,20],upper=[35,255,255]) :
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    hsv_lower = np.array(lower)
    hsv_upper = np.array(upper)
    
    hsv_mask = cv2.inRange(hsv_image, hsv_lower, hsv_upper)
    
    hsv_filterd = cv2.bitwise_and(hsv_image, hsv_image, mask=hsv_mask)
    
    color_filterd = cv2.cvtColor(hsv_filterd, cv2.COLOR_HSV2BGR)

    return color_filterd



def abs_sobel_thresh(image, orient='x', sobel_kernel=3, thresh=(0, 255)):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0) if orient == 'x' else np.zeros_like(gray)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1) if orient == 'y' else np.zeros_like(gray)
    abs_sobel = np.sqrt(sobelx**2 + sobely**2)
    scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel))
    grad_binary = np.zeros_like(scaled_sobel)
    grad_binary[(scaled_sobel >= thresh[0]) & (scaled_sobel <= thresh[1])] = 255
    return grad_binary

def mag_thresh(image, sobel_kernel=3, mag_thresh=(0, 255)):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    abs_sobel = np.sqrt(sobelx**2 + sobely**2)
    scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel)) 
    mag_binary = np.zeros_like(scaled_sobel)
    mag_binary[(scaled_sobel >= mag_thresh[0]) & (scaled_sobel <= mag_thresh[1])] = 255

    return mag_binary

def dir_threshold(image, sobel_kernel=3, thresh=(0, np.pi/2)):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    abs_sobelx = np.absolute(sobelx)
    abs_sobely = np.absolute(sobely)
    grad_dir = np.arctan2(abs_sobely, abs_sobelx)
    dir_binary = np.zeros_like(grad_dir)

def apply_thresholds(image, ksize=3):
    gradx = abs_sobel_thresh(image, orient='x', sobel_kernel=ksize, thresh=(20, 100))
    grady = abs_sobel_thresh(image, orient='y', sobel_kernel=ksize, thresh=(20, 100))
    mag_binary = mag_thresh(image, sobel_kernel=ksize, mag_thresh=(30, 100))
    dir_binary = dir_threshold(image, sobel_kernel=ksize, thresh=(0.7, 1.3))

    combined = np.zeros_like(gradx)
    combined[((gradx == 255) & (grady == 255)) | ((mag_binary == 255) & (dir_binary == 255))] = 255
    
    return combined


def apply_color_threshold(image):
    hls = cv2.cvtColor(image, cv2.COLOR_RGB2HLS)
    s_channel = hls[:,:,2]
    s_thresh_min = 170
    s_thresh_max = 255
    s_binary = np.zeros_like(s_channel)
    s_binary[(s_channel >= s_thresh_min) & (s_channel <= s_thresh_max)] = 255

    return s_binary
    

def combine_threshold(s_binary, combined):
    combined_binary = np.zeros_like(combined)
    combined_binary[(s_binary == 255) | (combined == 255)] = 255

    return combined_binary


################################### histogram
plt.ion()
fig, ax = plt.subplots()

def get_histogram(image):
    # histogram = np.sum(image, axis=0).sum(axis=1)
    histogram = np.sum(image, axis=0)
    # ax.clear()
    # ax.plot(histogram)
    # ax.set_title("Vertical Sum Histogram")
    # plt.draw()
    # plt.pause(0.001)
    return histogram


def color_filter(color_img) :
    hsv = cv2.cvtColor(color_img, cv2.COLOR_BGR2HSV)
    
    lower = (15,20,20)
    upper = (30,255,255)
    
    

################################### hough

def find_lines(binary_warped) :
    # print(image.shape[1]/2)
    # dilated = cv2.dilate(binary_warped, (5,5), iterations=2)
    # l_image = dilated[:,:int(dilated.shape[1]/2)]
    # r_image = dilated[:,int(dilated.shape[1]/2):]
    
    # cv2.imshow("l", l_image)
    # cv2.imshow("r", r_image)
    
    # l_histo = get_histogram(l_image)
    # r_histo = get_histogram(r_image)
    
    ########## 아래는 hough라는 망측한 아이를 사용하는 코드
    # l_lines = cv2.HoughLinesP(l_image, 20, np.pi/180. , 160, minLineLength=150, maxLineGap=20)
    # r_lines = cv2.HoughLinesP(r_image, 20, np.pi/180. , 160, minLineLength=150, maxLineGap=20)
    
    # if l_lines is not None :
    #     for i in range(l_lines.shape[0]) :
    #         lpt1 = (l_lines[i][0][0], l_lines[i][0][1]) # 시작점 좌표 x,y
    #         lpt2 = (l_lines[i][0][2], l_lines[i][0][3]) # 끝점 좌표, 가운데는 무조건 0
    #         cv2.line(warped_color, lpt1, lpt2, (0, 0, 255), 2, cv2.LINE_AA)
    
    # if r_lines is not None :
    #     for i in range(r_lines.shape[0]) :
    #         rpt1 = (r_lines[i][0][0]+int(dilated.shape[1]/2), r_lines[i][0][1]) # 시작점 좌표 x,y
    #         rpt2 = (r_lines[i][0][2]+int(dilated.shape[1]/2), r_lines[i][0][3]) # 끝점 좌표, 가운데는 무조건 0
    #         cv2.line(warped_color, rpt1, rpt2, (0, 0, 255), 2, cv2.LINE_AA)
            
    # cv2.imshow("hough", warped_color)
    #############망측한 hough는 여기까지
    
    histo = get_histogram(binary_warped)
    
    out_img = np.dstack((binary_warped, binary_warped, binary_warped))*255
    
    midpoint = int(img_size_x/2)
    leftx_base = np.argmax(histo[:midpoint])
    rightx_base = np.argmax(histo[midpoint:]) + midpoint
    
    
    nwindows = 4
    window_height = int(binary_warped.shape[0]/nwindows)
    nonzero = binary_warped.nonzero()
    nonzeroy = np.array(nonzero[0]) #row coordinate
    nonzerox = np.array(nonzero[1]) #col coordinate
    
    
    leftx_current = leftx_base
    rightx_current = rightx_base
    margin = int(img_size_x * 0.09)
    minpix = 50
    left_lane_inds = []
    right_lane_inds = []

    
    for window in range(nwindows):
        win_y_low = binary_warped.shape[0] - (window+1)*window_height   #from bottom to top
        win_y_high = binary_warped.shape[0] - window*window_height      ##low is top. high is bottom
        
        win_xleft_low = leftx_current - margin
        win_xleft_high = leftx_current + margin
        win_xright_low = rightx_current - margin
        win_xright_high = rightx_current + margin
        
        cv2.rectangle(out_img,(win_xleft_low,win_y_low),(win_xleft_high,win_y_high), (0,255,0), 2) 
        cv2.rectangle(out_img,(win_xright_low,win_y_low),(win_xright_high,win_y_high), (0,255,0), 2) 
        good_left_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xleft_low) &  (nonzerox < win_xleft_high)).nonzero()[0]
        good_right_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xright_low) &  (nonzerox < win_xright_high)).nonzero()[0]
        ### good data is true/false. but, use nonzero, counting "Ture"
                
        left_lane_inds.append(good_left_inds)
        right_lane_inds.append(good_right_inds)
        if len(good_left_inds) > minpix:
            leftx_current = int(np.mean(nonzerox[good_left_inds]))
        if len(good_right_inds) > minpix:        
            rightx_current = int(np.mean(nonzerox[good_right_inds]))

    left_lane_inds = np.concatenate(left_lane_inds)
    right_lane_inds = np.concatenate(right_lane_inds)

    leftx = nonzerox[left_lane_inds]
    lefty = nonzeroy[left_lane_inds] 
    rightx = nonzerox[right_lane_inds]
    righty = nonzeroy[right_lane_inds] 
    
    try:
        left_fit = np.polyfit(lefty, leftx, 2)
        right_fit = np.polyfit(righty, rightx, 2)
    except TypeError as e:
        print("TypeError:", e)
        
        info = {}
        info['leftx'] = 0
        info['rightx'] = 0
        info['left_fitx'] = 0
        info['right_fitx'] = 0
        info['ploty'] = 0

        return info
    
    ## 채우기 같은거
    ploty = np.linspace(0, binary_warped.shape[0]-1, binary_warped.shape[0] )       # height
    
    ##### yellow line #####
    left_fitx = left_fit[0]*ploty**2 + left_fit[1]*ploty + left_fit[2]
    right_fitx = right_fit[0]*ploty**2 + right_fit[1]*ploty + right_fit[2]
    out_img[np.uint32(ploty), np.uint32(left_fitx)] = [0,255,0]
    out_img[np.uint32(ploty), np.uint32(right_fitx)] = [0,255,0]
    
    # print(np.uint32(ploty))
    # print(np.uint32(left_fitx))
    
    # print(ploty)
    # print(left_fitx)
    #######################

    
    ##### red and blue line #####
    out_img[nonzeroy[left_lane_inds], nonzerox[left_lane_inds]] = [255, 0, 0]
    out_img[nonzeroy[right_lane_inds], nonzerox[right_lane_inds]] = [0, 0, 255]
    #############################
    
    # plt.imshow(out_img)
    # plt.plot(left_fitx, ploty, color='yellow')
    # plt.plot(right_fitx, ploty, color='yellow')
    # plt.xlim(0, img_size_x)
    # plt.ylim(img_size_y, 0)
    # plt.plot(histogram)
    # plt.imshow(output)
    # plt.show()
    # plt.pause(0.01)
    # ax.clear()
    
    
    ax.clear()
    
    ax.plot(histo)
    ax.set_title("Vertical Sum Histogram")
    plt.draw()
    plt.pause(0.001)
    
    
    info = {}
    info['leftx'] = leftx
    info['rightx'] = rightx
    info['left_fitx'] = left_fitx
    info['right_fitx'] = right_fitx
    info['ploty'] = ploty
    
    return info


#################################### histogram

def main() :
    while True :
        
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_img = np.asanyarray(color_frame.get_data())
        
        split_img = color_img.copy()
        split_img[:int(img_size_y*W_H_ratio),:] = 0
        
        warped_color = warp(split_img)
        
        
        ###find l_lines from warped
        combined = apply_thresholds(color_img) #threshold
        s_binary = apply_color_threshold(split_img)
        combined_binary = combine_threshold(s_binary, combined)
        warped_split_img = warp(combined_binary)
        
        cannied = cv2.Canny(warped_split_img, 300,400)
        cv2.imshow("combined_binary", warped_split_img)
        
        line_window = warped_split_img[:int(warped_split_img.shape[0]*warped_remain_ratio),:]
        infos = find_lines(line_window)   

        l_fitx = infos["left_fitx"]
        r_fitx = infos["right_fitx"]
        
        origin_l_x = int(l_fitx[-1])
        origin_r_x = int(r_fitx[-1])
        
        print(origin_l_x)
        print(origin_r_x)
        cv2.circle(color_img, (int(origin_l_x/(l_fitx.shape[0]) * img_size_x), int(img_size_y * W_H_ratio + ((img_size_y - img_size_y * W_H_ratio) * warped_remain_ratio))), 5, (255,0,0), -1, cv2.LINE_AA)
        cv2.circle(color_img, (int(origin_r_x/(r_fitx.shape[0]) * img_size_x), int(img_size_y * W_H_ratio + ((img_size_y - img_size_y * W_H_ratio) * warped_remain_ratio))), 5, (255,0,0), -1, cv2.LINE_AA)
        # print(l_fitx[-1])
        cv2.rectangle(color_img, (0, int(img_size_y * W_H_ratio)), (int(img_size_x), int(img_size_y * W_H_ratio)), (255,0,0), 2)
        cv2.rectangle(color_img, (0, int(img_size_y * W_H_ratio)), (int(img_size_x), int(img_size_y * W_H_ratio + ((img_size_y - img_size_y * W_H_ratio) * warped_remain_ratio))), (255,0,0), 2)
        
        cv2.imshow('line_window', line_window)
        cv2.imshow('Origin', color_img)
        cv2.imshow('warp', warped_color)
        
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    cv2.destroyAllWindows()

if __name__ == "__main__" :
    main()