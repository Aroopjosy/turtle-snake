# Turtle Catcher Simulation

This ROS 2 project demonstrates a turtle-catching simulation using the `turtlesim` package. The goal is to catch a turtle that moves around the screen autonomous control.

## Demo

![Watch the demo video](https://github.com/Aroopjosy/turtle-snake/blob/main/demo.gif)


*Click on the image above to watch the demo video.*

## Features

- Automated turtle-catching algorithm.
- Easy setup and installation.

## Installation Instructions

### Prerequisites

- **ROS 2 Humble Hawksbill** (or your ROS 2 version)
- **Ubuntu 22.04**

### Steps
1.**Create New  Workspace**
   ```bash
   mkdir -p turtle_ws/src
   cd turtle_ws/src
   ```
2.**Clone the repository:**
   ```bash
   git clone https://github.com/Aroopjosy/turtle-snake.git .
   cd ..
   ```
3.**Build Workspace**
 ```bash
   colcon build --packages-select turtle_snake --symlink-install
   ```
4.**Source & Run**
   ```bash
   source install/setup.bash
   ros2 launch turtle_snake turtle_snake_launch.py
   ```

