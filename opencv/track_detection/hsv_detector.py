import cv2

# 클릭 이벤트에 대한 콜백 함수
def get_hsv_value(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # 마우스 왼쪽 버튼 클릭 이벤트
        # 현재 프레임에서 클릭한 지점의 색상 가져오기
        bgr_color = frame[y, x]
        
        # BGR을 HSV로 변환
        hsv_color = cv2.cvtColor(bgr_color.reshape(1, 1, 3), cv2.COLOR_BGR2HSV)
        
        # HSV 값 출력
        print(f"Clicked at ({x}, {y}), HSV: {hsv_color[0][0]}")

# 카메라 초기화
cap = cv2.VideoCapture(4)

# 창에 콜백 함수 설정
cv2.namedWindow('Camera')
cv2.setMouseCallback('Camera', get_hsv_value)

# 실시간 영상 처리
while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # 영상 출력
    cv2.imshow('Camera', frame)
    
    if cv2.waitKey(1) & 0xFF == 27:  # ESC 키를 누르면 종료
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()
