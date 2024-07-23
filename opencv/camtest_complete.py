import cv2
import numpy as np
import time

total_num = 14
cap = []
img_list = [None] * total_num
cam_list = []

def main():
    global cap, img_list, cam_list

    for i in range(total_num):
        capture = cv2.VideoCapture(i)
        cap.append(capture)

        if cap[i].isOpened():
            ret, img_list[i] = cap[i].read()
            if ret:
                cam_list.append(i)

    print("passed cap")

    while True:
        for i in range(len(cam_list)):
            ret, img = cap[cam_list[i]].read()
            if ret:
                cv2.imshow(f'{cam_list[i]} camera data', img)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    for capture in cap:
        capture.release()

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
