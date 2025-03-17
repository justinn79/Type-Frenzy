
import pygame
import time

from settings import *

class FadeTransition:

    def __init__(self, display_surface):
        
        self.display_surface = display_surface

    def fade_out(self, fade=False):

        # creating the fade surface (the surface that is going to fill the screen during the fade out transition)
        fade_surface = pygame.Surface((self.display_surface.width, self.display_surface.height))
        fade_surface.fill(COLORS['black'])

        if fade:
            for alpha in range(0, 255, 5):  # fading from fully transparent (0) to fully opaque (255) in increments of 5
                fade_surface.set_alpha(alpha) # the alpha value is an integer from 0 to 255, 0 is fully transparent and 255 is fully opaque
                self.display_surface.blit(fade_surface, (0, 0))
                pygame.display.update()
                pygame.time.delay(15)  # change the value to adjust the speed of the fade
            fade = False

    def fade_in(self, display_surface, fade=False):

        self.screen_copy = pygame.Surface(display_surface.get_size()) # creating a screen_copy variable surface with the same dimensions as the display_surface
        self.screen_copy.blit(display_surface, (0, 0)) # retaining the current image of the display surface onto the screen_copy variable (copying its surface)

        # creating the fade surface (the surface that is going to disappear from the screen during the fade in transition)
        fade_surface = pygame.Surface((self.display_surface.width, self.display_surface.height))
        fade_surface.fill(COLORS['black'])

        if fade:
            for alpha in range(255, 0, -5):  # fading from fully opaque (255) to fully transparent (0) in decrements of 5

                self.display_surface.blit(self.screen_copy, (0,0)) # repeatedly blitting the screen_copy image before the fade surface to get the fading effect for fade in
                
                fade_surface.set_alpha(alpha) # the alpha value is an integer from 0 to 255, 0 is fully transparent and 255 is fully opaque
                self.display_surface.blit(fade_surface, (0, 0))
                pygame.display.update()
                pygame.time.delay(15)  # change the value to adjust the speed of the fade
            fade = False