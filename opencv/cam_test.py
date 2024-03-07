import cv2
import time

# cam2 depth  frame
# cam4 origin frame

def main() :
    cap = cv2.VideoCapture(2)   
    print("passed cap")

    while True :
        ret, img = cap.read()

        print(ret)

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