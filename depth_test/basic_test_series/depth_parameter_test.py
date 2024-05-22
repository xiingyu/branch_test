import pyrealsense2 as rs
import cv2


def main() :
    
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, rs.format.z16, 30)
    
    pipeline.start(config)
    device = pipeline.get_active_profile().get_device()
    depth_sensor = device.query_sensors()[0]
    
    default_ir_projector_power = depth_sensor.get_option(rs.option.projector_power)
    print(f"기본 IR 프로젝터 파워 값은 {default_ir_projector_power}입니다.")
    
    
    
    # ir_projector_power = 150
    # depth_sensor.set_option(rs.option.projector_power, ir_projector_power)
    
    
    #########################        understood     #####################################
    
    # device = pipeline.get_active_profile().get_device()
    print(f'device : {device}')
    # device : <pyrealsense2.device: Intel RealSense D435I (S/N: 030522070636  FW: 5.16.0.1  on USB3.2)>

    # depth_sensor = pipeline.get_active_profile().get_device().query_sensors()[0]
    print(f'depth_sensor : {depth_sensor}')
    # depth_sensor : <pyrealsense2.sensor: "Stereo Module">
    
    ######################################################################################

    pipeline.stop()


if __name__ == "__main__" :
    main()