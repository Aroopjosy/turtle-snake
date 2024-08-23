#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.srv import Kill

class TurtleKillNode(Node):
    def __init__(self):
        super().__init__('turtle_kill_node')
        self.client = self.create_client(Kill, 'kill')
        
        # Make sure the service is available
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for Kill service...')

        # Call the service with the turtle name
        turtle_name = 'bite'  # Change this to the name of the turtle you want to kill
        self.call_kill_service(turtle_name)

    def call_kill_service(self, turtle_name):
        request = Kill.Request()
        request.name = turtle_name
        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        
        if future.result() is not None:
            self.get_logger().info(f'Successfully killed {turtle_name}')
        else:
            self.get_logger().error(f'Failed to kill {turtle_name}')

def main():
    rclpy.init()
    node = TurtleKillNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Node stopped by user.')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
