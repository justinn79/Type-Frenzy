from src.settings import *
import random

class Particles:
    def __init__(self, particle_list, location):

        self.display_surface = pygame.display.get_surface()

        self.particle_list = particle_list
        self.location = location
        self.velocity = [random.randint(0, 20) / 10 - 1, random.randint(-2, 2)] # random.randint(0, 20) / 10 picks a number from 0 to 2 in intervals of 0.1. we do -1 after so that it is a range from -1 to 1. random.randint(-2, 2) is the y value (upwards/downwards velocity)
        self.timer = random.randint(3, 5) # this value is also gonna be the radius of our particle circle. this is because as the time for the particle gets closer to 0 (disappearing), we also want the particle to slowly decrease its size as well.
        # this list will have 3 elements in each element ex: [[location, velocity, timer]]

    def create_particle(self):
        # self.particle_list.append([[location, velocity, timer]])
        self.particle_list.append([self.location, self.velocity, self.timer])

    def draw(self):
        for particle in self.particle_list:
            # particle[0][0] is the particles x coordinate of location
            # particle[1][0] is the particles velocity on the x axis
            # particle[0][1] is the particles y coordinate of location
            # particle[1][1] is the particles velocity on the y axis
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

            x_loc = int(particle[0][0]) # getting the x coordinate of the location
            y_loc = int(particle[0][1]) # getting the y coordinate of the location

            pygame.draw.circle(self.display_surface, COLORS['white'], [x_loc, y_loc], int(particle[2])) # circle(surface, color, center, radius) -> Rect

            # a constraint to remove the particle once the timer hits 0 or below
            if particle[2] <= 0:
                self.particle_list.remove(particle)


    def update(self):
        self.create_particle()
        self.draw()