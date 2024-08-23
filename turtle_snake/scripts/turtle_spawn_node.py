#!/usr/bin/env python3

import rclpy
import math
import random
from rclpy.node import Node
from turtlesim.srv import Spawn

class TurtleSpawner(Node):

    def __init__(self):

        super().__init__('turtle_spawner')
        self.turtle_name_prefix = 'turtle'
        self.counter = 0
        self.client = self.create_client(Spawn, 'spawn')
        self.create_timer(2.0, self.spwan_new_turtle)


    def spwan_new_turtle(self):
        self.counter += 1
        name = self.turtle_name_prefix + str(self.counter)
        x = random.uniform(0.0, 11.0)
        y = random.uniform(0.0, 11.0)
        theta = random.uniform(0.0, 2*math.pi)
        self.call_spwan_server(name, x, y, theta)  # call server for new turtle

    def call_spwan_server(self, turtle_name, x, y, theta):
        
        while not self.client.wait_for_service(timeout_sec=0.1):
            self.get_logger().info("wait for server......")

        request = Spawn.Request()
        request.name = turtle_name
        request.x = x
        request.y = y
        request.theta = theta
        future = self.client.call_async(request)
        future.add_done_callback(self.spwan_callback)

    def spwan_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info(f'Successfully spawned {response.name}')
        except Exception as e:
            self.get_logger().error(f'Failed to spawn turtle: {str(e)}')


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

    

