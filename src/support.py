from src.settings import *

def read_words_from_file(filename):
        with open(filename, 'r') as file:
            # Read the file and split the contents by whitespace (spaces, newlines, etc.)
            words = file.read().split()
        return words

def audio_importer(*path):
    audio_dict = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            full_path = join(folder_path, file_name)
            audio_dict[file_name.split('.')[0]] = pygame.mixer.Sound(full_path)
    return audio_dict