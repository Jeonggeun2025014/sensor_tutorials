import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from sensor_msgs.msg import LaserScan

class LiDARlSubscriber(Node):

    def __init__(self):
        super().__init__('lidar_subscriber')
        self.subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.lidar_callback,
            10)
        self.subscription  # prevent unused variable warning

    def lidar_callback(self, msg):
        self.get_logger().info('Lidar data: "%f"' % msg.ranges[0])


def main(args=None):
    rclpy.init(args=args)

    lidar_subscriber = LiDARlSubscriber()

    rclpy.spin(lidar_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    lidar_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()