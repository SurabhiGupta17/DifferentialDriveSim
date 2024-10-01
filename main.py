import pygame
import sys
import forward_kinematics
import position_controller

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Colors
BACKGROUND = (0, 0, 0)
BUTTON_COLOR = (0, 100, 200)
TEXT_COLOR = (255, 255, 255)

font = pygame.font.Font(None, 36)

class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback

    def draw(self, surface):
        pygame.draw.rect(surface, BUTTON_COLOR, self.rect)
        text_surface = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

def start_forward_kinematics():
    forward_kinematics.run()

def start_position_controller():
    position_controller.run()

buttons = [
    Button(200, 200, 400, 80, "Forward Kinematics", start_forward_kinematics),
    Button(200, 350, 400, 80, "Position Controller", start_position_controller)
]

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for button in buttons:
                button.handle_event(event)

        screen.fill(BACKGROUND)
        for button in buttons:
            button.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()