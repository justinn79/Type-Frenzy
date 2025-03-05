from settings import *
from support import *

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
        self.font = pygame.font.Font(None, 30)

        # game variables
        self.player_string = 'test'
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.submit = ""

        # game settings
        self.text_rect_size_WIDTH = WINDOW_WIDTH // 3 # the upcoming and player_input string text rect WIDTH size
        self.text_rect_size_HEIGHT = 50 # the upcoming and player_input string text rect HEIGHT size

        # groups
        self.all_sprites = pygame.sprite.Group()

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

        # ------------- GAME SETUP -------------------
        self.load_game()

    def load_game(self):
        self.upcoming_text_rects = self.create_upcoming_text_rects(5, self.text_rect_size_WIDTH, self.text_rect_size_HEIGHT)

    def create_upcoming_text_rects(self, num_rects, rect_width, rect_height):
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
            # create a rectangle surface
            rect = pygame.Surface((rect_width, rect_height))
            rect.fill((255, 0, 0))  # Fill with red color

            # Get the rect's position (center horizontally within restricted width and stack vertically)
            rect_pos = rect.get_rect(center=(x1 + restricted_width // 2, start_y + i * (rect_height + spacing)))
            rects.append((rect, rect_pos))

        return rects

    def draw_game(self):
    
        # drawing the upcoming text rects
        for rect, rect_pos in self.upcoming_text_rects:
            self.display_surface.blit(rect, rect_pos)

        # ----------- Player input text surface -------------------

        # creating the coordinates of where the player_string will be displayed on screen
        player_string_surf_x = WINDOW_WIDTH // 2
        player_string_surf_y = WINDOW_HEIGHT - (WINDOW_HEIGHT // 6)

        self.player_string_surf = self.font.render(self.player_string, True, COLORS["white"])

        # getting the rect of the text_surface
        player_string_surf_rect = self.player_string_surf.get_frect(center=(player_string_surf_x, player_string_surf_y))

        # background for the player input text
        bg_player_string_rect = pygame.FRect(
            player_string_surf_x - self.text_rect_size_WIDTH / 2,  # Subtract half the width to center
            player_string_surf_y - self.text_rect_size_HEIGHT / 2,  # Subtract half the height to center
            self.text_rect_size_WIDTH,
            self.text_rect_size_HEIGHT
        )

        pygame.draw.rect(self.display_surface, COLORS['red'], bg_player_string_rect, 1)
        self.display_surface.blit(self.player_string_surf, player_string_surf_rect)
    
    # function to repeatedly check for user input
    def typing_input(self, event):
        
        if event.type == pygame.KEYDOWN:

            # handles the lower case letters
            if event.unicode.lower() in self.letters: # if the key that was just pressed is a lower case letter that exists in self.letters, then add that to the player_string string variable
                self.player_string += event.unicode.lower()

            # handles the backspace
            if event.key == pygame.K_BACKSPACE and len(self.player_string) > 0:
                self.player_string = self.player_string[:-1] # this just gets rid of the last character in the "self.player_string" string variable

            # handles the enter or space key
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self.submit = self.player_string
                self.player_string = ""

    def run(self):
        while self.running:
            # dt
            dt = self.clock.tick() / 1000
    
            # event loop
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    self.running = False

                self.typing_input(event)

            # update
            self.all_sprites.update(dt)

            # draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.display_surface)
            self.draw_game()
            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()