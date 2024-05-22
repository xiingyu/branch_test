import pyrealsense2 as rs

def list_all_options(sensor):
    # 모든 옵션을 나열하여 각 옵션의 이름과 기본값을 출력합니다
    for option in sensor.get_supported_options():
        print(option, sensor.get_option(option))

# 파이프라인을 생성하고 구성합니다
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# 파이프라인을 시작합니다
pipeline.start(config)

# 센서 장치를 가져옵니다
device = pipeline.get_active_profile().get_device()
depth_sensor = device.query_sensors()[0]

# 사용 가능한 모든 옵션을 나열합니다
list_all_options(depth_sensor)

# projector_power 옵션이 무엇인지 확인합니다
# IR 프로젝터 파워 값을 가져옵니다 (올바른 옵션 이름을 사용합니다)
try:
    projector_power_option = rs.option('projector_power')
    default_ir_projector_power = depth_sensor.get_option(projector_power_option)
    print(f"기본 IR 프로젝터 파워 값은 {default_ir_projector_power}입니다.")
except Exception as e:
    print(f"Error: {e}")

# 스트리밍을 중지합니다
pipeline.stop()