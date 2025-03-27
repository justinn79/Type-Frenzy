from src.settings import *

class TextFade:
    def __init__(self):

        self.alpha = 255 # alpha value starts at 255 (fully opaque / visible)
        self.fading_speed = 5

    def fading_text(self, text_surf):
        fade_text_surf = text_surf.copy() # creating a new surface for the text surf

        # setting the alpha for the fade text surf
        fade_text_surf.set_alpha(self.alpha)

        # decreasing the alpha value overtime (creating that fade effect)
        self.alpha -= self.fading_speed
        if self.alpha < 0:  # constraint - to make sure that the alpha value does not go below 0
            self.alpha = 0
        
        return fade_text_surf
