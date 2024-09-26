import pygame
import math
import numpy as np
from robot_model import draw_robot, update_robot_state
from scenarios import going_straight, turning_left, turning_right, turning_on_the_spot

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

background_color = (0, 0, 0)
grid_color = (0, 40, 65)
wheel_color = (0, 150, 225)
border_color = (0, 100, 175)
text_color = (255, 255, 255)

font = pygame.font.Font(pygame.font.match_font('corbel', True), 20)
small_font = pygame.font.Font(pygame.font.match_font('corbel', True), 16)

robot_state = [400, 300, 0]  # [x, y, theta]
robot_speed = 20
desired_speed = robot_speed
acceleration = 0
trail_positions = []

dt = 0.1  # Time step 
elapsed_time = 0
running = True

# Initial mode
mode = 'straight'
v_left, v_right = going_straight(robot_speed)

class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.font = pygame.font.Font(pygame.font.match_font('corbel', True), 18)

    def draw(self, screen):
        pygame.draw.rect(screen, (100, 100, 100), self.rect, 0)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

buttons = [
    Button(20, 500, 50, 40, "Left", lambda: 'left'),
    Button(80, 500, 80, 40, "Straight", lambda: 'straight'),
    Button(170, 500, 60, 40, "Right", lambda: 'right'),
    Button(430, 500, 120, 40, "Turn on Spot", lambda: 'turn_on_spot'),
    Button(560, 500, 100, 40, "Accelerate", lambda: 'accelerate'),
    Button(670, 500, 100, 40, "Decelerate", lambda: 'decelerate')
]

def handle_button_click(pos):
    global mode, desired_speed
    for button in buttons:
        if button.is_clicked(pos):
            action = button.callback()
            if action == 'accelerate':
                desired_speed = min(robot_speed + 10, 100) 
            elif action == 'decelerate':
                desired_speed = max(0, robot_speed - 10)  
            else:
                mode = action
            break

def draw_grid():
    for x in range(0, 800, 40):
        pygame.draw.line(screen, grid_color, (x, 0), (x, 600), 1)
    for y in range(0, 600, 40):
        pygame.draw.line(screen, grid_color, (0, y), (800, y), 1)

def draw_wheel_rotations(v_left, v_right):
    left_wheel_center = (450, 80)  
    draw_wheel(screen, left_wheel_center, v_left, "Left")

    right_wheel_center = (550, 80)  
    draw_wheel(screen, right_wheel_center, v_right, "Right")


def draw_wheel(screen, center, velocity, label):
    radius = 30 
    pygame.draw.circle(screen, wheel_color, center, radius, 2) 

    rotation_angle = (elapsed_time * velocity * 360 / 60) % 360  # Proportional rotation

    spoke_x = center[0] + radius * math.cos(math.radians(rotation_angle))
    spoke_y = center[1] + radius * math.sin(math.radians(rotation_angle))
    pygame.draw.line(screen, text_color, center, (spoke_x, spoke_y), 2)

    wheel_text = small_font.render(f"{label}: {velocity:.1f}", True, text_color)
    screen.blit(wheel_text, (center[0] - radius, center[1] + radius + 10))


def draw_orientation(robot_state):
    x, y, theta = robot_state

    center = (700, 80)  
    radius = 50
    pygame.draw.circle(screen, text_color, center, radius, 2) 

    for angle in range(0, 360, 45):
        spoke_angle = math.radians(angle)
        spoke_x = center[0] + radius * math.cos(spoke_angle)
        spoke_y = center[1] + radius * math.sin(spoke_angle)
        pygame.draw.line(screen, text_color, center, (spoke_x, spoke_y), 1)

    theta_angle = theta % (2 * math.pi)
    bold_spoke_x = center[0] + radius * math.cos(theta_angle)
    bold_spoke_y = center[1] + radius * math.sin(theta_angle)
    pygame.draw.line(screen, text_color, center, (bold_spoke_x, bold_spoke_y), 3)  

    orientation_text = font.render("Orientation", True, text_color)
    screen.blit(orientation_text, (center[0] - radius, center[1] + radius + 20))


def draw_robot_params(robot_state, elapsed_time, speed, acceleration):
    x, y, theta = robot_state

    param_texts = [
        f"Robot Coordinates: ({int(x)}, {int(y)})",
        f"Time Elapsed: {elapsed_time:.1f}s",
        f"Speed: {speed:.1f} units/s",
        f"Acceleration: {acceleration:.2f} units/s²"
    ]

    for i, text in enumerate(param_texts):
        param_surface = font.render(text, True, text_color)
        screen.blit(param_surface, (20, 20 + i * 30))  

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button click
                handle_button_click(pygame.mouse.get_pos())  

    elapsed_time += dt

    speed_diff = desired_speed - robot_speed
    if abs(speed_diff) > 0.1: 
        robot_speed += speed_diff * dt  

    if mode == 'straight':
        v_left, v_right = going_straight(robot_speed)
    elif mode == 'left':
        v_left, v_right = turning_left(robot_speed)
    elif mode == 'right':
        v_left, v_right = turning_right(robot_speed)
    elif mode == 'turn_on_spot':
        v_left, v_right = turning_on_the_spot(robot_speed)

    # Generate a time array for each step
    time_steps = np.linspace(0, dt, num=2)

    new_state = update_robot_state(robot_state, time_steps, v_left, v_right)
    robot_state = new_state[-1]

    acceleration = (v_right - v_left) / dt

    trail_positions.append((robot_state[0], robot_state[1]))

    screen.fill(background_color)

    draw_grid()

    for pos in trail_positions:
        pygame.draw.circle(screen, (255, 255, 255), (int(pos[0]), int(pos[1])), 2)

    draw_robot(screen, robot_state[0], robot_state[1], robot_state[2])

    draw_robot_params(robot_state, elapsed_time, robot_speed, acceleration)

    draw_wheel_rotations(v_left, v_right)

    draw_orientation(robot_state)

    for button in buttons:
        button.draw(screen)

    pygame.display.flip()
    clock.tick(30) 

pygame.quit()
