import cv2
import numpy as np
import pyrealsense2 as rs
import math
import time

import matplotlib.pyplot as plt

img_size_x = 1280
img_size_y = 720   
thresh_value = 120
thresh_max = 160
thresh_min = 50
thresh_weight = 1


    
plt.ion()
fig, ax = plt.subplots()


class Line:
    def __init__(self):
        # was the line detected in the last iteration?
        self.detected = False
        # Set the width of the windows +/- margin
        self.window_margin = 56
        # x values of the fitted line over the last n iterations
        self.prevx = []
        # polynomial coefficients for the most recent fit
        self.current_fit = [np.array([False])]
        #radius of curvature of the line in some units
        self.radius_of_curvature = None
        # starting x_value
        self.startx = None
        # ending x_value
        self.endx = None
        # x values for detected line pixels
        self.allx = None
        # y values for detected line pixels
        self.ally = None
        # road information
        self.road_inf = None
        self.curvature = None
        self.deviation = None


def prescaler(img) :
    abs_sobel = np.absolute(cv2.Sobel(img, cv2.CV_64F, 1, 0))
    scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel))
    sobel_x = np.zeros_like(scaled_sobel)

    th_sobelx = (15, 150)
    sobel_x[(scaled_sobel >= th_sobelx[0]) & (scaled_sobel <= th_sobelx[1])] = 255
    
    abs_sobel = np.absolute(cv2.Sobel(img, cv2.CV_64F, 0, 1))
    th_sobely = (25, 200)
    scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel))
    sobel_y = np.zeros_like(scaled_sobel)
    sobel_y[(scaled_sobel >= th_sobely[0]) & (scaled_sobel <= th_sobely[1])] = 255
    
    sobel_x = cv2.erode(sobel_x, (5,5), iterations=1)
    sobel_y = cv2.erode(sobel_y, (5,5), iterations=1)
    sobel_x = cv2.dilate(sobel_x, (3,3), iterations=2)
    sobel_y = cv2.dilate(sobel_y, (3,3), iterations=2)
    
    
    return sobel_x, sobel_y
    
    
    
def preprocesser(img) :
    img[:int(img_size_y/2),:, :] = 0
    hsv_color = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    hsv_lower = np.array([15,20,20])
    hsv_upper = np.array([30,255,255])
    
    hsv_mask = cv2.inRange(hsv_color, hsv_lower, hsv_upper)
    
    hsv_filterd = cv2.bitwise_and(hsv_color, hsv_color, mask=hsv_mask)
    color_filterd = cv2.cvtColor(hsv_filterd, cv2.COLOR_HSV2BGR)
    
    
    return color_filterd
    
    
    
    
# def gradient_func(img, sobel_x, sobel_y) :
#     sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
#     sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)

#     # Calculate the gradient magnitude
#     gradmag = np.sqrt(sobelx**2 + sobely**2)

#     # Rescale to 8 bit
#     scale_factor = np.max(gradmag)/255
#     gradmag = (gradmag/scale_factor).astype(np.uint8)

#     th_mag = (30, 255)

#     gradient_magnitude = np.zeros_like(gradmag)
#     gradient_magnitude[(gradmag >= th_mag[0]) & (gradmag <= th_mag[1])] = 255
#     # plt.imshow(gradient_magnitude)
#     sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=15)
#     sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=15)

#     # Take the absolute value of the gradient direction,
#     # apply a threshold, and create a binary image result
#     absgraddir = np.arctan2(np.absolute(sobely), np.absolute(sobelx))
#     gradient_direction = np.zeros_like(absgraddir)

#     th_dir = (0.7, 1.3)
#     gradient_direction[(absgraddir >= th_dir[0]) & (absgraddir <= th_dir[1])] = 255
#     gradient_direction = gradient_direction.astype(np.uint8)
#     # plt.imshow(gradient_direction)

#     grad_combine = np.zeros_like(gradient_direction).astype(np.uint8)
#     grad_combine[((sobel_x > 1) & (gradient_magnitude > 1) & (gradient_direction > 1)) | ((sobel_x > 1) & (sobel_y > 1))] = 255
#     # plt.imshow(grad_combine)
    
#     return gradient_magnitude, gradient_direction, grad_combine

