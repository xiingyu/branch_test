import cv2


cam_num = 8

def main() :
    cap = cv2.VideoCapture(cam_num)
    
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    
    while True : 
        ret, img = cap.read()
        
        if not ret :
            print("camera read fail")
        else :
            img_cp = img.copy()
            corners, ids, _ = cv2.aruco.detectMarkers(img, dictionary)
            
            
            # 적어도 하나의 마커가 감지된 경우
            if ids is not None:
                cv2.aruco.drawDetectedMarkers(img_cp, corners, ids)
            
            cv2.imshow("out", img_cp)
            key = cv2.waitKey(1)
            if key == ord('q') :
                break
                
    cv2.destroyAllWindows
    

if __name__ == "__main__" :
    main()