from settings import *
from timer import Timer
from support import *

class HealthBar:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.font = pygame.font.Font('fonts/Bungee-Regular.ttf', 25)

        # full heart image
        self.scale = 2.5
        self.heart_image = pygame.image.load('images/healthbar/fullheart.png').convert_alpha()
        self.heart_image_scaled = pygame.transform.scale(self.heart_image, (self.heart_image.get_width() * self.scale, self.heart_image.get_height() * self.scale))
        self.heart_image_scaled_HEIGHT = self.heart_image_scaled.get_height()
        self.heart_image_scaled_WIDTH = self.heart_image_scaled.get_width()

        # empty heart image
        self.scale = 2.5
        self.empty_heart_image = pygame.image.load('images/healthbar/emptyheart.png').convert_alpha()
        self.empty_heart_image_scaled = pygame.transform.scale(self.empty_heart_image, (self.empty_heart_image.get_width() * self.scale, self.empty_heart_image.get_height() * self.scale))
        self.empty_heart_image_scaled_HEIGHT = self.empty_heart_image_scaled.get_height()
        self.empty_heart_image_scaled_WIDTH = self.empty_heart_image_scaled.get_width()

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

        # heart spacing offset
        self.heart_offset_spacing = 10
        self.added_heart_spacing = self.number_of_hearts_total * self.heart_offset_spacing # this will be added onto the health_bar_region_WIDTH to accomodate for the spacing in between each heart

        # health bar region dimensions
         # we are multiplying these two values below because the region width depends on how many hearts the player has. we are also adding the heart spacing from above
        self.health_bar_region_WIDTH = (self.heart_image_scaled_WIDTH * self.number_of_hearts_total) + self.added_heart_spacing + self.heart_offset_spacing
        self.health_bar_region_HEIGHT = WINDOW_HEIGHT // 18

    def draw(self):
        # --------------------- DRAWING THE HEARTS/LIVES -----------------------------------
        health_bar_region_rect = pygame.FRect(self.left, self.top, self.health_bar_region_WIDTH, self.heart_image_scaled_HEIGHT) # pygame.FRect(length, top, width, height)
        pygame.draw.rect(self.display_surface, COLORS['purple'], health_bar_region_rect, 0, self.border_radius) # rect(surface, color, rect, width=0, border_radius=0)

        # drawing the empty hearts under the full hearts
        for i in range(self.number_of_hearts_total):
            # we are adding (i * self.heart_image_scaled_WIDTH) to make sure that for every heart, it is being spaced by the same amount of pixels as their width.
            # additionally, self.heart_offset_spacing is being added to space each heart apart with its value
            x_cord = self.left + (i * (self.heart_image_scaled_WIDTH + self.heart_offset_spacing)) + self.heart_offset_spacing 
            y_cord = self.top
            empty_heart_image_rect = self.empty_heart_image_scaled.get_frect(topleft=(x_cord, y_cord)) # pygame.FRect(length, top, width, height)
            self.display_surface.blit(self.empty_heart_image_scaled, empty_heart_image_rect)

        # ------------------------- 'LIVES' text above the hearts --------------------------------------
        # 'lives' text surf
        lives_text_surf = self.font.render('LIVES', True, COLORS["white"])
        # getting the rect of the 'lives' text surface
        lives_text_rect = lives_text_surf.get_frect(center=(health_bar_region_rect.x + (health_bar_region_rect.width / 3), health_bar_region_rect.centery - 35)) # (health_bar_region_rect.x + (health_bar_region_rect.width / 3) places it a third of the way down the width of the bar
        self.display_surface.blit(lives_text_surf, lives_text_rect)

        # drawing the full hearts
        for i in range(self.number_of_hearts_variable):
            # we are adding (i * self.heart_image_scaled_WIDTH) to make sure that for every heart, it is being spaced by the same amount of pixels as their width.
            # additionally, self.heart_offset_spacing is being added to space each heart apart with its value
            x_cord = self.left + (i * (self.heart_image_scaled_WIDTH + self.heart_offset_spacing)) + self.heart_offset_spacing 
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