def hls_transf(img) :
    hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    height, width = img.shape[:2]
    _, img = cv2.threshold(img, 180, 255, cv2.THRESH_BINARY)

    H = hls[:,:,0] # get Hue channel (색상)
    L = hls[:,:,1] # get Light channel (밝기)
    S = hls[:,:,2] # get Saturation channel (채도)
    
    th_h, th_l, th_s = (160, 255), (50, 160), (0, 255)
    h_img = np.zeros_like(H)
    h_img[(H > th_h[0]) & (H <= th_h[1])] = 255
    l_img = np.zeros_like(L)
    l_img[(L > th_l[0]) & (L <= th_l[1])] = 255
    s_img = np.zeros_like(S)
    s_img[(S > th_s[0]) & (S <= th_s[1])] = 255
    
    hls_combine = np.zeros_like(s_img).astype(np.uint8)
    hls_combine[((s_img > 1) & (l_img == 0)) | ((s_img == 0) & (h_img > 1) & (l_img > 1))] = 255 
    
    return h_img, l_img, s_img, hls_combine

def perspective_transf(img, combine) :
    global fig, ax
    
    height, width = img.shape[:2]
    print(height, width)
    src = np.float32([[int(img_size_x * 0.2), int(img_size_y * 0.7)],   ##  1 2 
                    [int(img_size_x * 0.8), int(img_size_y * 0.7)],     ## 4   3
                    [int(img_size_x * 0.9), int(img_size_y * 0.9)],     ## (x, y)
                    [int(img_size_x * 0.1), int(img_size_y * 0.9)]
                    ])
    dst = np.float32([[0, 0],
                    [width, 0],
                    [width, height],
                    [0, height]])

    M = cv2.getPerspectiveTransform(src, dst)                                       ##함수제공
    Minv = cv2.getPerspectiveTransform(dst, src)
    warp_img = cv2.warpPerspective(combine, M, (1280, 720), flags=cv2.INTER_LINEAR)
    
    
    histogram = np.sum(warp_img[int(warp_img.shape[0] / 2):, :], axis=0 )
    
    output = np.dstack((warp_img, warp_img, warp_img)) * 255
    
    
    
    

    plt.plot(histogram)
    # plt.imshow(output)
    plt.show()
    plt.pause(0.1)
    ax.clear()
    
    midpoint = int(histogram.shape[0] / 2)

    # These will be the starting point for the left and right lines
    start_leftX = np.argmax(histogram[:midpoint])
    start_rightX = np.argmax(histogram[midpoint:]) + midpoint

    print("start_leftX :", start_leftX, "// start_rightX :", start_rightX)
    
    
    return warp_img, (start_leftX, start_rightX)
    
    
    
def sliding_windows(output,warp_img, start_leftX, start_rightX) :
    
    left_line = Line()
    right_line = Line()
    
    num_windows = 10
    # Set height of windows
    window_height = np.int(warp_img.shape[0] / num_windows)

    print(f"number of windows : {num_windows}, height of window : {window_height}")
    # Identify the x and y positions of all nonzero pixels in the image
    # zero-pixel이 아닌 모든 픽셀의 x와 y 포지션
    nonzero = warp_img.nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])

    # Current positions to be updated for each window
    # 현재 포지션(각 window마다 업데이트) 
    current_leftX = start_leftX
    current_rightX = start_rightX

    # Set minimum number of pixels found to recenter window
    # 최소 픽셀
    min_num_pixel = 50

    window_margin = left_line.window_margin
    print(window_margin)
    # Create empty lists to receive left and right lane pixel indices
    win_left_lane = []
    win_right_lane = []

    # Step through the windows one by one
    for window in range(num_windows):
        # Identify window boundaries in x and y (and right and left)
        # 윈도우 경계 값을 정의하고 시각화
        win_y_low = warp_img.shape[0] - (window + 1) * window_height
        win_y_high = warp_img.shape[0] - window * window_height
        win_leftx_min = current_leftX - window_margin
        win_leftx_max = current_leftX + window_margin
        win_rightx_min = current_rightX - window_margin
        win_rightx_max = current_rightX + window_margin

        # Draw the windows on the visualization image
        cv2.rectangle(output, (win_leftx_min, win_y_low), (win_leftx_max, win_y_high), (0, 255, 0), 2)
        cv2.rectangle(output, (win_rightx_min, win_y_low), (win_rightx_max, win_y_high), (0, 255, 0), 2)
        
        # 윈도우 내부에 non-zero pixel 검출하고 리스트에 추가
        # Identify the nonzero pixels in x and y within the window
        left_window_inds = ((nonzeroy >= win_y_low) & (nonzeroy <= win_y_high) & (nonzerox >= win_leftx_min) & (
            nonzerox <= win_leftx_max)).nonzero()[0]
        right_window_inds = ((nonzeroy >= win_y_low) & (nonzeroy <= win_y_high) & (nonzerox >= win_rightx_min) & (
            nonzerox <= win_rightx_max)).nonzero()[0]
        # Append these indices to the lists
        win_left_lane.append(left_window_inds)
        win_right_lane.append(right_window_inds)

        # If you found > minpix pixels, recenter next window on their mean position
        if len(left_window_inds) > min_num_pixel:
            current_leftX = np.int(np.mean(nonzerox[left_window_inds]))
        if len(right_window_inds) > min_num_pixel:
            current_rightX = np.int(np.mean(nonzerox[right_window_inds]))
        
    # Concatenate the arrays of indices
    # 인덱스 어레이 연결(concatenate)
    win_left_lane = np.concatenate(win_left_lane)
    win_right_lane = np.concatenate(win_right_lane)

    # Extract left and right line pixel positions
    leftx, lefty = nonzerox[win_left_lane], nonzeroy[win_left_lane]
    rightx, righty = nonzerox[win_right_lane], nonzeroy[win_right_lane]

    output[lefty, leftx] = [255, 0, 0]
    output[righty, rightx] = [0, 0, 255]
    plt.imshow(output)
    
    
    

