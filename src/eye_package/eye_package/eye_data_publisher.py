import rclpy

from rclpy.node import Node

from std_msgs.msg import Float32
from std_msgs.msg import Float32MultiArray


class EyeDataPublisherHorizontal(Node):

    def __init__(self):
        super().__init__('eye_data_publisher_horizontal')
        self.publisher_ = self.create_publisher(Float32MultiArray, 'move_eye_horizontal', 10)
        timer_period = 1.0
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.left = True
        self.direction = 1.0
        self.x = 0.0
        self.y = 0.0

    def timer_callback(self):
        #msg = Float32()
        msg1 = Float32MultiArray()
        msg1.data = [self.x, 1.0]
        msg2 = Float32MultiArray()
        msg2.data = [self.y, -1.0]
        if self.left:
            self.left = False
            self.x = 0.5
            self.y = -0.5
        else:
            self.left = True
            self.x = -0.5
            self.y = 0.5

        self.publisher_.publish(msg1)

        self.get_logger().info('Publishing: %f' % msg1.data[0])

        self.publisher_.publish(msg2)

        self.get_logger().info('Publishing: %f' % msg2.data[0])
        

def main(args=None):
    rclpy.init(args=args)

    eye_data_publisher_horizontal = EyeDataPublisherHorizontal()

    rclpy.spin(eye_data_publisher_horizontal)

    eye_data_publisher_horizontal.destroy_node()

    rclpy.shutdown()

if __name__ == '__main__':
    main()