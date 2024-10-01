import pygame
import sys
import random
import forward_kinematics
import position_controller

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

BACKGROUND = (238, 247, 255)
BUTTON_COLOR = (205, 232, 229)
BUTTON_HOVER_COLOR = (150, 200, 200)  
TEXT_COLOR = (22, 66, 60)  
DOT_COLOR = (100, 150, 200)

title_font = pygame.font.SysFont('Corbel', 58, bold=True)  
byline_font = pygame.font.SysFont('Corbel', 24)
button_font = pygame.font.SysFont('Corbel', 30)

class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback

    def draw(self, surface, is_hovered):
        color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, TEXT_COLOR, self.rect, 3)
        text_surface = button_font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class Dot:
    def __init__(self):
        self.x = random.randint(0, 800)
        self.y = random.randint(0, 600)
        self.speed = random.uniform(0.5, 2)
        self.angle = random.uniform(0, 2 * 3.14159)

    def move(self):
        self.x += self.speed * pygame.math.Vector2(1, 0).rotate_rad(self.angle).x
        self.y += self.speed * pygame.math.Vector2(1, 0).rotate_rad(self.angle).y
        if self.x < 0 or self.x > 800:
            self.angle = 3.14159 - self.angle
        if self.y < 0 or self.y > 600:
            self.angle = -self.angle

    def draw(self, surface):
        pygame.draw.circle(surface, DOT_COLOR, (int(self.x), int(self.y)), 2.5)

def start_forward_kinematics():
    forward_kinematics.run()

def start_position_controller():
    position_controller.run()

buttons = [
    Button(200, 330, 400, 60, "Forward Kinematics", start_forward_kinematics),
    Button(200, 410, 400, 60, "Position Controller", start_position_controller)
]

dots = [Dot() for _ in range(50)]

def main():
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos() 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for button in buttons:
                button.handle_event(event)

        screen.fill(BACKGROUND)

        for dot in dots:
            dot.move()
            dot.draw(screen)

        title_surface = title_font.render("Differential Drive Sim", True, TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(400, 170))
        screen.blit(title_surface, title_rect)

        byline_surface = byline_font.render("by Surabhi Gupta", True, TEXT_COLOR)
        byline_rect = byline_surface.get_rect(center=(400, 230))
        screen.blit(byline_surface, byline_rect)

        for button in buttons:
            is_hovered = button.is_hovered(mouse_pos)
            button.draw(screen, is_hovered)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
