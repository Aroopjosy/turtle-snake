#!/usr/bin/env python3

import rclpy
import math
import random
from rclpy.node import Node
from turtlesim.srv import Spawn, Kill
from turtle_snake.msg import Turtle, TurtleArray
from turtle_snake.srv import CatchTurtle
class TurtleSpawner(Node):

    def __init__(self):

        super().__init__('turtle_spawner')

        self.declare_parameter('turtle_prefix', 'turtle')
        self.declare_parameter('spawm_frequency', 1.0)

        self.turtle_name_prefix = self.get_parameter('turtle_prefix').value
        self.spawn_frequency_ = self.get_parameter('spawm_frequency').value
        self.counter = 1
        self.alive_turtles_ = []
        self.turtles_publisher = self.create_publisher(TurtleArray, 'alive_turtles', 10)
        self.client = self.create_client(Spawn, 'spawn')
        self.turtle_kill_client = self.create_client(Kill, 'kill')
        self.catch_turtle_service_ = self.create_service(CatchTurtle, 'catch_turtle', self.catch_turtle_service_callback)
        self.create_timer(self.spawn_frequency_, self.spawn_new_turtle)



    def turtles_publish(self):
        msg = TurtleArray()
        msg.turtles = self.alive_turtles_
        self.turtles_publisher.publish(msg)

    def spawn_new_turtle(self):
        self.counter += 1
        name = self.turtle_name_prefix + str(self.counter)
        x = random.uniform(0.0, 11.0)
        y = random.uniform(0.0, 11.0)
        theta = random.uniform(0.0, 2*math.pi)
        self.call_spawn_server(name, x, y, theta)  # call server for new turtle

    def call_spawn_server(self, turtle_name, x, y, theta):
        while not self.client.wait_for_service(timeout_sec=0.1):
            self.get_logger().warn("wait for Spwan service")

        request = Spawn.Request()
        request.name = turtle_name
        request.x = x
        request.y = y
        request.theta = theta
        turtle = Turtle()
        turtle.name = turtle_name
        turtle.x = x
        turtle.y = y
        turtle.theta = theta
        self.alive_turtles_.append(turtle)
        future = self.client.call_async(request)
        future.add_done_callback(self.spwan_callback)

    def spwan_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info(f'Successfully spawned {response.name}')
            self.turtles_publish()

        except Exception as e:
            self.get_logger().error(f'Failed to spawn turtle: {str(e)}')

    def catch_turtle_service_callback(self, request, response):
        turtle_name = request.name
        self.call_turtle_kill_client(turtle_name)
        response.success = True
        return response

    def call_turtle_kill_client(self, turtle_name):
        while not self.turtle_kill_client.wait_for_service(0.2):
            self.get_logger().info("wait for turtle kill service")

        request = Kill.Request()
        request.name = turtle_name
        future = self.turtle_kill_client.call_async(request)
        future.add_done_callback(self.turtle_callback)
    
    def turtle_callback(self, future):
        try:
            future.result()
            self.get_logger().info(f'Successfully killed')
            del self.alive_turtles_[0]
            self.turtles_publish()

        except Exception as e:
            self.get_logger().error(f'Failed to kill turtle: {str(e)}')
        

def main():
    rclpy.init()
    node = TurtleSpawner()
    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        node.get_logger().info("User stopped node")

    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

    

