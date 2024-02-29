import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import math

# ROS 2 노드를 정의하는 클래스
class LidarNode(Node):

    def __init__(self):
        super().__init__('lidar_node')

        # ROS 2로 변환될 때 사용할 변수 및 구조체 정의
        self.angle_in = []
        self.size = 0
        self.angle_increment = 0.0
        self.range_min = 0.10
        self.range_max = 12.0
        self.ros_n_mul = 2

        # ROS 2로 변환될 때 사용할 publisher 정의
        self.publisher_ = self.create_publisher(LaserScan, 'scan', 10)

        # ROS 1 노드에서 사용되는 함수들을 여기에 추가하여 ROS 1 코드를 이식합니다.
        # 예: serial 통신 설정, 데이터 처리 함수 등

    def point_cloud_filter(self, scan):
        # 레이저 스캔 데이터의 간단한 필터링 함수
        # 여기에 필터링 로직 추가
        pass

    def angle_insert(self, scan_in):
        # 각도 보간 함수
        scan_out = LaserScan()

        temp_size = 500  # 레이더가 한 바퀴 돌 때 생성되는 포인트 수

        scan_out.ranges = [math.inf] * (temp_size * self.ros_n_mul)
        scan_out.intensities = [0] * (temp_size * self.ros_n_mul)

        for i in range(self.size):
            temp_i = int(self.angle_in[i] / (360.0 / (self.ros_n_mul * temp_size)) + 0.5)
            temp_i = min(temp_i, temp_size * self.ros_n_mul - 1)

            if scan_in.ranges[i] == 0:
                scan_out.ranges[temp_i] = math.inf
            else:
                scan_out.ranges[temp_i] = scan_in.ranges[i]
                scan_out.intensities[temp_i] = 127 if scan_in.ranges[i] > 0 else 0

        scan_out.angle_increment = 2.0 * math.pi / (self.ros_n_mul * temp_size)
        scan_out.angle_min = 0.0
        scan_out.angle_max = 2 * math.pi - scan_out.angle_increment
        scan_out.range_min = self.range_min
        scan_out.range_max = self.range_max

        return scan_out

    def poll(self):
        # 레이더 데이터 수신 함수
        scan = LaserScan()

        # 여기에 레이더 데이터 수신 및 처리 로직 추가

        return scan

    def run(self):
        while rclpy.ok():
            scan = self.poll()
            self.point_cloud_filter(scan)
            scan_publish = self.angle_insert(scan)
            scan_publish.header.frame_id = 'laser_link'
            scan_publish.header.stamp = self.get_clock().now().to_msg()

            self.publisher_.publish(scan_publish)
            rclpy.spin_once(self)

# ROS 2 노드 실행
def main(args=None):
    rclpy.init(args=args)
    lidar_node = LidarNode()
    lidar_node.run()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
