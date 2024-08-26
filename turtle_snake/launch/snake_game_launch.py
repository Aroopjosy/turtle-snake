
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
        Node(
            package='turtle_snake',
            executable='turtle_spawn_node.py',
            name='turtle_spawner',
            parameters=[
                {'turtle_prefix': 'my_turtle'},
                {'spawm_frequency': 2.0}
            ]
        ),
        Node(
            package='turtle_snake',
            executable='turtle_controller_node.py',
            name='turtle_controller',
            parameters=[
                {'catch_closest_turtle' : True}
            ]
        )
  ])