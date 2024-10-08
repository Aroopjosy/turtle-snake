#!/usr/bin/env python3

import rclpy
import math
from rclpy.node import Node
from turtlesim.msg import Pose
from turtlesim.srv import Kill
from geometry_msgs.msg import Twist
from turtle_snake.msg import TurtleArray
from turtle_snake.srv import CatchTurtle

class TurtleControllerNode(Node):

    def __init__(self):

        super().__init__('turtle_controller')

        self.declare_parameter("catch_closest_turtle", True)

        self.pose_ = None
        self.bite_turtle_ = None
        self.catch_closest_turtle = self.get_parameter('catch_closest_turtle').value
        self.cmd_vel_publisher_ = self.create_publisher(Twist, 'master/cmd_vel', 10)
        self.create_subscription(Pose, '/master/pose', self.turtle_pose_callback, 10)
        self.create_subscription(TurtleArray, 'alive_turtles', self.alive_turtle_callback, 10)
        self.turtle_kill_client = self.create_client(Kill, 'kill')
        self.catch_turtle_client = self.create_client(CatchTurtle, 'catch_turtle')
        self.timer = self.create_timer(0.1, self.timer_callback,)


    def turtle_pose_callback(self, msg):
        self.pose_ = msg

    def alive_turtle_callback(self, msg):
        if len(msg.turtles) > 0:
            if self.catch_closest_turtle:
                closest_turtle = None
                closest_turtle_distance = None

                for turtle in msg.turtles:
                    dist_x = turtle.x- self.pose_.x
                    dist_y = turtle.y - self.pose_.y
                    distance = math.sqrt(dist_x * dist_x + dist_y * dist_y)

                    if closest_turtle is None or distance < closest_turtle_distance:
                        closest_turtle = turtle
                        closest_turtle_distance = distance

                self.bite_turtle_ = closest_turtle
                print("==============================================")
            else:
                self.bite_turtle_ = msg.turtles[0]

        else:
            self.get_logger().info(f"bite turtle not added")


    def call_catch_turtle_service(self, turtle_name):
        while not self.catch_turtle_client.wait_for_service(0.1):
            self.get_logger().info("waiting for catch turtle service")
        
        request = CatchTurtle.Request()
        request.name = turtle_name
        future = self.catch_turtle_client.call_async(request)
        future.add_done_callback(self.catch_turtle_callback)

    def catch_turtle_callback(self, future):
        try:
            response =future.result()
            if response.success:
                self.get_logger().info("turtle killed")

        except Exception as e:
            self.get_logger().warn("turtle kill erorr : %s ",e)

    def timer_callback(self):
        if self.pose_ is None or self.bite_turtle_ is None:
            self.get_logger().info("looking for turtle...")
            return
        
        dist_x = self.bite_turtle_.x- self.pose_.x
        dist_y = self.bite_turtle_.y - self.pose_.y
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
            self.get_logger().info(f"Kill turtle Name: {self.bite_turtle_.name}")
            self.call_catch_turtle_service(self.bite_turtle_.name)
            self.bite_turtle_ =None

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



        
