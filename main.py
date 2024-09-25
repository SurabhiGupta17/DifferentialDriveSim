import pygame
import math
import numpy as np
from robot_model import draw_robot, update_robot_state
from scenarios import going_straight, turning_left, turning_right, accelerating, decelerating, turning_on_the_spot

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

background_color = (234, 216, 177)  # Light beige

# Initial robot state: [x, y, theta]
robot_state = [400, 300, 0]  # Start at the center facing right
robot_speed = float(20)
trail_positions = []

dt = 0.1  # Time step for the simulation
running = True

v_left, v_right = turning_left(robot_speed)
print(f"Initial velocities: v_left={v_left}, v_right={v_right}")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Generate a time array for each step
    time_steps = np.linspace(0, dt, num=2)  # Generate 2 time points for odeint
    
    # Print the current state and velocities before updating
    print(f"Current State: x={robot_state[0]}, y={robot_state[1]}, theta={robot_state[2]}")
    print(f"Time steps: {time_steps}, v_left: {v_left}, v_right: {v_right}")
    
    new_state = update_robot_state(robot_state, time_steps, v_left, v_right)
    
    robot_state = new_state[-1]
    
    trail_positions.append((robot_state[0], robot_state[1]))
    
    screen.fill(background_color)
    
    for pos in trail_positions:
        pygame.draw.circle(screen, (0, 0, 0), (int(pos[0]), int(pos[1])), 2)
    
    draw_robot(screen, robot_state[0], robot_state[1], robot_state[2])
    
    pygame.display.flip()
    
    clock.tick(30)

pygame.quit()