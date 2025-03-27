from src.settings import *
from src.support import *

class ScreenFlash:
    def __init__(self, display_surface):
    
        self.display_surface = display_surface

        # ----------------- SCREEN FLASH PROPERTIES ------------------------
        self.flash_duration = 30
        self.flash_timer = self.flash_duration
        self.flashing = False
        self.screen_flash_colour = ''

        self.alpha_value = 60
    

    def screen_flash(self, colour=None):

        if colour:
            self.flashing = True

            if colour == 'red':
                self.color_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                red_color = (255, 60, 60)
                self.color_surface.fill((red_color[0], red_color[1], red_color[2], self.alpha_value))

            if colour == 'green':
                pass

        if self.flashing:
            self.flash_timer -= 1
            self.display_surface.blit(self.color_surface, (0,0))
            if self.flash_timer <= 0:
                self.flashing = False
                self.flash_timer = self.flash_duration