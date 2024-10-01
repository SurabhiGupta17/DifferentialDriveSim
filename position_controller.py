import pygame
import math
import numpy as np
from robot_model import draw_robot, update_robot_state

def run():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    background_color = (0, 0, 0)
    grid_color = (0, 40, 65)
    wheel_color = (0, 150, 225)
    border_color = (0, 100, 175)
    text_color = (255, 255, 255)
    button_color = (100, 100, 100)
    button_hover_color = (150, 150, 150)

    font = pygame.font.Font(pygame.font.match_font('corbel', True), 20)
    small_font = pygame.font.Font(pygame.font.match_font('corbel', True), 16)
    button_font = pygame.font.Font(pygame.font.match_font('corbel', True), 18)

    start_position = [400, 300]
    robot_state = np.array([400, 300, 0])  # [x, y, theta]
    target_position = None  
    trail_positions = []

    # Control parameters
    Ktheta = 0.1
    Kv = 0.005

    r = 0.05  
    s = 0.3 

    dt = 0.1  # Time step 
    elapsed_time = 0
    running = True
    target_reached = False
    target_radius = 40 

    robot_moving = False

    class Button:
        def __init__(self, x, y, width, height, text, callback):
            self.rect = pygame.Rect(x, y, width, height)
            self.text = text
            self.callback = callback
            self.is_hover = False
            self.is_active = False

        def draw(self, screen):
            color = button_hover_color if self.is_hover else button_color
            if self.is_active:
                color = (200, 200, 200)
            pygame.draw.rect(screen, color, self.rect, 0)
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
            text_surface = button_font.render(self.text, True, (255, 255, 255))
            screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

        def handle_event(self, event):
            if event.type == pygame.MOUSEMOTION:
                self.is_hover = self.rect.collidepoint(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.callback()
                    return True
            return False

    def select_target():
        nonlocal selecting_target, target_reached, target_position, robot_moving
        selecting_target = not selecting_target
        select_target_button.is_active = selecting_target
        if selecting_target:
            target_reached = False
            target_position = None
            robot_moving = False

    def start_robot():
        nonlocal robot_moving
        if target_position is not None and not target_reached:
            robot_moving = True

    select_target_button = Button(20, 500, 190, 40, "Select Target Position", select_target)
    start_button = Button(700, 500, 60, 40, "Start", start_robot)
    buttons = [select_target_button, start_button]

    selecting_target = False

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

        rotation_angle = (elapsed_time * velocity * 360 / 60) % 360  

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

    def draw_robot_params(robot_state, target_position, elapsed_time):
        x, y, theta = robot_state

        param_texts = [
            f"Robot: ({int(x)}, {int(y)})",
            f"Time Elapsed: {elapsed_time:.1f}s",
            f"Orientation: {math.degrees(theta):.1f}°"
        ]

        if target_position is not None:
            xD, yD = target_position
            param_texts.insert(1, f"Target: ({int(xD)}, {int(yD)})")
            error_x = xD - x
            error_y = yD - y
            param_texts.append(f"Error (X): {error_x:.2f}")
            param_texts.append(f"Error (Y): {error_y:.2f}")

        for i, text in enumerate(param_texts):
            param_surface = font.render(text, True, text_color)
            screen.blit(param_surface, (20, 20 + i * 30))  

    def normalize_angle(angle):
        return (angle + math.pi) % (2 * math.pi) - math.pi

    def compute_control(robot_state, target_position, Ktheta, Kv, r, s):
        x, y, theta = robot_state
        xD, yD = target_position

        theta_D = math.atan2(yD - y, xD - x)

        # Normalize angle difference
        angle_diff = normalize_angle(theta_D - theta)

        theta_dot = Ktheta * angle_diff
        v = Kv * math.sqrt((xD - x)**2 + (yD - y)**2)

        # Find wheel angular velocities 
        phi_dot_L = (1/r) * v + (-s/(2*r)) * theta_dot
        phi_dot_R = (1/r) * v + (s/(2*r)) * theta_dot

        return phi_dot_L, phi_dot_R, v, theta_dot

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if selecting_target:
                    target_position = np.array(event.pos)
                    selecting_target = False
                    select_target_button.is_active = False
                    target_reached = False
                    robot_moving = False
                else:
                    for button in buttons:
                        result = button.handle_event(event)
                        if result == "back":
                            return "back"
                        if result:
                            break
            else:
                for button in buttons:
                    button.handle_event(event)

        elapsed_time += dt

        if target_position is not None and not target_reached and robot_moving:
            phi_dot_L, phi_dot_R, v, theta_dot = compute_control(robot_state, target_position, Ktheta, Kv, r, s)
    
            time_steps = np.linspace(0, dt, num=2)

            new_state = update_robot_state(robot_state, time_steps, phi_dot_L, phi_dot_R)
            robot_state = new_state[-1]

            trail_positions.append((int(robot_state[0]), int(robot_state[1])))

            distance_to_target = np.linalg.norm(robot_state[:2] - target_position)
            if distance_to_target < target_radius:
                target_reached = True
                robot_moving = False

        screen.fill(background_color)

        draw_grid()

        for pos in trail_positions:
            if isinstance(pos, (list, tuple)) and len(pos) == 2:
                pygame.draw.circle(screen, (255, 255, 255), pos, 2)

        # Draw start box
        pygame.draw.rect(screen, (0, 255, 0), (start_position[0] - 5, start_position[1] - 5, 10, 10))

        draw_robot(screen, robot_state[0], robot_state[1], robot_state[2])

        draw_robot_params(robot_state, target_position, elapsed_time)

        if target_position is not None and robot_moving:
            draw_wheel_rotations(phi_dot_L, phi_dot_R)
        else:
            draw_wheel_rotations(0, 0)

        draw_orientation(robot_state)

        if target_position is not None and not target_reached:
            pygame.draw.rect(screen, (255, 0, 0), (int(target_position[0]) - 5, int(target_position[1]) - 5, 10, 10))

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    return "quit"

if __name__ == "__main__":
    run()