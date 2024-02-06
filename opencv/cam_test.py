import cv2
import time

def main() :
    cap = cv2.VideoCapture(0)

    while True :
        ret, img = cap.read()

        if not ret :
            print("fail to connection")
            time.sleep(1)
        else :
            cv2.imshow("img", img)

            key = cv2.waitKey(1)
            if key == ord('q') :
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__" :
    main()