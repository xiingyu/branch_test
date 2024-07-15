import pyrealsense2 as rs
import numpy as np
import time

# 초기화 코드: 카메라 및 센서 초기화
def initialize_camera():
    # Start the frames pipeline
    p = rs.pipeline()
    conf = rs.config()
    conf.enable_stream(rs.stream.accel)
    conf.enable_stream(rs.stream.gyro)
    p.start(conf)
    return p

# 자이로 데이터 가져오기
def gyro_data(gyro):
    return np.asarray([gyro.x, gyro.y, gyro.z])

# 가속도 데이터 가져오기
def accel_data(accel):
    return np.asarray([accel.x, accel.y, accel.z])

# 센서 데이터 스트림 처리 함수
def update_angle(gyro_data, accel_data, dt, angle, accel_angle, alpha):
    # 자이로로부터 각속도 적분하여 각도 계산
    gyro_angle_change = gyro_data[0] * dt
    angle += gyro_angle_change
    
    # 가속도로부터 각도 계산
    accel_angle = np.arctan2(accel_data[1], accel_data[2])
    
    # 보완 필터로 각도 계산
    angle = alpha * (angle + gyro_angle_change) + (1 - alpha) * accel_angle

    return angle, accel_angle

# 카메라 및 센서 초기화
p = initialize_camera()

# 샘플링 주기 (초 단위)
dt = 0.05

# 보완 필터 상수
alpha = 0.98

# 초기화: 초기 각도 및 보정된 초기 각도 설정
initial_accel_angle = None
accel_angle = 0.0
angle = 0.0

try:
    while True:
        start_time = time.time()
        
        # 센서 데이터 프레임 읽기
        f = p.wait_for_frames()
        accel = accel_data(f[0].as_motion_frame().get_motion_data())
        gyro = gyro_data(f[1].as_motion_frame().get_motion_data())
        
        gyro = 0.0
        for i in range(10) :
            gyro += gyro_data(f[1].as_motion_frame().get_motion_data())
            
        gyro = gyro /10
        
        
        # 초기 가속도 각도 계산
        if initial_accel_angle is None:
            initial_accel_angle = np.arctan2(accel[1], accel[2])
            accel_angle = initial_accel_angle
        
        # 각도 업데이트
        angle, accel_angle = update_angle(gyro, accel, dt, angle, accel_angle, alpha)
        
        print(f"Current angle: {angle}")

        # 주기 조절을 위한 sleep (실제 시스템에서는 센서 샘플링 주기에 맞추어야 합니다)
        elapsed_time = time.time() - start_time
        time.sleep(max(0, dt - elapsed_time))
        # print(elapsed_time)

finally:
    p.stop()

    
    
    """
    import numpy as np
import time

# 초기 자이로 및 가속도 센서 값
gyro = np.array([0.0, 0.0, 0.0])  # 자이로 초기값 (rad/s)
accel = np.array([0.0, 0.0, 9.81])  # 가속도 초기값 (m/s^2), 가속도 중력 가속도로 초기화

# 샘플링 주기 (초 단위)
dt = 0.01

# 보완 필터 상수
alpha = 0.98

# 보정된 초기 각도
initial_accel_angle = np.arctan2(accel[1], accel[2])
accel_angle = initial_accel_angle

# 현재 각도 (초기 각도는 0으로 설정)
angle = 0.0

# 센서 데이터 스트림 처리 함수
def update_angle(gyro_data, accel_data, dt):
    global angle, accel_angle
    
    # 자이로로부터 각속도 적분하여 각도 계산
    gyro_angle_change = gyro_data[0] * dt
    angle += gyro_angle_change
    
    # 가속도로부터 각도 계산
    accel_angle = np.arctan2(accel_data[1], accel_data[2])
    
    # 보완 필터로 각도 계산
    angle = alpha * (angle + gyro_angle_change) + (1 - alpha) * accel_angle

    return angle

# 테스트를 위한 예제 데이터 (여기에 실제 센서 데이터를 사용하세요)
gyro_data_stream = [np.array([0.01, 0.0, 0.0])] * 1000  # 예제 자이로 데이터 (rad/s)
accel_data_stream = [np.array([0.0, 0.0, 9.81])] * 1000  # 예제 가속도 데이터 (m/s^2)

# 시간 경과에 따른 각도 추정
angles = []
for gyro_data, accel_data in zip(gyro_data_stream, accel_data_stream):
    current_angle = update_angle(gyro_data, accel_data, dt)
    angles.append(current_angle)
    time.sleep(dt)  # 실제 시스템에서는 센서 샘플링 주기에 맞추어야 합니다.

print(angles)

    """