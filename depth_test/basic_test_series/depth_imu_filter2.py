import pyrealsense2 as rs
import numpy as np
import time
import math

# 각도 계산을 위한 변수 초기화
gyro_angle = np.array([0.0, 0.0, 0.0])
accel_angle = np.array([0.0, 0.0, 0.0])
filtered_angle = np.array([0.0, 0.0, 0.0])
alpha = 0.98  # Complementary filter 상수
prev_timestamp = None

# 파이프라인 설정
pipeline = rs.pipeline()
config = rs.config()

# IMU 스트림 활성화
config.enable_stream(rs.stream.gyro)
config.enable_stream(rs.stream.accel)

# 파이프라인 시작
pipeline.start(config)

def get_accel_angle(accel_data):
    x, y, z = accel_data
    pitch = math.atan2(y, math.sqrt(x**2 + z**2)) * 180 / math.pi
    roll = math.atan2(-x, z) * 180 / math.pi
    return np.array([pitch, roll])

try:
    while True:
        frames = pipeline.wait_for_frames()

        # 자이로스코프 프레임 가져오기
        gyro_frame = frames.first_or_default(rs.stream.gyro)
        accel_frame = frames.first_or_default(rs.stream.accel)
        
        if gyro_frame and accel_frame:
            gyro_data = gyro_frame.as_motion_frame().get_motion_data()
            accel_data = accel_frame.as_motion_frame().get_motion_data()
            curr_timestamp = gyro_frame.get_timestamp()

            if prev_timestamp is not None:
                dt = (curr_timestamp - prev_timestamp) / 1000.0  # 밀리초를 초로 변환

                # 자이로스코프 데이터를 이용한 각도 계산
                gyro = np.array([gyro_data.x, gyro_data.y, gyro_data.z])
                gyro_angle += gyro * dt

                # 가속도계를 이용한 각도 계산
                accel_angle_pitch_roll = get_accel_angle([accel_data.x, accel_data.y, accel_data.z])
                accel_angle = np.array([accel_angle_pitch_roll[0], accel_angle_pitch_roll[1], gyro_angle[2]])

                # Complementary Filter 적용
                filtered_angle = alpha * (filtered_angle + gyro * dt) + (1 - alpha) * accel_angle

            prev_timestamp = curr_timestamp

            print(f"Filtered Angle: {filtered_angle}")

        time.sleep(0.01)  # 너무 자주 호출되지 않도록 조정

finally:
    pipeline.stop()
