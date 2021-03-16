import rclpy

from rclpy.node import Node


from std_msgs.msg import Float32MultiArray


class HeadTiltDataPublisher(Node):

    def __init__(self):
        super().__init__('head_tilt_data_publisher')
        self.publisher_ = self.create_publisher(Float32MultiArray, 'tilt_head', 10)
        timer_period = 1.0
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.right = 0.0
        self.left = 0.0
        self.vertical = 0.0

    def timer_callback(self):
        msg1 = Float32MultiArray()
        msg2 = Float32MultiArray()
        msg3 = Float32MultiArray()
        msg1.data = [self.right, 1.0]
        msg2.data = [self.vertical, 0.0]
        msg3.data = [self.left, -1.0]


        self.publisher_.publish(msg1)

        self.get_logger().info('Publishing: %f' % msg1.data[0])

        self.publisher_.publish(msg2)

        self.get_logger().info('Publishing: %f' % msg2.data[0])

        self.publisher_.publish(msg3)

        self.get_logger().info('Publishing: %f' % msg3.data[0])
        

def main(args=None):
    rclpy.init(args=args)

    head_tilt_data_publisher = HeadTiltDataPublisher()

    rclpy.spin(head_tilt_data_publisher)

    head_tilt_data_publisher.destroy_node()

    rclpy.shutdown()

if __name__ == '__main__':
    main()