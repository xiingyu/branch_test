import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import math, serial

class SCLaser:
    def __init__(self):
        print("sc_mini start")
        self.node = rclpy.create_node("sc_mini")

        baud_rate = self.node.get_parameter_or("~baud_rate", rclpy.ParameterValue(115200)).value
        frame_id = self.node.get_parameter_or("~frame_id", rclpy.ParameterValue("laser_link")).value
        port = self.node.get_parameter_or("~port", rclpy.ParameterValue("/dev/sc_mini")).value

        self.ser = serial.Serial(port, baud_rate)

        self.scan = sensor_msgs.msg.LaserScan()
        self.scan_publish = sensor_msgs.msg.LaserScan()

        self.laser_pub = self.node.create_publisher(sensor_msgs.msg.LaserScan, "scan", 1000)

        self.laser = SCLaser()



    def point_cloud_filter(self, scan):
        pass

    def angle_insert(self, scan_in, scan_out):
        pass

    def poll(self, scan):
        pass

class SCMiniNode(Node):
    def __init__(self):
        super().__init__('sc_mini')
        self.laser_pub = self.create_publisher(LaserScan, 'scan', 1000)
        self.scan = LaserScan()
        self.scan_publish = LaserScan()
        self.laser = SCLaser()

    def main_loop(self):
        while rclpy.ok():
            if self.laser.poll(self.scan) == 0:
                self.laser.point_cloud_filter(self.scan)
                self.laser.angle_insert(self.scan, self.scan_publish)
                self.scan_publish.header.frame_id = 'laser_link'
                self.scan_publish.header.stamp = self.get_clock().now().to_msg()
                self.laser_pub.publish(self.scan_publish)

def main(args=None):
    rclpy.init(args=args)
    node = SCMiniNode()
    node.main_loop()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
