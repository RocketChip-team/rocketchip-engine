#! /usr/bin/python2
import pygame
from Scripts.Tile import *

class Game:
    def __init__(self, width, ratio, background, fps, title):
        self.WIDTH = width
        self.HEIGHT = int(width*ratio)
        self.BACKGROUND = background
        self.RUNNING = True
        self.FPS = fps
        self.TITLE = title
        self.sheet = Sheet("bank1.chr")

        pygame.init()
        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(self.TITLE)

        self.levents = pygame.event.get()
        self.clock = pygame.time.Clock()

        while self.RUNNING:
            self.events()
            self.update()
            self.draw()

    def events(self):
        self.levents = pygame.event.get()
        for event in self.levents:
            if event.type == pygame.QUIT:
                self.RUNNING = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.RUNNING = False

    def update(self):
        pass

    def draw(self):
        self.display.fill(self.BACKGROUND)
        pygame.display.update()
        self.clock.tick(self.FPS)


if __name__ == "__main__":
    game = Game(600, 9/16.0, (0, 0, 0), 60, "Pygame Boilerplate")
    pygame.quit()
    quit()
