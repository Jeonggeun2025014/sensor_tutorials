import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import matplotlib.pyplot as plt

class LidarSubscriber(Node):

    def __init__(self):
        super().__init__('lidar_subscriber')
        self.subscription = self.create_subscription(
            LaserScan, '/scan', self.scan_callback, 10)
        self.subscription
        self.get_logger().info('LidarSubscriber node started.')

        self.init_plot()
    
    def scan_callback(self, scan_msg):
        xs = []
        ys = []

        self.process_scan_data(scan_msg, xs, ys)
        self.plot_scan(xs, ys)  # 그래프 갱신

    def process_scan_data(self, scan_msg, xs, ys):
        # ranges 배열을 하나씩 순회하면서 (거리, 각도) -> (x, y)로 변환
        for i in range(len(scan_msg.ranges)):
            r = scan_msg.ranges[i]

            # 측정 실패(무한대/NaN) 데이터는 건너뜀
            if math.isinf(r) or math.isnan(r):
                continue

            # 노이즈 제거: 3m보다 먼 값은 3m로 클리핑
            if r > 3.0:
                r = 3.0

            # i번째 거리값에 해당하는 각도 계산
            angle = scan_msg.angle_min + i * scan_msg.angle_increment

            # 극좌표(r, angle) -> 직교좌표(x, y) 변환
            x = r * math.cos(angle)
            y = r * math.sin(angle)

            xs.append(x)
            ys.append(y)

    def init_plot(self):
        # 그래프 초기 설정 (x-y 직교좌표)
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.points, = self.ax.plot([], [], 'b.')
        self.ax.set_xlim(-3, 3)
        self.ax.set_ylim(-3, 3)
        self.ax.set_aspect('equal')
        self.ax.set_title("LiDAR Scan Data (X-Y View)")
        self.ax.set_xlabel("x (m)")
        self.ax.set_ylabel("y (m)")

    def plot_scan(self, xs, ys):
        self.points.set_data(xs, ys)
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

