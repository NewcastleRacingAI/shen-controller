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

import math

from .purepursuit import get_angle

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('nrai_controller')
        self.publisher_cmd = self.create_publisher(AckermannDriveStamped, '/cmd', 10)
        self.subscriber_path = self.create_subscription(Path, '/path', self.process, 10)

    def process(self, msg):
        drive = AckermannDriveStamped()
        get_angle(msg.poses, drive.drive)
        #self.publisher_cmd.publish(get_angle(msg.poses))


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()