import cv2
import pyrealsense2 as rs
import os

folder_path = '/home/skh/testing_folder/gukbang_test/depth_learning/images'
img_num = len

def main() :
    cap = cv2.VideoCapture(0)
    
    num = len(os.listdir(folder_path))
    print(f'{num} of images detected.')
    
    while True :
        ret, img = cap.read()
        
        cv2.imshow("realtime", img)
        key = cv2.waitKey(1)
        
        if key == ord('q') :
            break
        elif key == ord('s') :
            cv2.imwrite(f'/home/skh/testing_folder/gukbang_test/depth_learning/images/img{num+1}.png', img)
            num = num+1
            print(f'saved as img{num}.png !!')
    
    cap.release
    cv2.destroyAllWindows
    
if __name__ == "__main__" :
    main()
        