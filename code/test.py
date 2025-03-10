import pygame
import sys

# Initialize pygame
pygame.init()

# Set up display
width, height = 500, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Depleting Bar Example")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Bar settings
bar_width = 300
bar_height = 30
bar_x = (width - bar_width) // 2
bar_y = height // 2
max_value = 100  # Full value of the bar
current_value = max_value  # Initial value of the bar
depletion_rate = 0.05  # How fast the bar depletes (lower means slower)

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(WHITE)  # Fill the screen with white

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Deplete the bar over time
    current_value -= depletion_rate
    if current_value < 0:
        current_value = 0  # Prevent going below 0

    # Draw the bar
    pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_width, bar_height))  # Outline of the bar
    pygame.draw.rect(screen, RED, (bar_x, bar_y, (bar_width * current_value) / max_value, bar_height))  # Filled portion

    # Update display
    pygame.display.flip()

    # Set the framerate
    clock.tick(60)

# Quit pygame
pygame.quit()
sys.exit()
