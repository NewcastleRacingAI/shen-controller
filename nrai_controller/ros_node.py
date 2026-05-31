#!/usr/bin/env python3
# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped, Pose, Point, Quaternion
from ackermann_msgs.msg import AckermannDriveStamped, AckermannDrive
from nav_msgs.msg import Path

import struct
import os

import math

from .purepursuit import get_angle

class MinimalPublisher(Node):

    def __init__(self, nims: bool):
        self.nims = nims
        super().__init__('nrai_controller')
        self.publisher_cmd = self.create_publisher(AckermannDriveStamped, '/cmd', 10)
        self.subscriber_path = self.create_subscription(Path, '/path', self.process, 10)

    def process(self, msg):
        drive = AckermannDriveStamped()
        drive.drive = get_angle(msg.poses, drive.drive)
        drive.drive.steering_angle_velocity = float(1)
        drive.drive.speed = float(0.5)
        drive.drive.acceleration = float(0.25)
        drive.drive.jerk = float(0.1)
        if self.nims:
            drive = drive.drive
            #new_instruction = bytes()
            #new_instruction += np.float32(drive.steering_angle).tobytes()
            #new_instruction += np.float32(drive.steering_angle_velocity).tobytes()
            #new_instruction += np.float32(drive.speed).tobytes()
            #new_instruction += np.float32(drive.acceleration).tobytes()
            #new_instruction += np.float32(drive.jerk).tobytes()
            #new_instruction += bytes(b'\xff\xff\xff\xff')
            new_instruction = struct.pack('<5fI', drive.steering_angle, drive.steering_angle_velocity, drive.speed, drive.acceleration, drive.jerk, 0xFFFFFFFF)
            try:
                fd = os.open("/tmp/lower_ctrl_cmd", os.O_WRONLY)
                with open(fd, "wb") as file:
                    file.write(new_instruction)
            except FileNotFoundError:
                self.get_logger().info("Could not access FIFO. Likely not yet configured.")
            except BrokenPipeError:
                self.get_logger().info("FIFO terminated")
        else:
            self.publisher_cmd.publish(drive)
        


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher(False)

    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()

def nims(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher(True)

    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()