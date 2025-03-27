from src.settings import *
from src.timer import Timer
from src.support import *

class HealthBar:
    def __init__(self, number_of_lives):

        self.display_surface = pygame.display.get_surface()

        self.font = pygame.font.Font('assets/fonts/Bungee-Regular.ttf', 25)

        self.out_of_lives = False

        # full heart image
        self.scale = 2.5
        self.heart_image = pygame.image.load('assets/images/healthbar/fullheart.png').convert_alpha()
        self.heart_image_scaled = pygame.transform.scale(self.heart_image, (self.heart_image.get_width() * self.scale, self.heart_image.get_height() * self.scale))
        self.heart_image_scaled_HEIGHT = self.heart_image_scaled.get_height()
        self.heart_image_scaled_WIDTH = self.heart_image_scaled.get_width()

        # empty heart image
        self.scale = 2.5
        self.empty_heart_image = pygame.image.load('assets/images/healthbar/emptyheart.png').convert_alpha()
        self.empty_heart_image_scaled = pygame.transform.scale(self.empty_heart_image, (self.empty_heart_image.get_width() * self.scale, self.empty_heart_image.get_height() * self.scale))
        self.empty_heart_image_scaled_HEIGHT = self.empty_heart_image_scaled.get_height()
        self.empty_heart_image_scaled_WIDTH = self.empty_heart_image_scaled.get_width()

        # health bar location
        self.left = WINDOW_WIDTH // 22
        self.top = WINDOW_HEIGHT // 18

        self.border_radius = 10

        # number of hearts / the number of lives
        self.number_of_hearts_total = number_of_lives
        self.number_of_hearts_variable = self.number_of_hearts_total

        # heart spacing offset
        self.heart_offset_spacing = 10
        self.added_heart_spacing = self.number_of_hearts_total * self.heart_offset_spacing

        # health bar region dimensions
        self.health_bar_region_WIDTH = (self.heart_image_scaled_WIDTH * self.number_of_hearts_total) + self.added_heart_spacing + self.heart_offset_spacing
        self.health_bar_region_HEIGHT = WINDOW_HEIGHT // 18

        # health bar rect
        self.health_bar_region_rect = pygame.FRect(self.left, self.top, self.health_bar_region_WIDTH, self.heart_image_scaled_HEIGHT)

    def draw(self):
        # --------------------- DRAWING THE HEARTS/LIVES -----------------------------------
        pygame.draw.rect(self.display_surface, COLORS['darkgray'], self.health_bar_region_rect, 0, self.border_radius)

        # drawing the empty hearts under the full hearts
        for i in range(self.number_of_hearts_total):
            x_cord = self.left + (i * (self.heart_image_scaled_WIDTH + self.heart_offset_spacing)) + self.heart_offset_spacing 
            y_cord = self.top
            empty_heart_image_rect = self.empty_heart_image_scaled.get_frect(topleft=(x_cord, y_cord))
            self.display_surface.blit(self.empty_heart_image_scaled, empty_heart_image_rect)

        # ------------------------- 'LIVES' text above the hearts --------------------------------------
        lives_text_surf = self.font.render('LIVES', True, COLORS["white"])

        lives_text_rect = lives_text_surf.get_frect(center=(self.health_bar_region_rect.x + (lives_text_surf.get_width() / 2), self.health_bar_region_rect.centery - 35))
        self.display_surface.blit(lives_text_surf, lives_text_rect)

        # drawing the full hearts
        for i in range(self.number_of_hearts_variable):
            x_cord = self.left + (i * (self.heart_image_scaled_WIDTH + self.heart_offset_spacing)) + self.heart_offset_spacing 
            y_cord = self.top
            heart_image_rect = self.heart_image_scaled.get_frect(topleft=(x_cord, y_cord))
            self.display_surface.blit(self.heart_image_scaled, heart_image_rect)

    def losing_hearts(self, amount):
        self.number_of_hearts_variable -= amount

    def check_out_of_hearts(self):
        if self.number_of_hearts_variable == 0:
            self.out_of_lives = True

    def update(self):
        self.draw()
        self.check_out_of_hearts()

