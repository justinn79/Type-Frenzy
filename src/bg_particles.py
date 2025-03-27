from src.settings import *
from src.support import *
import random

class BgParticles:
    def __init__(self, display_surface):
        
        self.display_surface = display_surface
    
        self.x = random.randint(0, WINDOW_WIDTH)
        self.y = random.randint(0, WINDOW_HEIGHT)

        self.size = random.randint(6, 12)

        self.speed_x = random.uniform(-1, 1)
        self.speed_y = random.uniform(-1, 1)

        self.opacity = random.randint(30, 70)  

    def draw(self):
        
        particle_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA) 

        # draw location of the circle to be at the CENTER of the surface
        draw_loc_x = self.size // 2
        draw_loc_y = self.size // 2
        
        circle_radius = self.size // 2

        particle_surface.set_alpha(self.opacity)

        pygame.draw.circle(particle_surface, COLORS['white'], (draw_loc_x, draw_loc_y), circle_radius)
        
        self.display_surface.blit(particle_surface, (self.x - self.size, self.y - self.size))

    def update(self):
        self.draw()
        self.x += self.speed_x
        self.y += self.speed_y
        
        # particle wrap around the screen
        if self.x < 0: self.x = WINDOW_WIDTH
        if self.x > WINDOW_WIDTH: self.x = 0
        if self.y < 0: self.y = WINDOW_HEIGHT
        if self.y > WINDOW_HEIGHT: self.y = 0
