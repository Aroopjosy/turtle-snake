
import launch
from launch_ros.actions import Node
# from 
# import turtlesim
def generate_launch_description():
    return launch.LaunchDescription([
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='main',
            remappings=[
                ('/turtle1/cmd_vel', '/master/cmd_vel'),
                ('/turtle1/color_sensor', '/master/color_sensor'),
                ('/turtle1/pose', '/master/pose')
            ]
        ),  
        # Node(
        #     package='turtlesim',
        #     executable='turtle_teleop_key',
        #     name='turtle_controller',
        # )
  ])