import pygame
import math
import numpy as np
from scipy.integrate import odeint


# Load and scale the robot image once at the start
robot_image = pygame.image.load("assets/robot_model.png")

# Scale the image to the desired size
original_width, original_height = robot_image.get_size()
desired_width = 100  
desired_height = int(desired_width * original_height / original_width)  # Maintain aspect ratio
robot_image = pygame.transform.smoothscale(robot_image, (desired_width, desired_height))

#Define robot parameters
wheel_radius = 0.05
wheel_base = 0.3

def differential_drive_kinematics(state, t, v_left, v_right):
    x, y, theta = state
    v = (v_left + v_right)/2 * wheel_radius #Linear velocity
    omega = (v_right - v_left)/wheel_base * wheel_radius

    dxdt = v*np.cos(theta)
    dydt = v*np.sin(theta)
    dthetadt = omega

    return [dxdt, dydt, dthetadt]


def update_robot_state(initial_state, t, v_left, v_right):
    return odeint(differential_drive_kinematics, initial_state, t, args=(v_left, v_right)) 


def draw_robot(screen, x, y, theta):
    # Rotate the image based on the robot's orientation (theta)
    rotated_image = pygame.transform.rotate(robot_image, -math.degrees(theta))

    # Get the rectangle of the rotated image
    new_rect = rotated_image.get_rect(center=(x, y))

    # Blit (draw) the rotated image to the screen
    screen.blit(rotated_image, new_rect.topleft)


