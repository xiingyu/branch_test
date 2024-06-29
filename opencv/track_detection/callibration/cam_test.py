# opencv 라이브러리
import cv2

# 카메라 열기
cap = cv2.VideoCapture(4)

# 현재 카메라 해상도 얻기
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print('default resolution width {} height {}'.format(width, height))

# 1280x720 해상도로 변경 시도
print('set resolution width {} height {}'.format(1280, 720))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# 1280x720 해상도로 변경 시도
print('set resolution width {} height {}'.format(1920, 1080))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# ret,img = cap.read()
# cv2.imshow("title", img)
# cv2.waitKey(0)


# 변경된 해상도 가져오기
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print('changed resolution width {} height {}'.format(width, height))

# # 600x400 해상도로 변경 시도
# print('set resolution width {} height {}'.format(600, 400))
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)

# # 변경된 해상도 가져오기
# width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
# height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
# print('changed resolution width {} height {}'.format(width, height))
