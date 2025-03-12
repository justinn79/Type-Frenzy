from settings import *
from support import *

class ScreenFlash:
    def __init__(self, display_surface):
    
        self.display_surface = display_surface

        # ----------------- SCREEN FLASH PROPERTIES ------------------------
        self.flash_duration = 30
        self.flash_timer = self.flash_duration
        self.flashing = False
        self.screen_flash_colour = ''

        self.alpha_value = 60  # alpha value between 0 (fully transparent) and 255 (fully opaque)
    

    def screen_flash(self, colour=None):

        if colour:
            self.flashing = True

            # colour red is for when the player inputs the wrong word
            if colour == 'red':
                # creating a surface for the red flash
                self.color_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                red_color = (255, 60, 60)
                self.color_surface.fill((red_color[0], red_color[1], red_color[2], self.alpha_value))  # set red with transparency

            if colour == 'green':
                pass

        # after setting "self.flashing" to True and creating a color surface for the flash, we want to now count down the timer and blit that color surface to the screen
        if self.flashing:
            self.flash_timer -= 1
            self.display_surface.blit(self.color_surface, (0,0)) # repeatedly blit the flash color surface until the if statement below is met.
            if self.flash_timer <= 0: # checks to see if the timer runs out. if so, set flashing to False to stop the flash
                self.flashing = False
                self.flash_timer = self.flash_duration # resets the flash_timer variable for the next flash