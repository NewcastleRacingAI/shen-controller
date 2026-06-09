#!/usr/bin/env python3
import struct
import os
import math

from .purepursuit import get_angle

fifo_in = '/opt/PATHPLANNING_Path'
fifo_out = '/tmp/lower_ctrl_cmd'

class AckermannDrive():
    
    def __init__(self):
        self.steering_angle = float(0)
        self.steering_angle_velocity = float(1)
        self.speed = float(0.5)
        self.acceleration = float(0.25)
        self.jerk = float(0.1)

def main(args=None):
    
    fd_in = os.open(fifo_in, os.O_WRONLY)
        with open(fd_in, "wb") as file:
            while True:
                path = pickle.load(file)
                drive = AckermannDrive()
                
                get_angle(path, drive)
                steering_angle_velocity = float(1)
                speed = float(0.5)
                acceleration = float(0.25)
                jerk = float(0.1)
                
                new_instruction = struct.pack('<5fI', drive.steering_angle, drive.steering_angle_velocity, drive.speed, drive.acceleration, drive.jerk, 0xFFFFFFFF)
                try:
                    fd = os.open(fifo_out, os.O_WRONLY)
                    with open(fd, "wb") as fifo:
                        fifo.write(new_instruction)
                except FileNotFoundError:
                    self.get_logger().info("Could not access FIFO. Likely not yet configured.")
                except BrokenPipeError:
                    self.get_logger().info("FIFO terminated")

if __name__ == '__main__':
    main()