def main() :
    
    pipeline = rs.pipeline()
    config = rs.config()

    config.enable_stream(rs.stream.depth,img_size_x,img_size_y, rs.format.z16, 30)
    config.enable_stream(rs.stream.color,img_size_x,img_size_y, rs.format.bgr8, 30)
    
    profile = pipeline.start(config)    
    
    while True :
        
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_img = np.asanyarray(color_frame.get_data())
        
        color_filterd = preprocesser(color_img)
        gray_img = cv2.cvtColor(color_filterd, cv2.COLOR_BGR2GRAY)
        
        
        Y, X, _ = color_img.shape
        
        sobel_x, sobel_y = prescaler(gray_img)
        ###
        combined_binary = np.zeros_like(sobel_x)
        combined_binary[(sobel_x == 255) | (sobel_y == 255)] = 255
        ###
        
        # gradient_magnitude, gradient_direction, grad_combine = gradient_func(gray_img, sobel_x, sobel_y)
        
        h_img, l_img, s_img, hls_combine = hls_transf(color_img)
        warp_img, (start_leftX, start_rightX) = perspective_transf(color_img, combined_binary)
        
        
        cv2.polylines(color_img, [np.array([[int(img_size_x * 0.2), int(img_size_y * 0.7)],   ##  1 2 
                    [int(img_size_x * 0.8), int(img_size_y * 0.7)],     ## 4   3
                    [int(img_size_x * 0.9), int(img_size_y * 0.9)],     ## (x, y)
                    [int(img_size_x * 0.1), int(img_size_y * 0.9)]
                    ])], True, (0,255,0), 2)
        cv2.circle(color_img, (start_leftX,int(img_size_y * 0.9)),5, (255,0,0), -1, cv2.LINE_AA)
        cv2.circle(color_img, (start_rightX,int(img_size_y * 0.9)),5, (255,0,0), -1, cv2.LINE_AA)
        
        
        
        
        cv2.imshow('Origin',color_img)
        cv2.imshow('color_filterd',color_filterd)
        
        # cv2.imshow('sobel_x',sobel_x)
        # cv2.imshow('sobel_y',sobel_y)
        # cv2.imshow('gradient_magitude',gradient_magnitude)
        # cv2.imshow('gradient_direction',gradient_direction)
        # cv2.imshow('grad_combine',grad_combine)
        
        # cv2.imshow("h_img", h_img)
        # cv2.imshow("l_img", l_img)
        # cv2.imshow("s_img", s_img)
        # cv2.imshow("combined_binary", combined_binary)
        # cv2.imshow("hls_combine",hls_combine)
        cv2.imshow("warp",warp_img)
        
        key = cv2.waitKey(1)
        if key == ord('q') :
            break
    cv2.destroyAllWindows()

if __name__ == "__main__" :
    main()