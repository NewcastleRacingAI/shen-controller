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

#from .purepursuit import get_angle

### Testing

from geometry_msgs.msg import PoseStamped
import math
#from ackermann_msgs.msg import AckermannDriveStamped, AckermannDrive
def get_angle(path: object, drive: object) -> object:

    lookahead_distance = 5
    max_angle = 21
    wheel_base = 5

    path.insert(0, PoseStamped())
    for i in range(0, len(path)-1):
        gradient = (path[i].pose.position.y - path[i+1].pose.position.y)/(path[i].pose.position.x - path[i+1].pose.position.x)
        constant = path[i].pose.position.y - (gradient*path[i].pose.position.x)

        a = 1 + math.pow(gradient, 2)
        b = 2 * gradient * constant
        c = math.pow(constant, 2) - math.pow(lookahead_distance, 2)

        discriminant = math.pow(b, 2) - (4 * a * c)

        if discriminant>=0:
            xplus = ((-1 * b) + math.sqrt(discriminant)) / (2 * a)
            xminus = ((-1 * b) - math.sqrt(discriminant)) / (2 * a)

            #print("Node " + str(i) + " and " + str(i+1))
            #print("[" + str(path[i].pose.position.x) + ", " + str(path[i+1].pose.position.x) + "]")

            #print("y = " + str(gradient) + "x + " + str(constant) + " {" + str(min(path[i+1].pose.position.x, path[i].pose.position.x)) + " < x < " + str(max(path[i+1].pose.position.x, path[i].pose.position.x)) + "}")

            yplus = (gradient * xplus) + constant
            yminus = (gradient * xminus) + constant

            #print("xplus: " + str(xplus) + " yplus: " + str(yplus))
            #print("xminus: " + str(xminus) + " yminus: " + str(yminus))
            #print("Magnitude: " + str(math.sqrt(math.pow(xplus, 2) + math.pow(yplus, 2))))

            if min(path[i+1].pose.position.x, path[i].pose.position.x) <= xplus <= max(path[i+1].pose.position.x, path[i].pose.position.x):
                a = (math.atan(yplus/xplus) % math.pi) - math.pi/2
                angle = math.atan(2 * wheel_base * math.sin(a)/(lookahead_distance))
                drive.steering_angle = angle
            elif min(path[i+1].pose.position.x, path[i].pose.position.x) <= xminus <= max(path[i+1].pose.position.x, path[i].pose.position.x):
                a = (math.atan(yminus/xminus) % math.pi) - math.pi/2
                angle = math.atan(2 * wheel_base * math.sin(a)/(lookahead_distance))
                drive.steering_angle = angle

        #print("M: " + str(m))
        #print("C: " + str(c))
        #print(path[i].pose.position.x)
        #print(path[i].pose.position.y)
        #print(path[i].pose.position.z)
        #print("~~~~~~~~~~")
    return drive

### End of Testing

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('controller')
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