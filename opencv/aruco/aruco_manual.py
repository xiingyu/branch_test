import numpy as np
import cv2
import cv2.aruco as aruco

aruco_dict = aruco.Dictionary_create(9, 5)
print("Dictionary created successfully")

# add empty bytesList array to fill with 9 markers later
aruco_dict.bytesList = np.empty(shape=(9, 4, 4), dtype=np.uint8)

print("bytesList created successfully")

# Define markers
markers = [
    [[1,0,0,0,1],[1,0,0,1,0],[1,1,1,0,0],[1,0,0,1,0],[1,0,0,0,1]],  # K
    [[0,1,1,1,0],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[0,1,1,1,0]],  # O
    [[1,1,1,1,0],[1,0,0,0,1],[1,1,1,1,0],[1,0,0,1,0],[1,0,0,0,1]],  # R
    [[1,1,1,1,1],[1,0,0,0,0],[1,1,1,1,0],[1,0,0,0,0],[1,1,1,1,1]],  # E
    [[0,0,1,0,0],[0,1,0,1,0],[1,1,1,1,1],[1,0,0,0,1],[1,0,0,0,1]],  # A
    [[1,1,1,1,0],[1,0,0,0,1],[1,1,1,1,0],[1,0,0,1,0],[1,0,0,0,1]],  # R
    [[1,0,0,0,1],[1,1,0,1,1],[1,0,1,0,1],[1,0,0,0,1],[1,0,0,0,1]],  # M
    [[1,0,0,0,1],[0,1,0,1,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0]],  # Y
    [[0,1,0,1,0],[1,1,1,1,1],[1,1,1,1,1],[0,1,1,1,0],[0,0,1,0,0]]   # heart
]

# Convert markers to bytesList
for i, bits in enumerate(markers):
    mybits = np.array(bits, dtype=np.uint8)
    aruco_dict.bytesList[i] = aruco.Dictionary.getByteListFromBits(mybits)

# Corresponding characters for each marker
marker_chars = ["K", "O", "R", "E", "A", "R", "M", "Y", "Heart"]

aruco_param = aruco.DetectorParameters_create()

img_size_x = 1280
img_size_y = 720

# Open video capture from (first) webcam
cap = cv2.VideoCapture(4)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, img_size_x)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, img_size_y)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:
        # Convert to grayscale
        grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        bw = cv2.threshold(grayscale, 128, 255, cv2.THRESH_BINARY)[1]

        corners, ids, points = aruco.detectMarkers(bw, aruco_dict, parameters=aruco_param)
        
        # Draw markers on frame
        frame = aruco.drawDetectedMarkers(frame, corners)
        
        # Draw custom text
        if ids is not None:
            for i in range(len(ids)):
                corner = corners[i][0]
                top_left = (int(corner[0][0]), int(corner[0][1]))
                bottom_right = (int(corner[2][0]), int(corner[2][1]))
                # center = (int((top_left[0] + bottom_right[0]) / 2), int((top_left[1] + bottom_right[1]) / 2))
                
                marker_id = ids[i][0]
                if marker_id < len(marker_chars):
                    cv2.putText(frame, marker_chars[marker_id], top_left, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        
        # Display the resulting frame
        cv2.imshow('bw', bw)
        cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
