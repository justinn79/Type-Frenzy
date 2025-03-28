from src.settings import *
from src.support import *
from src.healthbar import *
from src.typingtimer import *
from src.screen_flash import *
from src.text_fade import *
from src.bg_particles import *
from src.ui import *
from src.audio_manager import *

import random
import math

class Game:
    def __init__(self, display_surface, audio_manager):
        pygame.init()
        pygame.font.init()

        self.display_surface = display_surface

        # game title and game icon
        self.game_icon = pygame.image.load('assets/images/game_icon/game_icon.ico').convert_alpha()
        pygame.display.set_icon(self.game_icon)
        pygame.display.set_caption('Type Frenzy')

        self.clock = pygame.time.Clock()
        self.running = True

        # background
        self.main_menu_bg = pygame.image.load('assets/images/ui/main_menu_background.png').convert_alpha()

        #----------------AUDIO-------------------------
        self.audio_manager = audio_manager
        self.sound_volume = 0.2
        # storing all the different typing sounds in a dictionary
        self.typing_sounds = {}
        # retrieving only the typing sounds within the audio dictionary and storing it in the typing sounds dictionary above.
        for sound_key, value in self.audio_manager.audio.items():
            if sound_key in ["type_sound1", "type_sound2", "type_sound3", "type_sound4", "type_sound5"]:
                self.typing_sounds[sound_key] = value

        self.font = pygame.font.Font('assets/fonts/Bungee-Regular.ttf', 30)

        # bool variable to check if the player has paused the game
        self.pause_game = False
        self.original_pause_game_state = False
        
        # game variables
        self.player_string = ""
        self.can_append_to_player_string = True
        self.player_string_limit = 12
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.submit = ""
        self.submitted = False
        self.number_of_queued_texts = 5
        self.list_of_queued_texts = []
        self.wordlist_index = 0
        self.combo = 0
        self.highest_combo_value = 0
        self.score = 0
        self.min_word_length = 3
        self.max_word_length = 8

        # changing game variables (game modifier variables)
        # --- Perfect Modifier ------
        self.default_number_of_lives = 4
        self.number_of_lives = self.default_number_of_lives
        # --- Double Time Modifier ------
        self.default_depletion_rate = 0.20
        self.depletion_rate = self.default_depletion_rate

        # variables that are constantly checked/updated (used to check for the game over state)
        self.out_of_lives = False
        self.out_of_time = False

        # text shake variables
        self.shake = False
        self.shake_timer = 0

        # combo text growing variables
        self.pulse_grow = False
        self.pulse_complete = False

        self.growth_rate = 0.1
        self.max_scale = 3
        self.min_scale = 1
        self.grow_scale = 1

        # game settings
        self.text_rect_size_WIDTH = WINDOW_WIDTH // 3
        self.text_rect_size_HEIGHT = 50

        # game modifiers
        self.game_modifiers = [] 

        # game modifier multiplier
        self.game_modifier_multiplier = 1
        # groups
        self.all_sprites = pygame.sprite.Group()

        # -------------- WORD LIST FROM A PRE DEFINED WORD TEXT FILE --------------------------------
        #creating the wordlist list
        self.wordlist = read_words_from_file('assets/word_storage/words.txt')
        # initial setup with loading the texts into the list of queued texts list to prepare the game
        while len(self.list_of_queued_texts) < self.number_of_queued_texts:
            word = random.choice(self.wordlist)
            if self.min_word_length <= len(word) <= self.max_word_length and word.isalpha() and word not in self.list_of_queued_texts:
                self.list_of_queued_texts.append(word)

        # ------------- GAME SETUP -------------------
        # game modifier icon images
        self.icon_scale = 2
        # double time mod icon
        self.double_time_icon = pygame.image.load('assets/images/game_mod_icons/double_time_icon.png').convert_alpha()
        self.double_time_icon = pygame.transform.scale(self.double_time_icon, (self.double_time_icon.get_width() * self.icon_scale, self.double_time_icon.get_height() * self.icon_scale))

        # hidden mod icon
        self.hidden_icon = pygame.image.load('assets/images/game_mod_icons/hidden_icon.png').convert_alpha()
        self.hidden_icon = pygame.transform.scale(self.hidden_icon, (self.hidden_icon.get_width() * self.icon_scale, self.hidden_icon.get_height() * self.icon_scale))

        # perfect mod icon
        self.perfect_icon = pygame.image.load('assets/images/game_mod_icons/perfect_icon.png').convert_alpha()
        self.perfect_icon = pygame.transform.scale(self.perfect_icon, (self.perfect_icon.get_width() * self.icon_scale, self.perfect_icon.get_height() * self.icon_scale))

        self.load_game()
        
    def load_game(self):

        self.queued_text_rects = self.create_queued_text_rects(5, self.text_rect_size_WIDTH, self.text_rect_size_HEIGHT)

        for game_modifier in self.game_modifiers:

            if game_modifier == 'Double Time':
                self.depletion_rate = self.default_depletion_rate * 2
                self.game_modifier_multiplier += 0.25

            if game_modifier == 'Hidden':
                self.game_modifier_multiplier += 0.15

            if game_modifier == 'Perfect':
                self.number_of_lives = 1
                self.game_modifier_multiplier += 0.1

            
        if 'Double Time' not in self.game_modifiers:
            self.depletion_rate = self.default_depletion_rate
        if 'Perfect' not in self.game_modifiers:
            self.number_of_lives = self.default_number_of_lives

        # instances
        self.healthbar = HealthBar(self.number_of_lives)
        self.typingtimer = TypingTimer(self.depletion_rate)
        self.screenflash = ScreenFlash(self.display_surface)
        self.textfade = TextFade()

        self.bg_particles = [BgParticles(self.display_surface) for _ in range(100)]


        # ------------ PLAYER INPUT BOX COORDINATES --------------------------
        # creating the coordinates of where the player_string will be displayed on screen (THIS IS USED IN draw_player_input_text())
        self.input_box = pygame.image.load('assets/images/ui/input_box.png').convert_alpha()
        self.input_box_scaled = pygame.transform.scale(self.input_box, (self.input_box.get_width() * 1.7, self.input_box.get_height() * 1.5))
        self.player_string_surf_x_original = WINDOW_WIDTH // 2
        self.player_string_surf_x = self.player_string_surf_x_original
        self.player_string_surf_y_original = WINDOW_HEIGHT - (WINDOW_HEIGHT // 6)
        self.player_string_surf_y = self.player_string_surf_y_original

    def reset_game(self, display_surface, audio_manager):
        self.__init__(display_surface, audio_manager)

    def reset_pause_game_state(self):
        self.pause_game = self.original_pause_game_state

    # --------------------------------- GAME LOGIC FUNCTIONS------------------------------------------------------------------------------------------#

    def update_queued_word_list_TEXTFILE(self):
        while len(self.list_of_queued_texts) < self.number_of_queued_texts:
            word = random.choice(self.wordlist)
            if self.min_word_length <= len(word) <= self.max_word_length and word.isalpha() and word not in self.list_of_queued_texts:
                self.list_of_queued_texts.insert(0, word)

    def check_user_input(self):
        # capping the length of the player_string so that the user cannot exceed a certain amount
        if len(self.player_string) >= self.player_string_limit:
            self.can_append_to_player_string = False
        else:
            self.can_append_to_player_string = True

        # --------------------------------------------- CORRECT INPUT --------------------------------------------------------
        # checks if the next word is equal to the player input string
        if self.list_of_queued_texts[-1] == self.submit and self.submitted:
            self.calculate_score(self.list_of_queued_texts[-1])
            self.list_of_queued_texts.pop(-1)
            self.player_string = ''
            self.typingtimer.reset_typing_timer()
            self.draw_combo_count(increment=True)
            self.textfade.alpha = 255
            self.submitted = False

        # --------------------------------------------- WRONG INPUT --------------------------------------------------------
        elif self.list_of_queued_texts[-1] != self.submit and self.submitted:
            self.audio_manager.play_sound_effect('combo_break_sound', self.sound_volume)
            self.shake_text(30)

            # health logic
            self.healthbar.losing_hearts(1)

            self.screenflash.screen_flash('red')
            self.draw_combo_count(reset=True)
            self.submitted = False 

    def calculate_score(self, input_score):
        
        if self.combo == 0:
            combo_multiplier = 1
        else:
            combo_multiplier = self.combo

        score_value = len(input_score) * self.game_modifier_multiplier
        self.score += int(score_value * combo_multiplier)
            
    def typing_input(self, event):
        
        if event.type == pygame.KEYDOWN:

            # handles the lower case letters
            if event.unicode.lower() in self.letters and self.can_append_to_player_string:
                # typing sound randomizer
                random_typing_sound_key = random.choice(list(self.typing_sounds.keys()))
                self.audio_manager.play_sound_effect(random_typing_sound_key, self.sound_volume)

                self.player_string += event.unicode.lower()

            # handles the backspace
            if event.key == pygame.K_BACKSPACE and len(self.player_string) > 0:
                self.player_string = self.player_string[:-1]

            # handles the enter or space key
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.player_string != '':
                    self.submit = self.player_string
                    self.submitted = True

            # handles the tab key to erase the players current typed string
            if event.key == pygame.K_TAB:
                self.player_string = ""

            if event.key == pygame.K_ESCAPE:
                self.pause_game = True

    # --------------------------------- GAME DRAWING FUNCTIONS -----------------------------------------------------------------------------------#

    def draw_bg(self):
        self.scaled_main_menu_bg = pygame.transform.scale(self.main_menu_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.scaled_main_menu_bg_rect = self.scaled_main_menu_bg.get_frect(topleft=(0,0))
        self.display_surface.blit(self.scaled_main_menu_bg, self.scaled_main_menu_bg_rect)

    def draw_particle_bg(self):
        for bg_particle in self.bg_particles:
            bg_particle.update()

    def create_queued_text_rects(self, num_rects, rect_width, rect_height):
        rects = []
        spacing = 10

        region_width = WINDOW_WIDTH // 3
        region_height = WINDOW_HEIGHT // 3

        # set the restriction area / calculating x1, y1, x2, y2 to center the region on the screen
        x1 = (WINDOW_WIDTH - region_width) // 2
        y1 = (WINDOW_HEIGHT - region_height) // 2
        x2 = x1 + region_width
        y2 = y1 + region_height


        # define the width and height of the restricted area
        restricted_width = x2 - x1
        restricted_height = y2 - y1

        # calculate the starting Y position for the first rectangle to be centered vertically within the restricted area
        total_height = num_rects * rect_height + (num_rects - 1) * spacing
        start_y = y1 + (restricted_height - total_height) // 2

        # making sure the rectangles do not exceed the width of the restricted area
        if rect_width > restricted_width:
            rect_width = restricted_width

        for i in range(num_rects):

            # if it is the last rectangle (the next word for the player to type) then have it look different than the rest
            if (i + 1) == num_rects:
                rect = pygame.Surface((rect_width + 25, rect_height), pygame.SRCALPHA)

                pygame.draw.rect(rect, COLORS['orange'], rect.get_rect(), border_radius=10)

                border_color = COLORS['darkorange']
                border_width = 5
            else: # otherwise, normally just make the rectangles like this
                rect = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)

                pygame.draw.rect(rect, COLORS['lightblue'], rect.get_rect(), border_radius=10)

                border_color = COLORS['darkblue']
                border_width = 5

            pygame.draw.rect(rect, border_color, rect.get_rect(), border_radius=10, width=border_width)

            # get the rect's position (center horizontally within restricted width and stack vertically)
            text_x = x1 + restricted_width // 2
            text_y = start_y + i * (rect_height + spacing)
            rect_pos = rect.get_frect(center=(text_x, text_y))

            rects.append((rect, rect_pos, i))

        return rects
    
    def draw_queued_text_rects(self, rects):
        for rect, rect_pos, _ in rects:
            self.display_surface.blit(rect, rect_pos)

    def draw_queued_text(self, rects):
        for rect, rect_pos, i in rects:
            queued_text_surf = self.font.render(self.list_of_queued_texts[i], True, COLORS['white'])

            rect_center = rect_pos.center

            text_x = rect_center[0] - queued_text_surf.get_width() // 2
            text_y = rect_center[1] - queued_text_surf.get_height() // 2

            text_rect = queued_text_surf.get_rect()
            text_rect.center = rect_center
            
            if self.list_of_queued_texts[i] == self.list_of_queued_texts[-1]:
                self.draw_pulsating_text(self.list_of_queued_texts[i], (text_rect.centerx, text_rect.centery))
            else:
                self.display_surface.blit(queued_text_surf, (text_x, text_y))

    def draw_pulsating_text(self, text, center_position):

        if not hasattr(self, "frame_count"):
            self.frame_count = 0

        # using a sine wave for the pulsating text effect
        scale_factor = 1 + 0.1 * math.sin(self.frame_count * 2 * math.pi / 1000)
        self.scaled_font = pygame.font.Font('assets/fonts/Bungee-Regular.ttf', int(30 * scale_factor))
        text_surface = self.scaled_font.render(text, True, COLORS['white'])

        text_width = text_surface.get_width()
        text_height = text_surface.get_height()

        text_position = (center_position[0] - text_width // 2, center_position[1] - text_height // 2)

        if 'Hidden' in self.game_modifiers:
            text_surface = self.textfade.fading_text(text_surface)

        self.display_surface.blit(text_surface, text_position)

        self.frame_count += 20

    def draw_player_input_text(self):

        self.player_string_surf = self.font.render(self.player_string, True, COLORS["white"])

        self.player_string_surf_rect = self.player_string_surf.get_frect(center=(self.player_string_surf_x, self.player_string_surf_y))
        
        input_box_rect = self.input_box_scaled.get_frect()
        input_box_rect.center = (self.player_string_surf_rect.centerx, self.player_string_surf_rect.centery)

        self.display_surface.blit(self.input_box_scaled, input_box_rect)
        self.display_surface.blit(self.player_string_surf, self.player_string_surf_rect)

    def shake_text(self, timer=None):
        if timer:
            self.shake = True
            self.shake_timer = timer

        if self.shake:
            if self.shake_timer > 0:
                self.shake_timer -= 1
                self.player_string_surf_x -= random.randint(-2, 2)
                self.player_string_surf_y -= random.randint(-1, 1)

            if self.shake_timer <= 0:
                self.player_string_surf_x = self.player_string_surf_x_original
                self.player_string_surf_y = self.player_string_surf_y_original
                self.shake = False 

    def draw_combo_count(self, increment=None, reset=None):
            
        # --------------------------setting up the combo string before it takes on the grow effect----------------------------

        font_scale = 1
        x_font = pygame.font.Font('assets/fonts/Bungee-Regular.ttf', int(25 * font_scale))
        combo_font = pygame.font.Font('assets/fonts/Bungee-Regular.ttf', int(42 * font_scale))

        x_string_surf = x_font.render("x", True, COLORS["white"])

        combo_string_surf = combo_font.render(str(self.combo), True, COLORS["white"])

        combined_width = x_string_surf.get_width() + combo_string_surf.get_width() + 5
        combined_height = max(x_string_surf.get_height(), combo_string_surf.get_height())
        combined_surface = pygame.Surface((combined_width, combined_height), pygame.SRCALPHA)

        combined_surface.blit(x_string_surf, (0, combined_height - x_string_surf.get_height() - 5))
        combined_surface.blit(combo_string_surf, (x_string_surf.get_width() + 5, 0))
        
        bottomleft_x = WINDOW_WIDTH // 22
        bottomleft_y = WINDOW_HEIGHT - WINDOW_HEIGHT // 16

        if reset:
            self.combo = 0

        if increment:
            self.combo += 1
            if self.combo > self.highest_combo_value:
                self.highest_combo_value = self.combo
            self.pulse_grow = True
            self.grow_scale = 1 
            self.pulse_complete = False
        
        # --------------------------GIVES THE COMBO STRING SURFACE THAT POP GROW EFFECT ------------------------------
        if self.pulse_grow:
            
            # growing phase
            if self.grow_scale < self.max_scale and not self.pulse_complete:
                self.grow_scale += self.growth_rate 

            # once its at max scale, set pulse_complete to true
            if self.grow_scale >= self.max_scale and not self.pulse_complete:
                self.pulse_complete = True

            # shrinking phase
            if self.grow_scale > self.min_scale and self.pulse_complete:
                self.grow_scale -= self.growth_rate

            # once it reaches the min scale and the pulse has been complete, stop the pulse and reset the variables
            if self.grow_scale <= self.min_scale and self.pulse_complete:
                self.grow_scale = 1
                self.pulse_complete = False
                self.pulse_grow = False

            combined_surface = pygame.transform.scale(combined_surface, 
                                            (int(combined_surface.get_width() * self.grow_scale),
                                             int(combined_surface.get_height() * self.grow_scale)))

        combined_rect = combined_surface.get_frect(center=(bottomleft_x, bottomleft_y))
        
        self.display_surface.blit(combined_surface, combined_rect)
            
    def draw_score(self):
        score_text_surf = self.font.render(("Score:"), True, COLORS["white"])

        score_surf = self.font.render(str(self.score), True, COLORS["white"])

        combined_width = score_text_surf.get_width() + score_surf.get_width() + 5
        combined_height = max(score_text_surf.get_height(), score_surf.get_height())
        
        combined_surface = pygame.Surface((combined_width, combined_height), pygame.SRCALPHA)

        
        combined_surface.blit(score_text_surf, (0, 0))
        combined_surface.blit(score_surf, (score_text_surf.get_width() + 5, 0))

        topright_x = WINDOW_WIDTH - 175
        topright_y = 50

        combined_rect = combined_surface.get_frect(center=(topright_x, topright_y))
        
        self.display_surface.blit(combined_surface, combined_rect)
   
    def draw_game_modifiers(self, game_modifier):
        icon_spacing = 70
        for i in range(len(game_modifier)):

            if game_modifier[i] == 'Double Time':
                icon_surf = self.double_time_icon
            if game_modifier[i] == 'Hidden':
                icon_surf = self.hidden_icon
            if game_modifier[i] == 'Perfect':
                icon_surf = self.perfect_icon

            x_loc = self.healthbar.health_bar_region_rect.x + (i * icon_spacing)
            y_loc = self.healthbar.health_bar_region_rect.y + 50
            
            self.display_surface.blit(icon_surf, (x_loc, y_loc))

    # --------------------------------- GAME DRAWING LOOP FUNCTION -----------------------------------------------------------------------------------#

    def draw_game(self):
        self.draw_bg()
        self.draw_particle_bg()
        # -------------queued text surface and the texts itself-------------------------------
        self.draw_queued_text_rects(self.queued_text_rects)
        self.draw_queued_text(self.queued_text_rects)

        # ----------- Player input text surface -------------------
        self.draw_player_input_text()
        self.shake_text()

        self.draw_combo_count()
        self.draw_score()
        self.draw_game_modifiers(self.game_modifiers)

        # ---------------------- Screen flash when player inputs wrong --------------------
        self.screenflash.screen_flash()

    # --------------------------------- GAME LOGIC LOOP FUNCTION------------------------------------------------------------------------------------------#

    def game_logic(self):
        self.check_user_input()
        self.update_queued_word_list_TEXTFILE()
        
        # updating the instances created
        self.healthbar.update()
        self.typingtimer.update()

        # Game Over variable checks
        self.out_of_lives = self.healthbar.out_of_lives
        self.out_of_time = self.typingtimer.out_of_time
    