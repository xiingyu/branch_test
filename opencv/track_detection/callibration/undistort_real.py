import cv2
import numpy as np

# # 저장된 npz 파일 불러오기
# with np.load('camera_matrix_ov2710.npz') as data:
#     print(data['dist'])
#     mtx = data['mtx']
#     dist = data['dist']

# # 왜곡된 이미지 불러오기
# img = cv2.imread('./images/image2.png')
# h, w = img.shape[:2]

# # 새로운 카메라 매트릭스 계산
# newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

# # 왜곡 보정
# undistorted_img = cv2.undistort(img, mtx, dist, None, newcameramtx)

# roix,roiy,roiw,roih = roi
# result = undistorted_img[roiy:roiy+roih,roix : roix + roiw]
# # 보정된 이미지 저장
# # cv2.imwrite('undistorted_image.jpg', undistorted_img)

# # 보정된 이미지 보여주기
# cv2.imshow('undistorted_image', undistorted_img)
# cv2.imshow("result",result)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
cam_num = 4

def main() :
    # cap = cv2.VideoCapture(4)
    
    cap = cv2.VideoCapture(cam_num)
    print('set resolution width {} height {}'.format(1920, 1080))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print('changed resolution width {} height {}'.format(width, height))
    
    with np.load('camera_matrix_ov2710.npz') as data:
        print(data['dist'])
        mtx = data['mtx']
        dist = data['dist']
        
    while True :
        ret, img = cap.read()
        
        if not ret :
            print("fail")
        else :
            h, w = img.shape[:2]
            newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

            undistorted_img = cv2.undistort(img, mtx, dist, None, newcameramtx)
            roix,roiy,roiw,roih = roi
            result = undistorted_img[roiy-50:roiy+roih+50,roix-50 : roix + roiw+50]
            cv2.imshow("result",result)
            print(result.shape)
            
            key = cv2.waitKey(1)
            if key == ord('q') :
                break
            
    cap.release
    cv2.destroyAllWindows
    
if __name__ == "__main__" :
    main()