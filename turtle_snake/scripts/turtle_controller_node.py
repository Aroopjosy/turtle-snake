#!/usr/bin/env python3

import rclpy
import math
import random
from rclpy.node import Node
from std_msgs.msg import String
from turtlesim.msg import Pose
from turtlesim.srv import Kill, Spawn
from geometry_msgs.msg import Twist

class TurtleControllerNode(Node):

    def __init__(self):

        super().__init__('turtle_controller')

        self.goal_x = 8.0
        self.goal_y = 4.0
        self.pose_ = None

        self.create_subscription(Pose, '/master/pose', self.turtle_pose_callback, 10)
        self.cmd_vel_publisher_ = self.create_publisher(Twist, 'master/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)

    def turtle_pose_callback(self, msg):
        self.pose_ = msg

    def timer_callback(self):
        if self.pose_ is None:
            self.get_logger().info("looking for turtle...")
            return
        
        dist_x = self.goal_x- self.pose_.x
        dist_y = self.goal_y - self.pose_.y
        distance = math.sqrt(dist_x * dist_x + dist_y * dist_y)
       
        msg = Twist()
        
        if distance > 0.5:
            #position
            msg.linear.x = distance

            #orientation
            angle_to_goal = math.atan2(dist_y, dist_x)
            diff = angle_to_goal - self.pose_.theta
            if diff > math.pi:
                diff -= 2*math.pi

            elif diff < -math.pi:
                diff += 2*math.pi
            
            msg.angular.z = 6*diff

        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.get_logger().info("kill turtle ")

        self.cmd_vel_publisher_.publish(msg)

        


def main():
    rclpy.init()
    node = TurtleControllerNode()
    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()



        
