import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import math


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

        self.publisher_ = self.create_publisher(LaserScan, 'scan', 10)

    def point_cloud_filter(self, scan):
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
        scan = LaserScan()
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
    node = LidarNode()
    try :
        rclpy.spin(node.run())
    except KeyboardInterrupt :
        node.get_logger().info("interrupted")
    finally :
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
