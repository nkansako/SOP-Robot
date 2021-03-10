import rclpy

from rclpy.node import Node

from std_msgs.msg import Float32



class EyeDataPublisherHorizontal(Node):

    def __init__(self):
        super().__init__('eye_data_publisher_horizontal')
        self.publisher_ = self.create_publisher(Float32, 'move_eye_horizontal', 10)
        timer_period = 1.0
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.left = True
        self.pos = 1.0

    def timer_callback(self):
        msg = Float32()
        msg.data = self.pos
        if self.left:
            self.pos = -1.0
            self.left = False
        else:
            self.pos = 1.0
            self.left = True

        self.publisher_.publish(msg)

        self.get_logger().info('Publishing: %f' % msg.data)
        

def main(args=None):
    rclpy.init(args=args)

    eye_data_publisher_horizontal = EyeDataPublisherHorizontal()

    rclpy.spin(eye_data_publisher_horizontal)

    eye_data_publisher_horizontal.destroy_node()

    rclpy.shutdown()

if __name__ == '__main__':
    main()