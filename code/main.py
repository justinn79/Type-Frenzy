from settings import *
from support import *
from healthbar import *
from typingtimer import *
from screen_flash import *
import random
import math

class Game:
    def __init__(self):
        # setup
        # pygame.init()
        pygame.font.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Tipitype')
        self.clock = pygame.time.Clock()
        self.running = True

        # font
        self.font = pygame.font.Font('fonts/Bungee-Regular.ttf', 30)
        
        # game variables
        self.player_string = ""
        self.can_append_to_player_string = True
        self.player_string_limit = 12
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.submit = ""
        self.submitted = False # bool value to check if the player has submitted an input
        self.number_of_queued_texts = 5
        self.list_of_queued_texts = []
        self.wordlist_index = 0 # this index is used to append the words from the wordlist to the list_of_queued_texts list

        # text shake variables
        self.shake = False
        self.shake_timer = 0

        # game settings
        self.text_rect_size_WIDTH = WINDOW_WIDTH // 3 # the queued and player_input string text rect WIDTH size
        self.text_rect_size_HEIGHT = 50 # the queued and player_input string text rect HEIGHT size

        # groups
        self.all_sprites = pygame.sprite.Group()

        # ------------- GAME SETUP -------------------
        self.load_game()

    def load_game(self):

        # ---------------- WORD LIST --------------------------------------
        # creating the wordlist list
        self.wordlist = read_words_from_file('word_storage/words.txt')
        
        # ------------- WORD LIST SORTING ---------------------
        # sorting the wordlist list
        self.len_indexes = [] # a list to show how many words has a specific length or less (variable below)
        self.length = 1 # value to check how many words in the word list has this specific number of letters
        self.wordlist.sort(key=len) # sorting the word list by the length of each word
        # a for loop to go through the entire word list and sort out their word lengths within the "self.len_indexes" list
        for i in range(len(self.wordlist)):
            if len(self.wordlist[i]) > self.length:
                self.length += 1
                self.len_indexes.append(i)
        self.len_indexes.append(len(self.wordlist)) # appends the maximum length word list at the end of the iteration above

        # initial setup with loading the texts into the list of queued texts list to prepare the game
        while len(self.list_of_queued_texts) < self.number_of_queued_texts:
            self.list_of_queued_texts.append(self.wordlist[self.wordlist_index])
            self.wordlist_index += 1
        # -------------------------------------------------------------------------------------------

        # list of the queued text rectangles to be drawn
        self.queued_text_rects = self.create_queued_text_rects(5, self.text_rect_size_WIDTH, self.text_rect_size_HEIGHT)

        # instances
        self.healthbar = HealthBar()
        self.typingtimer = TypingTimer()
        self.screenflash = ScreenFlash(self.display_surface)

        # ------------ PLAYER INPUT BOX COORDINATES --------------------------
        # creating the coordinates of where the player_string will be displayed on screen (THIS IS USED IN draw_player_input_text())
        self.player_string_surf_x_original = WINDOW_WIDTH // 2
        self.player_string_surf_x = self.player_string_surf_x_original
        self.player_string_surf_y_original = WINDOW_HEIGHT - (WINDOW_HEIGHT // 6)
        self.player_string_surf_y = self.player_string_surf_y_original

            
    def create_queued_text_rects(self, num_rects, rect_width, rect_height):
        rects = []
        spacing = 10  # space between each rectangle

        # region width and region height (the area we want these rectangles to be drawn in)
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
            rect_width = restricted_width  # adjust width to fit the restricted area if it exceeds

        for i in range(num_rects):

            # if it is the last rectangle (the next word for the player to type) then have it look different than the rest
            if (i + 1) == num_rects:
                # create a rectangle surface
                rect = pygame.Surface((rect_width + 25, rect_height), pygame.SRCALPHA) # pygame.SRCALPHA adds transparency in the surface

                # draw rect on the surface
                pygame.draw.rect(rect, COLORS['orange'], rect.get_rect(), border_radius=10) # rect(surface, color, rect, width=0, border_radius=0, border_top_left_radius=-1,

                # rect border properties
                border_color = COLORS['darkorange']
                border_width = 5
            else: # otherwise, normally just make the rectangles like this
                # create a rectangle surface
                rect = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA) # pygame.SRCALPHA adds transparency in the surface

                # draw rect on the surface
                pygame.draw.rect(rect, COLORS['purple'], rect.get_rect(), border_radius=10) # rect(surface, color, rect, width=0, border_radius=0, border_top_left_radius=-1,

                # rect border properties
                border_color = COLORS['darkpurple']
                border_width = 5

            pygame.draw.rect(rect, border_color, rect.get_rect(), border_radius=10, width=border_width)

            # get the rect's position (center horizontally within restricted width and stack vertically)
            text_x = x1 + restricted_width // 2
            text_y = start_y + i * (rect_height + spacing)
            rect_pos = rect.get_frect(center=(text_x, text_y))

            # append the rect and its position to the list
            rects.append((rect, rect_pos, i))
            # print(rect_pos)

        return rects
    
    def draw_queued_text_rects(self, rects):
        for rect, rect_pos, _ in rects:
            self.display_surface.blit(rect, rect_pos)

    def draw_queued_text(self, rects):
        for rect, rect_pos, i in rects:
            #creating the text surf
            queued_text_surf = self.font.render(self.list_of_queued_texts[i], True, COLORS['white'])

            # get the center of the rectangle (rect_pos is the top-left corner of the rectangle)
            rect_center = rect_pos.center
            
            # CHECK THIS FROM HERE ALL THE WAY DOWN 

            # calculate the position for the text (centered inside the rectangle)
            text_x = rect_center[0] - queued_text_surf.get_width() // 2
            text_y = rect_center[1] - queued_text_surf.get_height() // 2

            text_rect = queued_text_surf.get_rect()
            text_rect.center = rect_center  # align the center of the text to the center of the rect

            # pygame.draw.circle(self.display_surface, COLORS['red'], (text_rect.centerx, text_rect.centery), 5) # using this red circle to check location of coordinate

            
            # draw the text
            # if the current queued text matches the last queued text in the list (which is the next text that the player has to input), then make the text pulsate
            if self.list_of_queued_texts[i] == self.list_of_queued_texts[-1]:
                self.draw_pulsating_queued_text(self.list_of_queued_texts[i], (text_rect.centerx, text_rect.centery))
            # otherwise, just blit the text normally
            else:
                self.display_surface.blit(queued_text_surf, (text_x, text_y))

    def draw_pulsating_queued_text(self, text, center_position):

        # initialize frame_count as an attribute of the function if it doesn't exist 
        if not hasattr(self, "frame_count"):
            self.frame_count = 0  # initialize the counter
            # i am using the 'hasattr' method to do a check everytime this 'draw_pulsating_queued_text' function is called to PREVENT 'frame_count' from being overwritten and set back to 0. i want to preserve the value from when it was called to the very end

        # using a sine wave for the pulsating text effect
        scale_factor = 1 + 0.1 * math.sin(self.frame_count * 2 * math.pi / 1000)  # adjust 1000 for speed
        self.scaled_font = pygame.font.Font('fonts/Bungee-Regular.ttf', int(30 * scale_factor))
        text_surface = self.scaled_font.render(text, True, COLORS['white'])

        # text surface dimensions
        text_width = text_surface.get_width()
        text_height = text_surface.get_height()

        # adjusting position to center the text based on its new size
        text_position = (center_position[0] - text_width // 2, center_position[1] - text_height // 2)

        # Draw the text on the screen at the new position
        self.display_surface.blit(text_surface, text_position)

        # incrementing the frame_count value to give it that pulsating effect
        self.frame_count += 20 # edit this value to decrease or increase the speed of the pulse


    def check_user_input(self):
        # capping the length of the player_string so that the user cannot exceed a certain amount
        if len(self.player_string) >= self.player_string_limit:
            self.can_append_to_player_string = False
        else:
            self.can_append_to_player_string = True # this flag is used in the game loop to check whether or not the "player_string" can be added onto or not

        # checks if the next word is equal to the player input string
        if self.list_of_queued_texts[-1] == self.submit and self.submitted:
            # print('correct')
            self.list_of_queued_texts.pop(-1) # remove that word from the list of queued text
            self.player_string = '' # resets the player string to get ready for the next word
            self.typingtimer.reset_typing_timer() # resets the typing timer when the player string is correct
            self.submitted = False # after doing the CORRECT player input check to the queued text, we want to set this back to False so that this if statement doesnt continuously loop
        elif self.list_of_queued_texts[-1] != self.submit and self.submitted:
            print('WRONG')
            self.shake_text(30) # shake the player text if it is wrong
            self.healthbar.losing_hearts(1)
            self.screenflash.screen_flash('red')
            self.submitted = False # after doing the INCORRECT player input check to the queued text, we want to set this back to False so that this if statement doesnt continuously loop

        
    def update_queued_word_list(self):
        if len(self.list_of_queued_texts) < self.number_of_queued_texts:
            self.list_of_queued_texts.insert(0, self.wordlist[self.wordlist_index])
            self.wordlist_index += 1
            # print(self.list_of_queued_texts)

    def shake_text(self, timer=None):
        if timer:
            self.shake = True
            self.shake_timer = timer

        if self.shake:
            if self.shake_timer > 0: # if the shake timer is still above 0, decrement the value by 1 and apply the shake offset
                self.shake_timer -= 1
                self.player_string_surf_x -= random.randint(-2, 2) # shake offset position
                self.player_string_surf_y -= random.randint(-1, 1) # shake offset position

            if self.shake_timer <= 0: # once the shake timer hits 0, put the player text back in its original spot
                self.player_string_surf_x = self.player_string_surf_x_original
                self.player_string_surf_y = self.player_string_surf_y_original
                self.shake = False # set self.shake to false so that this function wont be active again until the player inputs another wrong text (which gives this function another timer value to activate the function)

    def draw_player_input_text(self):

        self.player_string_surf = self.font.render(self.player_string, True, COLORS["white"])

        # getting the rect of the text_surface
        self.player_string_surf_rect = self.player_string_surf.get_frect(center=(self.player_string_surf_x, self.player_string_surf_y))
        
        # background for the player input text
        bg_player_string_rect = pygame.FRect(
            self.player_string_surf_x - self.text_rect_size_WIDTH / 2,  # subtract half the width to center
            self.player_string_surf_y - self.text_rect_size_HEIGHT / 2,  # subtract half the height to center
            self.text_rect_size_WIDTH,
            self.text_rect_size_HEIGHT
        )

        pygame.draw.rect(self.display_surface, COLORS['blue'], bg_player_string_rect, 5, border_radius=10)
        self.display_surface.blit(self.player_string_surf, self.player_string_surf_rect)

    def draw_game(self):
    
        # ------------- Queued text surface and the texts itself-------------------------------
        # drawing the queued text rects
        self.draw_queued_text_rects(self.queued_text_rects)
        # drawing the queued texts on top of the rects above
        self.draw_queued_text(self.queued_text_rects)

        # ----------- Player input text surface -------------------
        self.draw_player_input_text()
        self.shake_text() # if the player gets the input wrong, shake the text

        # ---------------------- Screen flash when player inputs wrong --------------------
        self.screenflash.screen_flash()


    def game_logic(self):
        self.check_user_input()
        self.update_queued_word_list()
        # print(self.wordlist_index)
        
        # updating the instances created
        self.healthbar.update()
        self.typingtimer.update()
    
    # function to repeatedly check for user input
    def typing_input(self, event):
        
        if event.type == pygame.KEYDOWN:

            # handles the lower case letters
            if event.unicode.lower() in self.letters and self.can_append_to_player_string: # if the key that was just pressed is a lower case letter that exists in self.letters, then add that to the player_string string variable
                self.player_string += event.unicode.lower()

            # handles the backspace
            if event.key == pygame.K_BACKSPACE and len(self.player_string) > 0:
                self.player_string = self.player_string[:-1] # this just gets rid of the last character in the "self.player_string" string variable

            # handles the enter or space key
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self.submit = self.player_string
                self.submitted = True

            # handles the escape key
            if event.key == pygame.K_ESCAPE:
                self.player_string = ""

    def run(self):
        while self.running:
            # dt
            dt = self.clock.tick(60)
    
            # event loop
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    self.running = False

                self.typing_input(event)

            # update
            self.all_sprites.update(dt)

            # draw
            self.display_surface.fill(COLORS['background'])
            self.all_sprites.draw(self.display_surface)
            self.draw_game()
            self.game_logic()
            
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()