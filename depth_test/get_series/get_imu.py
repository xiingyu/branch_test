import pyrealsense2 as rs
import numpy as np
import time


p = rs.pipeline()
conf = rs.config()
conf.enable_stream(rs.stream.accel)
conf.enable_stream(rs.stream.gyro)
prof = p.start(conf)




try:
    while True:
        f = p.wait_for_frames()
        accel = f[1].as_motion_frame().get_motion_data()
        gyro = f[0].as_motion_frame().get_motion_data()
        
        
        np.asarray([gyro.x, gyro.y, gyro.z])
        np.asarray([accel.x, accel.y, accel.z])
        
        # print(f'gyro data is {gyro}, accel data is {accel}')
        print(f'gyrodata x: {0.0000 if gyro.x == 0.0 else gyro.x} y: {0.0000 if gyro.y == 0 else gyro.y} z: {0.0000 if gyro.z == 0 else gyro.z} , accel x: {0.0000 if accel.x == 0 else accel.x} y: {0.0000 if accel.y == 0 else accel.y} z: {0.0000 if accel.z == 0 else accel.z}')
        time.sleep(0.1)


finally:
    p.stop()
