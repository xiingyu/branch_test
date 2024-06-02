import pyrealsense2 as rs
import numpy as np
import time

class ComplementaryFilter:
    def __init__(self, alpha=0.98):
        self.alpha = alpha
        self.angle = np.zeros(3)  # Roll, Pitch, Yaw

    def update(self, gyro, acc_angle, dt):
        self.angle = self.alpha * (self.angle + gyro * dt) + (1 - self.alpha) * acc_angle
        return self.angle

def initialize_camera():
    # Start the frames pipe
    p = rs.pipeline()
    conf = rs.config()
    conf.enable_stream(rs.stream.accel)
    conf.enable_stream(rs.stream.gyro)
    p.start(conf)
    return p

def gyro_data(gyro):
    return np.asarray([gyro.x, gyro.y, gyro.z])

def accel_data(accel):
    return np.asarray([accel.x, accel.y, accel.z])

def calculate_acc_angle(accel):
    acc_angle = np.zeros(3)
    acc_angle[0] = np.arctan2(accel[1], np.sqrt(accel[0]**2 + accel[2]**2))  # Roll
    acc_angle[1] = np.arctan2(-accel[0], np.sqrt(accel[1]**2 + accel[2]**2))  # Pitch
    return acc_angle

p = initialize_camera()
filter = ComplementaryFilter()

try:
    prev_time = time.time()
    while True:
        f = p.wait_for_frames()
        accel = accel_data(f[0].as_motion_frame().get_motion_data())
        gyro = gyro_data(f[1].as_motion_frame().get_motion_data())

        current_time = time.time()
        dt = current_time - prev_time
        prev_time = current_time

        acc_angle = calculate_acc_angle(accel)
        angle = filter.update(gyro, acc_angle, dt)

        print("Filtered angles (Roll, Pitch, Yaw): ", angle)

        time.sleep(0.01)

finally:
    p.stop()
