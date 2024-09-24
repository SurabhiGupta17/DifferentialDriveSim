import pygame
import math

# Load and scale the robot image once at the start
robot_image = pygame.image.load("assets/robot_model.png")

# Scale the image to the desired size
original_width, original_height = robot_image.get_size()
desired_width = 100  
desired_height = int(desired_width * original_height / original_width)  # Maintain aspect ratio
robot_image = pygame.transform.smoothscale(robot_image, (desired_width, desired_height))

def draw_robot(screen, x, y, theta):
    # Rotate the image based on the robot's orientation (theta)
    # The angle must be negated to match the coordinate system
    rotated_image = pygame.transform.rotate(robot_image, -math.degrees(theta))

    # Get the rectangle of the rotated image
    new_rect = rotated_image.get_rect(center=(x, y))

    # Blit (draw) the rotated image to the screen
    screen.blit(rotated_image, new_rect.topleft)

