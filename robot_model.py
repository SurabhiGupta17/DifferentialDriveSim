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
wheel_base = 3

def differential_drive_kinematics(state, t, v_left, v_right):
    x, y, theta = state
    v = (v_left + v_right)/2  #Linear velocity
    omega = (v_right - v_left)/wheel_base 
    print(f"t={t:.2f}, v_left: {v_left}, v_right: {v_right}, v: {v}, omega: {omega}")
    dxdt = v*np.cos(theta)
    dydt = v*np.sin(theta)
    dthetadt = omega
    print(f"State: x={x}, y={y}, theta={theta}, v={v}, omega={omega}")
    print(f"dxdt={dxdt}, dydt={dydt}, dthetadt={dthetadt}")

    return [dxdt, dydt, dthetadt]


def update_robot_state(initial_state, t, v_left, v_right):
    print(f"Initial State: {initial_state}")
    print(f"Time: {t}, v_left: {v_left}, v_right: {v_right}")
    new_state = odeint(differential_drive_kinematics, initial_state, t, args=(v_left, v_right))
    
    # Print the new state after integration
    print("New State after integration:")
    for idx, state in enumerate(new_state):
        print(f"Time: {t[idx]:.2f}, State: x={state[0]}, y={state[1]}, theta={state[2]}")
    
    return new_state

def draw_robot(screen, x, y, theta):
    print(f"Drawing Robot at x={x}, y={y}, theta={theta}")
    # Rotate the image based on the robot's orientation (theta)
    rotated_image = pygame.transform.rotate(robot_image, -math.degrees(theta))

    # Get the rectangle of the rotated image
    new_rect = rotated_image.get_rect(center=(x, y))

    # Blit (draw) the rotated image to the screen
    screen.blit(rotated_image, new_rect.topleft)


