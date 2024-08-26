#!/usr/bin/env python3

import rclpy
import math
import random
from rclpy.node import Node
from std_msgs.msg import String
from turtlesim.msg import Pose
from turtlesim.srv import Kill, Spawn
from geometry_msgs.msg import Twist
from turtle_snake.msg import TurtleArray
from turtle_snake.srv import CatchTurtle

class TurtleControllerNode(Node):

    def __init__(self):

        super().__init__('turtle_controller')

        self.goal_x = 8.0
        self.goal_y = 4.0
        self.pose_ = None
        self.bite_turtle_ = None
        self.bite_counter_  = 0
        self.create_subscription(Pose, '/master/pose', self.turtle_pose_callback, 10)
        self.cmd_vel_publisher_ = self.create_publisher(Twist, 'master/cmd_vel', 10)
        self.create_subscription(TurtleArray, 'alive_turtles', self.alive_turtle_callback, 10)
        self.timer = self.create_timer(0.1, self.timer_callback,)
        self.turtle_kill_client = self.create_client(Kill, 'kill')
        self.catch_turtle_client = self.create_client(CatchTurtle, 'catch_turtle')

    def turtle_pose_callback(self, msg):
        self.pose_ = msg

    def alive_turtle_callback(self, msg):
        if len(msg.turtles) > 0:
            # print("bitte count :", self.bite_counter_)
            self.bite_turtle_ = msg.turtles[0]

        else:

            self.get_logger().info(f"bite turtle not added")

    # def call_turtle_kill(self, turtle_name):
    #     while not self.turtle_kill_client.wait_for_service():
    #         self.get_logger().info("wait for kill server to online")

    #     request = Kill.Request()
    #     request.name = turtle_name
    #     future = self.turtle_kill_client.call_async(request)
    #     future.add_done_callback(self)

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
            self.get_logger().info("turtle killed : %s ",e)



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
            # self.get_logger().info("kill turtle Name : %s", self.bite_turtle_.name)
            self.get_logger().info(f"Kill turtle Name: {self.bite_turtle_.name}")
            self.call_catch_turtle_service(self.bite_turtle_.name)



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



        
