import cv2
import cv2.aruco as aruco
import time

ids_before = 51

def detect_aruco(frame) :
    global ids_before
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters_create()

    corners, ids, points = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)

    if ids is not None :
        if ids_before != ids[0] :
            ids_before = ids[0]
            print(f"Detected {ids[0]}")


def main() :
    cap = cv2.VideoCapture(0)

    while True :
        ret, img = cap.read()

        if not ret :
            print("fail to connection")
            time.sleep(1)
        else :
            resized = cv2.resize(img, dsize=(640,480), interpolation=cv2.INTER_LINEAR)
            detect_aruco(resized)
            cv2.imshow("img", resized)

            key = cv2.waitKey(1000)
            if key == ord('q') :
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__" :
    main()