import pygame
import sys

pygame.init()

# Set up display dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Text Display Example")

# Initialize the font module
pygame.font.init()

# Set up font
font = pygame.font.Font(None, 36)

# Define the text with newlines
multiline_text = "Hello, Pygame!\nThis is a new line.\nAnd another one."

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    screen.fill((0, 0, 0))

    # Split the multiline text into lines
    lines = multiline_text.split('\n')

    y_offset = height // 2 - len(lines) * font.get_height() // 2

    # Render and blit each line
    for line in lines:
        text_surface = font.render(line, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.centerx = width // 2
        text_rect.y = y_offset
        screen.blit(text_surface, text_rect)
        y_offset += font.get_height()

    # Update the display
    pygame.display.flip()
