import pygame

class Player:
    def __init__(self):
        pygame.mixer.init()
        self.current = None

    def load(self, file):
        self.current = file
        pygame.mixer.music.load(file)

    def play(self):
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    def get_pos(self):
        return pygame.mixer.music.get_pos()