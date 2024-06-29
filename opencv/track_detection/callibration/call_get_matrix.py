import cv2
import numpy as np
import glob

# 체크보드 크기
chessboard_size = (10, 7)    ##corner 개수
square_size = 1.0  # 실제 정사각형 크기, 단위는 임의

# 객체 포인트 (3D)
objp = np.zeros((np.prod(chessboard_size), 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2) * square_size

# 저장할 배열들
objpoints = []  # 3D 점
imgpoints = []  # 2D 점

# 이미지 불러오기
images = glob.glob('./images/*.png')  # 체크보드 이미지 경로

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 코너 찾기
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)
    
    if ret:
        objpoints.append(objp)
        imgpoints.append(corners)
        
        # 코너 그리기
        cv2.drawChessboardCorners(img, chessboard_size, corners, ret)
        cv2.imshow('img', img)
        cv2.waitKey(100)
        
cv2.destroyAllWindows()

# 카메라 매트릭스와 왜곡 계수 계산
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# 결과 저장
np.savez('camera_matrix_ov2710.npz', mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)
