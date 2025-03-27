from src.settings import *
from src.timer import Timer
from src.support import *
from src.particles import *

class TypingTimer:
    def __init__(self, depletion_rate):

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
        self.depletion_rate = depletion_rate
        
        #increasing factor for the bar values
        self.bar_multiplier = 1
        self.bar_multiplier_increment = 0.0001 # increase this value for a faster bar multiplier rate increase

        # particles
        self.particle_list = []

        # out of time check (game over check)
        self.out_of_time = False

    
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
        

        pygame.draw.rect(self.display_surface, COLORS['white'], typing_bar_outline_rect, 3, border_radius = 10) # rect(surface, color, rect, width=0, border_radius=0)
        pygame.draw.rect(self.display_surface, COLORS['white'], typing_bar_filling_rect, border_radius = 10) # rect(surface, color, rect, width=0, border_radius=0)

        # particle effect at the end of the filling bar
        # this variable holds the x coordinate of the right side of the filling bar rect
        right_side_filling_bar_rect_x = typing_bar_filling_rect.right

        # this variable holds the y coordinate of the right side of the filling bar rect (we want the y pos to vary since one specific y point would look to focused on a thick bar)
        right_side_filling_bar_rect_y = self.typing_bar_y + random.randint(-10, 10)

        particle_location = [right_side_filling_bar_rect_x, right_side_filling_bar_rect_y]
        
        self.particles = Particles(self.particle_list, particle_location)

    def reset_typing_timer(self):
        self.current_value = self.max_value

    def constraint(self):
        if self.current_value < 0:
            self.current_value = 0  # prevent going below 0

    def game_over_check(self):
        if self.current_value <= 0:
            self.out_of_time = True

    def update_timer_value(self):
        self.current_value -= self.depletion_rate * self.bar_multiplier
        self.bar_multiplier += self.bar_multiplier_increment
        # print(self.bar_multiplier)

    def update(self):
        self.draw()
        # adjust the depletion rate to account for delta time
        self.update_timer_value()
        self.constraint()
        self.game_over_check()
        self.particles.update()
