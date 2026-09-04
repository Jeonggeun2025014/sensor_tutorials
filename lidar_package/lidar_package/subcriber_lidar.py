import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import matplotlib.pyplot as plt
import numpy as np

class LidarSubscriber(Node):

    def __init__(self):
        super().__init__('lidar_subscriber')
        self.subscription = self.create_subscription(
            LaserScan, '/scan', self.listener_callback, 10)
        self.subscription
        self.get_logger().info('LidarSubscriber node started.')

        # 그래프 초기 설정
        plt.ion()
        self.fig, self.ax = plt.subplots(subplot_kw={'projection': 'polar'})
        self.line, = self.ax.plot([], [], 'b.')
        self.ax.set_ylim(0, 10)  # 최대 10m
        self.ax.set_title("LiDAR Scan Data (Polar View)")

    def listener_callback(self, msg):
        ranges = np.array(msg.ranges)
        angles = np.arange(msg.angle_min, msg.angle_max, msg.angle_increment)
        ranges = np.clip(ranges, 0, 10)  # 노이즈 제거 (10m 이상 클리핑)

        # 극좌표 그래프 갱신
        self.line.set_data(angles, ranges)
        self.ax.figure.canvas.draw()
        self.ax.figure.canvas.flush_events()

def main(args=None):
    rclpy.init(args=args)
    node = LidarSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    plt.close()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


# import rclpy
# from rclpy.node import Node

# from std_msgs.msg import String
# from sensor_msgs.msg import LaserScan

# class LiDARlSubscriber(Node):

#     def __init__(self):
#         super().__init__('lidar_subscriber')
#         self.subscription = self.create_subscription(
#             LaserScan,
#             'scan',
#             self.lidar_callback,
#             10)
#         self.subscription  # prevent unused variable warning

#     def lidar_callback(self, msg):
#         self.get_logger().info('Lidar data: "%f"' % msg.ranges[0])


# def main(args=None):
#     rclpy.init(args=args)

#     lidar_subscriber = LiDARlSubscriber()

#     rclpy.spin(lidar_subscriber)

#     # Destroy the node explicitly
#     # (optional - otherwise it will be done automatically
#     # when the garbage collector destroys the node object)
#     lidar_subscriber.destroy_node()
#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()

