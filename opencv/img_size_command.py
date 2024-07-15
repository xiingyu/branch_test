import cv2

img_size_x = 320
img_size_y = 180

def main() :
    cap = cv2.VideoCapture(4)   
    print("passed cap")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, img_size_x)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, img_size_y)

    while True :
        ret, img = cap.read()

        if not ret :
            print("fail to connection")
        else :
            cv2.imshow("img", img)

            key = cv2.waitKey(1)
            if key == ord('q') :
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__" :
    main()