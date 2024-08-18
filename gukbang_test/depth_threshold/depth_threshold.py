import pyrealsense2 as rs
import numpy as np
import cv2

# RealSense 파이프라인 설정
pipeline = rs.pipeline()
config = rs.config()

# 스트림 설정 (Depth와 Color 스트림 활성화)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# 스트리밍 시작
pipeline.start(config)

try:
    while True:
        # 프레임을 가져오기
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        if not depth_frame or not color_frame:
            continue

        # Depth 이미지를 Numpy 배열로 변환
        depth_image = np.asanyarray(depth_frame.get_data())
        
        # x 방향의 차이 계산
        dx = np.abs(np.diff(depth_image, axis=1))
        
        # y 방향의 차이 계산
        dy = np.abs(np.diff(depth_image, axis=0))
        
        # 차이 값을 통합하여 급격한 변화 영역을 계산
        gradient_magnitude = np.hypot(dx[:-1, :], dy[:, :-1])
        
        # 임계값 설정 (예: 1000)
        threshold = 10
        
        # 급격한 거리 변화가 있는 영역 찾기
        edges = gradient_magnitude > threshold
        
        # 멀리 있는 데이터를 제거할 마스크 생성
        depth_mask = np.ones_like(depth_image, dtype=bool)
        
        # 급격히 변화한 지점 이후의 데이터를 제거
        depth_mask[:-1, :-1] = ~edges
        
        # 마스크 적용하여 멀리 있는 데이터를 날림
        filtered_depth_image = np.where(depth_mask, depth_image, 0)
        
        # Depth 이미지를 컬러맵으로 변환하여 시각화
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(filtered_depth_image, alpha=0.03), cv2.COLORMAP_JET)
        
        # 결과 이미지 표시
        cv2.imshow('Filtered Depth Image', depth_colormap)
        
        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # 스트리밍 정지
    pipeline.stop()
    cv2.destroyAllWindows()
