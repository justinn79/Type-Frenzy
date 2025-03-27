from src.settings import *
import random

class Particles:
    def __init__(self, particle_list, location):

        self.display_surface = pygame.display.get_surface()

        self.particle_list = particle_list
        self.location = location
        self.velocity = [random.randint(0, 20) / 10 - 1, random.randint(-2, 2)]
        self.timer = random.randint(3, 5)

    def create_particle(self):
        self.particle_list.append([self.location, self.velocity, self.timer])

    def draw(self):
        for particle in self.particle_list:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]

            # adding onto the vertical velocity to pull the particles down if the particle was initially going up
            if particle[1][1] < 0:
                particle[1][1] += 0.1

            # subtracting the vertical velocity to bring the particles up if the particle was initially going down
            if particle[1][1] > 0:
                particle[1][1] -= 0.1
            
            # counting down on the timer of the particle (we are also decreasing the particles radius here, aka using the same value)
            particle[2] -= 0.1

            x_loc = int(particle[0][0])
            y_loc = int(particle[0][1])

            pygame.draw.circle(self.display_surface, COLORS['white'], [x_loc, y_loc], int(particle[2]))

            # a constraint to remove the particle once the timer hits 0 or below
            if particle[2] <= 0:
                self.particle_list.remove(particle)


    def update(self):
        self.create_particle()
        self.draw()