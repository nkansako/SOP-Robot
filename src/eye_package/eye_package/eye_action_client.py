import sys

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node


from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

from std_msgs.msg import Float32
from std_msgs.msg import Float32MultiArray

class MoveEyeClientHorizontal(Node):

    def __init__(self):
        super().__init__('eye_client_node')
        # Action client to send goals to jaw controller
        self.eye_action_client_horizontal = ActionClient(self, FollowJointTrajectory, '/eyes_controller/follow_joint_trajectory')

        # Subscriber to get data from face tracker
        self.get_data = self.create_subscription(
            Float32MultiArray,
            'move_eye_horizontal',
            self.send_goal,
            10,
        )

    def send_goal(self, position):
        # Message type in JointTrajectory
        goal_msg = JointTrajectory()

        # Joint trajectory points
        jtp = JointTrajectoryPoint()
        jtp.velocities = [0.0]
        jtp.time_from_start.sec = 0
        jtp.time_from_start.nanosec = 0   
        jtp.positions = [position.data[0]]
        if position.data[1] == 1.0:
            joint = "eyes_shift_horizontal_joint"
        else:
            joint = "eyes_shift_vertical_joint"
        # Build message
        jointNames = []
        #print(joint)
        jointNames.append(joint)
        goal_msg.points = [jtp]
        goal_msg.joint_names = jointNames

        # Assign goal
        goal = FollowJointTrajectory.Goal()
        goal.trajectory = goal_msg

        self.eye_action_client_horizontal.wait_for_server()

        self.get_logger().info('Goal: %f ' % jtp.positions[0])

        self.eye_action_client_horizontal.send_goal_async(goal)


def main(args=None):

    rclpy.init(args=args)

    move_eye_client_horizontal = MoveEyeClientHorizontal()

    rclpy.spin(move_eye_client_horizontal)

    move_eye_client_horizontal.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
