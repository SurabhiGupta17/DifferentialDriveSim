import pygame
import math

robot_image = pygame.image.load("assets/robot_model.png")

original_width, original_height = robot_image.get_size()

desired_width = 100  
desired_height = int(desired_width * original_height / original_width)  # Maintain aspect ratio

robot_image = pygame.transform.smoothscale(robot_image, (desired_width, desired_height))

def draw_robot(screen, x, y, theta):
    # Get the dimensions of the scaled image
    width, height = robot_image.get_size()

    # Rotate the image based on the robot's orientation (theta)
    rotated_image = pygame.transform.rotate(robot_image, -math.degrees(theta))

    # Calculate the new image rectangle to maintain its center
    new_rect = rotated_image.get_rect(center=(x, y))

    # Blit (draw) the rotated image to the screen
    screen.blit(rotated_image, new_rect.topleft)
