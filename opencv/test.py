import cv2
import time

def main() :
    cam = cv2.VideoCapture(0)

    ret, img = cam.read()
    print(img.shape)

    cv2.imshow("img", img)

    key = cv2.waitKey(0)

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__" :
    main()