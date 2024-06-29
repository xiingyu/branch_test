import cv2
import numpy as np

# 저장된 npz 파일 불러오기
with np.load('camera_matrix_ov2710.npz') as data:
    print(data['dist'])
    mtx = data['mtx']
    dist = data['dist']

# 왜곡된 이미지 불러오기
img = cv2.imread('./images/image2.png')
h, w = img.shape[:2]

# 새로운 카메라 매트릭스 계산
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

# 왜곡 보정
undistorted_img = cv2.undistort(img, mtx, dist, None, newcameramtx)

roix,roiy,roiw,roih = roi
result = undistorted_img[roiy:roiy+roih,roix : roix + roiw]
# 보정된 이미지 저장
# cv2.imwrite('undistorted_image.jpg', undistorted_img)

# 보정된 이미지 보여주기
cv2.imshow('undistorted_image', undistorted_img)
cv2.imshow("result",result)
cv2.waitKey(0)
cv2.destroyAllWindows()
