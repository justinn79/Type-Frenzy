from settings import *

class Timer:
    def __init__(self, duration, func = None, repeat = None, autostart = False):
        self.duration = duration
        self.start_time = 0
        self.active = False
        self.func = func
        self.repeat = repeat

        if autostart: # by setting autostart, we don't have to call to activate the timer in main.py, it will just automatically start once the Timer instance has been created. ex: calling self.bee_timer.activate() after having self.bee_timer = Timer(2000, func = self.create_bee)
            self.activate()

    def __bool__(self): # this is what is being called if you put this Timer class inside of an if statement.
        return self.active

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0
        if self.repeat: # repeat the timer once the timer has been deactivated / finished.
            self.activate()

    def update(self):
        # print(self.duration)
        if pygame.time.get_ticks() - self.start_time >= self.duration: # once the duration of the timer has been met, execute the following code..
            if self.func and self.start_time != 0: # @ 8:27 doing "self.start_time != 0" because there could be a chance that pygame.time.get_ticks() would be 0 above and trigger the statement to be true.
                self.func() # call the function that is intended to be used with the timer
            self.deactivate() # deactivate the timer, aka reset it.