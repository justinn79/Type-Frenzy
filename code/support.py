from settings import *

def read_words_from_file(filename):
        with open(filename, 'r') as file:
            # Read the file and split the contents by whitespace (spaces, newlines, etc.)
            words = file.read().split()
        return words