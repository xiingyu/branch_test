import cv2
import numpy as np
import pyrealsense2 as rs

import matplotlib.pyplot as plt

img_size_x = 1280
img_size_y = 720  
thresh_value = 120
thresh_max = 160
thresh_min = 50
thresh_weight = 1

plt.ion()
fig, ax = plt.subplots()

l_top, r_top = 0, 0

#########################   TOOL BOX  ##########################

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
    
#########################   ########  ##########################


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
    

def warp(img):
    global fig, ax
    img_size = (img.shape[1], img.shape[0])
    
    src = np.float32([[int(img_size_x * 0.2), int(img_size_y * 0.7)],   ##  1 2 
                    [int(img_size_x * 0.8), int(img_size_y * 0.7)],     ## 4   3
                    [int(img_size_x * 0.9), int(img_size_y * 0.9)],     ## (x, y)
                    [int(img_size_x * 0.1), int(img_size_y * 0.9)]
                    ])
    dst = np.float32([[0, 0],
                    [img_size_x, 0],
                    [img_size_x, img_size_y],
                    [0, img_size_y]])
    
    M = cv2.getPerspectiveTransform(src, dst)
    # Minv = cv2.getPerspectiveTransform(dst, src)
    binary_warped = cv2.warpPerspective(img, M, img_size, flags=cv2.INTER_LINEAR)
    
   
    return binary_warped


def get_histogram(binary_warped):
    histogram = np.sum(binary_warped[int(binary_warped.shape[0] / 2):, :], axis=0 )
    # plt.plot(histogram)
    # # plt.imshow(output)
    # # plt.show()
    # plt.pause(0.1)
    # ax.clear()
    return histogram


def slide_window(binary_warped, histogram):
    global l_top, r_top
    
    left_fitx = []
    right_fitx = []
    
    out_img = np.dstack((binary_warped, binary_warped, binary_warped))*255
    midpoint = int(histogram.shape[0]/2)
    
    ###argmax -> 가장 높은value를 가진 자리값 반환
    leftx_base = np.argmax(histogram[:midpoint])
    rightx_base = np.argmax(histogram[midpoint:]) + midpoint
    
    l_top = leftx_base
    r_top = rightx_base
    
    #nwindows :  number of virtical rectangles
    nwindows = 9
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
        pass
    
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
    
    plt.imshow(out_img)
    plt.plot(left_fitx, ploty, color='yellow')
    plt.plot(right_fitx, ploty, color='yellow')
    plt.xlim(0, img_size_x)
    plt.ylim(img_size_y, 0)
    plt.plot(histogram)
    # plt.imshow(output)
    plt.show()
    # plt.pause(0.01)
    ax.clear()
    
    
    
    info = {}
    info['leftx'] = leftx
    info['rightx'] = rightx
    info['left_fitx'] = left_fitx
    info['right_fitx'] = right_fitx
    info['ploty'] = ploty
    
    return ploty, left_fitx, right_fitx, info


def measure_curvature(ploty, lines_info):
    ym_per_pix = 30/720 
    xm_per_pix = 3.7/700 

    leftx = lines_info['left_fitx']
    rightx = lines_info['right_fitx']

    leftx = leftx[::-1]  
    rightx = rightx[::-1]  

    y_eval = np.max(ploty)
    left_fit_cr = np.polyfit(ploty*ym_per_pix, leftx*xm_per_pix, 2)
    right_fit_cr = np.polyfit(ploty*ym_per_pix, rightx*xm_per_pix, 2)
    left_curverad = ((1 + (2*left_fit_cr[0]*y_eval*ym_per_pix + left_fit_cr[1])**2)**1.5) / np.absolute(2*left_fit_cr[0])
    right_curverad = ((1 + (2*right_fit_cr[0]*y_eval*ym_per_pix + right_fit_cr[1])**2)**1.5) / np.absolute(2*right_fit_cr[0])
    # print(left_curverad, 'm', right_curverad, 'm')
    
    return left_curverad, right_curverad


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
        
        combined = apply_thresholds(image) #threshold
        s_binary = apply_color_threshold(image)
        combined_binary = combine_threshold(s_binary, combined)
        warped_color = warp(image)
        binary_warped = warp(combined_binary)
        
        ###
        
        histogram = get_histogram(binary_warped)        
        ploty, left_fitx, right_fitx, infos = slide_window(binary_warped, histogram)        
        left_curverad, right_curverad = measure_curvature(ploty, infos)
        
        print(f'left : {left_curverad} right : {right_curverad}')
        
        
        cv2.polylines(image, [np.array([[int(img_size_x * 0.2), int(img_size_y * 0.7)],   ##  1 2 
                    [int(img_size_x * 0.8), int(img_size_y * 0.7)],     ## 4   3
                    [int(img_size_x * 0.9), int(img_size_y * 0.9)],     ## (x, y)
                    [int(img_size_x * 0.1), int(img_size_y * 0.9)]
                    ])], True, (0,255,0), 2)
        
        origin_left_x = np.uint32((0.1 * img_size_x) + (0.8 * img_size_x) * (left_fitx[-1] / img_size_x))
        origin_right_x = np.uint32((0.1 * img_size_x) + (0.8 * img_size_x) * (right_fitx[-1] / img_size_x))
        
        cv2.circle(image, (origin_left_x,int(img_size_y * 0.9)),5, (255,0,0), -1, cv2.LINE_AA)
        cv2.circle(image, (origin_right_x,int(img_size_y * 0.9)),5, (255,0,0), -1, cv2.LINE_AA)
        
        
        warped_color[np.uint32(ploty), np.uint32(left_fitx)] = [0,255,0]
        warped_color[np.uint32(ploty), np.uint32(right_fitx)] = [0,255,0]
            
        # cv2.imshow("warped", warped_color)
        cv2.imshow("origin_img", image)
        cv2.imshow('result images', binary_warped)
    
        
        key = cv2.waitKey(1)
        if key == ord('q') :
            break
    cv2.destroyAllWindows()

if __name__ == "__main__" :
    main()