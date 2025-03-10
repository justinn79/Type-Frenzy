from settings import *
from timer import Timer
from support import *

class TypingTimer:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        # creating the coordinates of where the typing timer bar will be displayed on screen
        self.typing_bar_x = WINDOW_WIDTH // 2
        self.typing_bar_y = WINDOW_HEIGHT - (WINDOW_HEIGHT // 16)

        # typing timer bar dimensions
        self.bar_width = WINDOW_WIDTH // 2
        self.bar_height = WINDOW_HEIGHT // 30

        # bar values
        self.max_value = 100
        self.current_value = self.max_value
        self.depletion_rate = 40

    
    def draw(self):
        typing_bar_outline_rect = pygame.FRect(  # pygame.FRect(length, top, width, height)
                                        self.typing_bar_x - self.bar_width / 2, # subtract half the width to get the rectangle centered
                                        self.typing_bar_y - self.bar_height / 2,  # subtract half the height to get the rectangle centered
                                        self.bar_width, # width of the bar
                                        self.bar_height) # height of the bar
        
        typing_bar_filling_rect = pygame.FRect(  # pygame.FRect(length, top, width, height)
                                        self.typing_bar_x - self.bar_width / 2, # subtract half the width to get the rectangle centered
                                        self.typing_bar_y - self.bar_height / 2,  # subtract half the height to get the rectangle centered
                                        (self.bar_width * self.current_value) / self.max_value , # width of the bar (changes overtime)
                                        self.bar_height) # height of the bar
        

        pygame.draw.rect(self.display_surface, COLORS['yellow'], typing_bar_outline_rect, 1, border_radius = 10) # rect(surface, color, rect, width=0, border_radius=0)
        pygame.draw.rect(self.display_surface, COLORS['white'], typing_bar_filling_rect, border_radius = 10) # rect(surface, color, rect, width=0, border_radius=0)

        # particle effect at the end of the filling bar

    def reset_typing_timer(self):
        self.current_value = self.max_value

    def constraint(self):
        if self.current_value < 0:
            self.current_value = 0  # prevent going below 0

    def game_over_check(self):
        if self.current_value <= 0:
            print('GAME OVER, TOO SLOW')

    def update(self, dt):
        self.draw()
        # adjust the depletion rate to account for delta time
        self.current_value -= self.depletion_rate * dt
        self.constraint()
        self.game_over_check()
