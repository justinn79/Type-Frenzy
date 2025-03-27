from src.settings import *

class TextFade:
    def __init__(self):

        self.alpha = 255
        self.fading_speed = 5

    def fading_text(self, text_surf):
        fade_text_surf = text_surf.copy()

        fade_text_surf.set_alpha(self.alpha)

        self.alpha -= self.fading_speed
        # constraint - to make sure that the alpha value does not go below 0
        if self.alpha < 0:  
            self.alpha = 0
        
        return fade_text_surf
