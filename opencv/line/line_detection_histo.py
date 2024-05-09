import cv2
import numpy as np
import pyrealsense2 as rs
import math

import matplotlib.pyplot as plt

img_size_x = 1280
img_size_y = 720   
thresh_value = 120
thresh_max = 160
thresh_min = 50
thresh_weight = 1


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

    th_sobelx = (35, 100)
    sobel_x[(scaled_sobel >= th_sobelx[0]) & (scaled_sobel <= th_sobelx[1])] = 255
    
    abs_sobel = np.absolute(cv2.Sobel(img, cv2.CV_64F, 0, 1))

    th_sobely = (30, 255)
    scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel))
    sobel_y = np.zeros_like(scaled_sobel)
    sobel_y[(scaled_sobel >= th_sobely[0]) & (scaled_sobel <= th_sobely[1])] = 255
    
    return sobel_x, sobel_y
    
    
    
    
def gradient_func(img, sobel_x, sobel_y) :
    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)

    # Calculate the gradient magnitude
    gradmag = np.sqrt(sobelx**2 + sobely**2)

    # Rescale to 8 bit
    scale_factor = np.max(gradmag)/255
    gradmag = (gradmag/scale_factor).astype(np.uint8)

    th_mag = (30, 255)

    gradient_magnitude = np.zeros_like(gradmag)
    gradient_magnitude[(gradmag >= th_mag[0]) & (gradmag <= th_mag[1])] = 255
    # plt.imshow(gradient_magnitude)
    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=15)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=15)

    # Take the absolute value of the gradient direction,
    # apply a threshold, and create a binary image result
    absgraddir = np.arctan2(np.absolute(sobely), np.absolute(sobelx))
    gradient_direction = np.zeros_like(absgraddir)

    th_dir = (0.7, 1.3)
    gradient_direction[(absgraddir >= th_dir[0]) & (absgraddir <= th_dir[1])] = 255
    gradient_direction = gradient_direction.astype(np.uint8)
    # plt.imshow(gradient_direction)

    grad_combine = np.zeros_like(gradient_direction).astype(np.uint8)
    grad_combine[((sobel_x > 1) & (gradient_magnitude > 1) & (gradient_direction > 1)) | ((sobel_x > 1) & (sobel_y > 1))] = 255
    # plt.imshow(grad_combine)
    
    return gradient_magnitude, gradient_direction, grad_combine

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

def perspective_transf(img) :
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

    # s_LTop2, s_RTop2 = [270, 40], [310, 40]
    # s_LBot2, s_RBot2 = [100, height], [450, height]

    # src = np.float32([s_LBot2, s_RBot2, s_RTop2, s_LTop2]) 
    # dst = np.float32([(250, 0), (510, 0), (510, 720), (250, 720)]) 

    # Calculates a perspective transform from four pairs of the corresponding point
    M = cv2.getPerspectiveTransform(src, dst)                                       ##함수제공
    Minv = cv2.getPerspectiveTransform(dst, src)
    warp_img = cv2.warpPerspective(img, M, (1280, 720), flags=cv2.INTER_LINEAR)
    
    
    left_line = Line()
    right_line = Line()
    print(warp_img.shape)
    histogram = np.sum(warp_img[int(warp_img.shape[0] / 2):, :], axis=(0,2))
    plt.plot(histogram)
    plt.show()
    
    return warp_img
    

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
        
        
        Y, X, _ = color_img.shape
        
        sobel_x, sobel_y = prescaler(color_img)
        gradient_magnitude, gradient_direction, grad_combine = gradient_func(color_img, sobel_x, sobel_y)
        
        h_img, l_img, s_img, hls_combine = hls_transf(color_img)
        warp_img = perspective_transf(color_img)
        
        
        
        
        cv2.imshow('Origin',color_img)
        # cv2.imshow('sobel_x',sobel_x)
        # cv2.imshow('sobel_y',sobel_y)
        cv2.imshow('gradient_magitude',gradient_magnitude)
        # cv2.imshow('gradient_direction',gradient_direction)
        # cv2.imshow('grad_combine',grad_combine)
        
        # cv2.imshow("h_img", h_img)
        # cv2.imshow("l_img", l_img)
        # cv2.imshow("s_img", s_img)
        cv2.imshow("warp",warp_img)
        
        key = cv2.waitKey(1)
        if key == ord('q') :
            break
    cv2.destroyAllWindows()

if __name__ == "__main__" :
    main()