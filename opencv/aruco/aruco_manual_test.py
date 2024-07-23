import numpy as np
import cv2
import cv2.aruco as aruco

# we will not use a built-in dictionary, but we could
# aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)


# define a custom dictionary with 3 markers of size 5x5
aruco_dict = aruco.Dictionary_create(3, 5)
print("Dictionary created successfully")

# add empty bytesList array to fill with 3 markers later
aruco_dict.bytesList = np.empty(shape = (4, 4, 4), dtype = np.uint8)

print("bytesList created successfully")

# add new marker(s)
mybits = np.array([[0,0,1,0,0],[0,1,0,1,0],[1,1,1,1,1],[1,0,0,0,1],[1,0,0,0,1]], dtype = np.uint8)  # A
aruco_dict.bytesList[0] = aruco.Dictionary.getByteListFromBits(mybits) 
mybits = np.array([[1,1,1,1,0],[1,0,0,0,1],[1,1,1,1,0],[1,0,0,0,1],[1,1,1,1,0]], dtype = np.uint8)  # B
aruco_dict.bytesList[1] = aruco.Dictionary.getByteListFromBits(mybits)
mybits = np.array([[0,1,1,1,0],[1,0,0,0,1],[1,0,0,0,0],[1,0,0,0,1],[0,1,1,1,0]], dtype = np.uint8)  # C 
aruco_dict.bytesList[2] = aruco.Dictionary.getByteListFromBits(mybits)
mybits = np.array([[1,0,1,0,0],[0,1,0,1,1],[0,1,1,0,0],[1,0,1,0,1],[1,1,1,0,0]], dtype = np.uint8)  # ArUco 5x5_50 id:0
aruco_dict.bytesList[3] = aruco.Dictionary.getByteListFromBits(mybits)

# save marker images
# for i in range(len(aruco_dict.bytesList)):
#     cv2.imwrite("custom_aruco_" + str(i) + ".png", aruco.generateImageMarker(aruco_dict, i, 128))

aruco_param = aruco.DetectorParameters_create()
# aruco_detector = aruco.ArucoDetector(aruco_dict, aruco_param)

# open video capture from (first) webcam
cap = cv2.VideoCapture(4)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:

        # Conver to grayscale
        grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        bw = cv2.threshold(grayscale, 128, 255, cv2.THRESH_BINARY)[1]

        corners, ids, points = aruco.detectMarkers(bw, aruco_dict, parameters=aruco_param)
        
        # draw markers on farme
        frame = aruco.drawDetectedMarkers(frame, corners, ids)

        # resize frame to show even on smaller screens
        frame = cv2.resize(frame, None, fx = 0.6, fy = 0.6)

        # Display the resulting frame
        cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()