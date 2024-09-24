import pygame
from robot_model import draw_robot

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

background_color = (234, 216, 177)  # Light beige

robot_x = 400
robot_y = 300
robot_theta = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_color)
    
    draw_robot(screen, robot_x, robot_y, robot_theta)
    
    pygame.display.flip()
    
    clock.tick(30)

pygame.quit()
