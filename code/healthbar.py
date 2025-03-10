from settings import *
from timer import Timer
from support import *

class HealthBar:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.font = pygame.font.Font('fonts/Bungee-Regular.ttf', 25)

        # Heart image
        self.scale = 2.5
        self.heart_image = pygame.image.load('images/healthbar/fullheart.png').convert_alpha()
        self.heart_image_scaled = pygame.transform.scale(self.heart_image, (self.heart_image.get_width() * self.scale, self.heart_image.get_height() * self.scale))
        self.heart_image_scaled_HEIGHT = self.heart_image_scaled.get_height()
        self.heart_image_scaled_WIDTH = self.heart_image_scaled.get_width()

        # health bar location
        self.left = WINDOW_WIDTH // 22
        self.top = WINDOW_HEIGHT // 18

        # health bar visuals
        self.border_radius = 10

        # offset spacing for each placement of the heart image
        # self.heart_image_offset_spacing = 30

        # number of hearts / the number of lives
        self.number_of_hearts_total = 4
        self.number_of_hearts_variable = self.number_of_hearts_total

        # health bar region dimensions
        self.health_bar_region_WIDTH = (self.heart_image_scaled_WIDTH * self.number_of_hearts_total) # we are multiplying these two values because the region width depends on how many hearts the player has
        self.health_bar_region_HEIGHT = WINDOW_HEIGHT // 18

    def draw(self):
        health_bar_region_rect = pygame.FRect(self.left, self.top, self.health_bar_region_WIDTH, self.heart_image_scaled_HEIGHT) # pygame.FRect(length, top, width, height)
        pygame.draw.rect(self.display_surface, COLORS['purple'], health_bar_region_rect, 0, self.border_radius) # rect(surface, color, rect, width=0, border_radius=0)

        for i in range(self.number_of_hearts_variable):
            x_cord = self.left + (i * self.heart_image_scaled_WIDTH) # we are adding this to make sure that for every heart, it is being spaced by the same amount of pixels as their width.
            y_cord = self.top
            heart_image_rect = self.heart_image_scaled.get_frect(topleft=(x_cord, y_cord)) # pygame.FRect(length, top, width, height)
            self.display_surface.blit(self.heart_image_scaled, heart_image_rect)

    def losing_hearts(self, amount):
        self.number_of_hearts_variable -= amount

    def check_out_of_hearts(self):
        if self.number_of_hearts_variable == 0:
            print('GAME OVER, NO MORE LIVES')

    def update(self):
        self.draw()
        self.check_out_of_hearts()


# # BACKGROUND health bar
# BACKGROUND_health_bar_rect = pygame.FRect(self.left, self.top, self.BACKGROUND_health_bar_WIDTH, self.BACKGROUND_health_bar_HEIGHT) # pygame.FRect(length, top, width, height)
# pygame.draw.rect(self.display_surface, COLORS['black'], BACKGROUND_health_bar_rect, 0, self.border_radius) # rect(surface, color, rect, width=0, border_radius=0)


# # Variable health bar
# VARIABLE_health_bar_rect = pygame.FRect(self.left, self.top, self.health_bar_WIDTH, self.health_bar_HEIGHT) # pygame.FRect(length, top, width, height)
# pygame.draw.rect(self.display_surface, COLORS['red'], VARIABLE_health_bar_rect, 0,  self.border_radius)  # rect(surface, color, rect, width=0, border_radius=0)

# # adding a white shine effect: a gradient looking shine across the top of the health bar
# # shine_rect = pygame.FRect(self.left, self.top, self.health_bar_WIDTH, self.health_bar_HEIGHT)
# shine_surface = pygame.Surface((self.health_bar_WIDTH, self.health_bar_HEIGHT), pygame.SRCALPHA)


# # Health bar BACKGROUND
# self.BACKGROUND_health_bar_WIDTH = WINDOW_WIDTH // 4 + self.health_bar_offset
# self.BACKGROUND_health_bar_HEIGHT = WINDOW_HEIGHT // 18 + self.health_bar_offset

# # full hp size of health (reference variable)
# self.full_health = self.BACKGROUND_health_bar_WIDTH - self.health_bar_offset

# # Variable size of the health (when depleting/gaining)
# self.health_bar_WIDTH = self.BACKGROUND_health_bar_WIDTH - self.health_bar_offset
# self.health_bar_HEIGHT = self.BACKGROUND_health_bar_HEIGHT - self.health_bar_offset

# # Decrement values for the health bar
# self.health_bar_DECREMENT = self.health_bar_WIDTH / 3

# # increment values for the health bar
# self.health_bar_INCREMENT = self.health_bar_WIDTH / 3

