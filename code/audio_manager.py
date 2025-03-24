import pygame
from support import *

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        # ---------------- GAME SOUNDS -----------------------------
        self.audio = audio_importer('audio') # a variable that holds all the audio files in a dictionary where "audio_importer()" from the 'support.py' file extracts them from the 'audio' folder

        # changing the volume of the sounds
        # self.audio['menu_track'].set_volume(0.1)

    def play_background_music(self, track_name, volume):
        self.audio[track_name].set_volume(volume)
        self.audio[track_name].play(-1)

    def stop_background_music(self):
        for sound_key in self.audio.keys():
            if sound_key == 'menu_track' or sound_key == 'in_game_track':
                sound = self.audio[sound_key]
                sound.stop()

    def play_sound_effect(self, sound_name, volume):
        self.audio[sound_name].set_volume(volume)
        self.audio[sound_name].play()

    def stop_all_sounds(self):
        for sound in self.audio.values():
            sound.stop()