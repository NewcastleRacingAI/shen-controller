#!/usr/bin/env python3

import pygame
import rclpy
import threading
from rclpy.node import Node

from std_msgs.msg import String, Header
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped, Pose, Point, Quaternion

from enum import Enum

path = Path()

class Sim(Node):

    def __init__(self):
        super().__init__('eufs_sim')
        self.publisher_cones = self.create_publisher(String, '/cones', 10)
        self.publisher_path = self.create_publisher(Path, '/path', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        self.publisher_path.publish(path)
        self.get_logger().info('Publishing: "%s"' % path)
        self.i += 1

class Colour(Enum):
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    RED = (255, 0, 0)

class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        x, y = 30, 60

        self.image = pygame.Surface([15, 30])
        self.image.fill((255, 255, 255))

        pygame.draw.rect(self.image, (255, 255, 255), pygame.Rect(0, 0, 30, 60))

        self.rect = self.image.get_rect()
        self.rect.x=(WIDTH/2) - (x/2)
        self.rect.y=(HEIGHT/2) - (y/2)

class Cone(pygame.sprite.Sprite):
    def __init__(self, colour):
        super().__init__()

        self.image = pygame.Surface([10, 10])
        self.image.fill(colour.value)

        self.colour = colour

        pygame.draw.rect(self.image, colour.value, pygame.Rect(0, 0, 10, 10))

        self.rect = self.image.get_rect()

class Waypoint(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface([10, 10])
        self.image.fill((0, 255, 0))

        pygame.draw.rect(self.image, (0, 255, 0), pygame.Rect(0, 0, 10, 10))

        self.rect = self.image.get_rect()


# Initialize Pygame
pygame.init()

# Initialize Node
rclpy.init()

sim = Sim()
nodeThread = threading.Thread(target=rclpy.spin, args=(sim,))
nodeThread.start()

# Set up the game window

WIDTH, HEIGHT = 800, 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((25,25,25))
pygame.display.set_caption("Sim")

objects = pygame.sprite.Group()
objects.add(Car())

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            match event.button:
                case 1:
                    newcone = Cone(Colour.BLUE)

                    x, y = pygame.mouse.get_pos()

                    newcone.rect.x=x
                    newcone.rect.y=y

                    objects.add(newcone)
                case 2:
                    waypoint = Waypoint()

                    x, y = pygame.mouse.get_pos()

                    waypoint.rect.x=x
                    waypoint.rect.y=y

                    objects.add(waypoint)
                    
                    point = Point()
                    point.x=float(((WIDTH/2) - x)/40)
                    point.y=float(((HEIGHT/2) - y)/40)

                    pose = Pose()
                    pose.position = point

                    poseStamped=PoseStamped()
                    poseStamped.pose=pose

                    path.poses.append(poseStamped)
                case 3:
                    newcone = Cone(Colour.YELLOW)

                    x, y = pygame.mouse.get_pos()

                    newcone.rect.x=x
                    newcone.rect.y=y

                    objects.add(newcone)
    objects.update()
    objects.draw(screen)
    pygame.display.update()

# Quit Pygame
pygame.quit()
sim.destroy_node()
rclpy.shutdown()