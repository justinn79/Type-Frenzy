from src.settings import *
from src.support import *
import random

class BgParticles:
    def __init__(self, display_surface):
        
        self.display_surface = display_surface
        
        # coordinate positions for the particle circle
        self.x = random.randint(0, WINDOW_WIDTH)
        self.y = random.randint(0, WINDOW_HEIGHT)

        # size of the particle circle
        self.size = random.randint(6, 12)

        # the particle speed
        self.speed_x = random.uniform(-1, 1)
        self.speed_y = random.uniform(-1, 1)


        # particle opacity (transparency) range - 0-255 (lower value for more fade)
        self.opacity = random.randint(30, 70)  

    def draw(self):
        
        particle_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA) #Surface((width, height), flags=0, depth=0, masks=None) -> Surface


        # we want the draw location of the circle to be at the CENTER of the surface. this is to ensure that the circle isnt clipped when drawn on the surface
        draw_loc_x = self.size // 2
        draw_loc_y = self.size // 2
        # we want the circle radius to equal HALF the size of the particle size. this is because we want the value of the RADIUS of the circle (half the diameter of the size we want)
        circle_radius = self.size // 2

        # set the opacity value for the circle
        particle_surface.set_alpha(self.opacity)

        pygame.draw.circle(particle_surface, COLORS['white'], (draw_loc_x, draw_loc_y), circle_radius) # circle(surface, color, center, radius) -> Rect
        
        self.display_surface.blit(particle_surface, (self.x - self.size, self.y - self.size))

    def update(self):
        self.draw()
        # updating the particle position
        self.x += self.speed_x
        self.y += self.speed_y
        
        # wrapping the particles around the screen, so that if it goes out of bounds, we will retain that particle and put it on the other side of the screen (to prevent on creating more)
        if self.x < 0: self.x = WINDOW_WIDTH
        if self.x > WINDOW_WIDTH: self.x = 0
        if self.y < 0: self.y = WINDOW_HEIGHT
        if self.y > WINDOW_HEIGHT: self.y = 0
