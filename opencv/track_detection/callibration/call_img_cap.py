import cv2
import os

cam_num = 0

def main() :
    global cam_num
    
    cap = cv2.VideoCapture(cam_num)
    print('set resolution width {} height {}'.format(1920, 1080))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print('changed resolution width {} height {}'.format(width, height))
    
    while True :
        ret, img = cap.read()
        
        if not ret :
            print("fail")
        else :
            cv2.imshow("img", img)
            k = cv2.waitKey(1)
            if k == ord('q') :
                break
            elif k == ord('s') :
                l = os.listdir("./images/")
                cv2.imwrite(f'./images/image{len(l)+1}.png', img)
                print("img saved")
    cv2.destroyAllWindows
    cap.release
        
if __name__ == "__main__" :
    main()