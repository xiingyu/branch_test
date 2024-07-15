import numpy as np
import pyrealsense2 as rs
import time

prev_filtered_accel = np.array([0.0, 0.0, 0.0])


def apply_complementary_filter(accel):
    global prev_filtered_accel
    
    alpha = 0.3 # imu 값 필터링 . 낮을수록 필터 강해짐.
    beta = 1 - alpha
    
    filtered_accel = alpha * accel + beta * prev_filtered_accel
    prev_filtered_accel = filtered_accel
    return filtered_accel

def calculate_camera_state(accel):
    threshold_accel = 0.02# 각 임계값. imu 값 튀면 증가 / 1,-1로 변화가 잘 안 되면 감소 1.5, spring, fall 1.2, winter 0.02
    if accel[0] < -threshold_accel:
        state = 1  # Right
    elif accel[0] > threshold_accel:
        state = -1  # Left
    else:
        state = 0

    return state

    
def main() :
    
    timer_period = 0.1

    p = rs.pipeline()
    conf = rs.config()
    conf.enable_stream(rs.stream.accel)
    conf.enable_stream(rs.stream.gyro)
    prof = p.start(conf)


    state_window = []
    state_window_size = 5 # 상태 필터 값. 높으면 필터 강해짐.

    while True :
            
        
        f = p.wait_for_frames()
        accel = np.array([f[0].as_motion_frame().get_motion_data().x])
        filtered_accel = apply_complementary_filter(accel)
        state = calculate_camera_state(filtered_accel)

        state_window.append(state)

        if len(state_window) > state_window_size:
            state_window.pop(0)

        avg_state = int(np.mean(state_window))


        print(f'Filtered Accel: {filtered_accel}')
        print(f'Camera State: {avg_state}')
        
        time.sleep(timer_period)
        
        

    return 0


if __name__ == "__main__" :
    main()