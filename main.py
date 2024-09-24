import pygame
import math
from robot_model import draw_robot  

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

background_color = (234, 216, 177)  # Light beige

robot_x = 400
robot_y = 300
robot_theta = 0  # Start facing to the right (0 radians)
robot_speed = 2

trail_positions = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:  # Move forward
        robot_x += robot_speed * math.cos(robot_theta)
        robot_y += robot_speed * math.sin(robot_theta)
        
        trail_positions.append((robot_x, robot_y))

    if keys[pygame.K_DOWN]:  # Move backward
        robot_x -= robot_speed * math.cos(robot_theta)
        robot_y -= robot_speed * math.sin(robot_theta)
        
        trail_positions.append((robot_x, robot_y))

    if keys[pygame.K_LEFT]:  # Rotate left
        robot_theta -= 0.1 

    if keys[pygame.K_RIGHT]:  # Rotate right
        robot_theta += 0.1  

    screen.fill(background_color)

    for pos in trail_positions:
        pygame.draw.circle(screen, (0, 0, 0), (int(pos[0]), int(pos[1])), 2)

    draw_robot(screen, robot_x, robot_y, robot_theta)

    pygame.display.flip()
    
    clock.tick(30)

pygame.quit()
