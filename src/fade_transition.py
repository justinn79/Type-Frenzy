
import pygame
import time

from src.settings import *

class FadeTransition:

    def __init__(self, display_surface):
        
        self.display_surface = display_surface

    def fade_out(self, fade=False):

        fade_surface = pygame.Surface((self.display_surface.width, self.display_surface.height))
        fade_surface.fill(COLORS['black'])

        if fade:
            for alpha in range(0, 255, 5):  
                fade_surface.set_alpha(alpha) 
                self.display_surface.blit(fade_surface, (0, 0))
                pygame.display.update()
                pygame.time.delay(10)
            fade = False

    def fade_in(self, display_surface, fade=False):

        self.screen_copy = pygame.Surface(display_surface.get_size())
        self.screen_copy.blit(display_surface, (0, 0))

        fade_surface = pygame.Surface((self.display_surface.width, self.display_surface.height))
        fade_surface.fill(COLORS['black'])

        if fade:
            for alpha in range(255, 0, -5):

                self.display_surface.blit(self.screen_copy, (0,0))
                
                fade_surface.set_alpha(alpha)
                self.display_surface.blit(fade_surface, (0, 0))
                pygame.display.update()
                pygame.time.delay(10)
            fade = False