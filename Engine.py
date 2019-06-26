#! /usr/bin/python2
import pygame
import copy
from Scripts.Tile import *
from Scripts.Controller import *
from Scripts.GameObject import *
from Scripts.FogLight import *

class Game:
    def __init__(self, width, ratio, background, fps, title, sheet, scale=1):
        self.WIDTH = width*scale
        self.HEIGHT = int(width*ratio)*scale
        self.BACKGROUND = background
        self.RUNNING = True
        self.FPS = fps
        self.TITLE = title
        self.sheet = sheet
        self.controller = Controller(0)
        self.fog_instensity = 0

        pygame.init()
        self.scale = scale
        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        self.render = pygame.Surface((self.WIDTH//scale, self.HEIGHT//scale), pygame.SRCALPHA)
        self.fog = pygame.Surface((self.WIDTH//scale, self.HEIGHT//scale), pygame.SRCALPHA)
        pygame.display.set_caption(self.TITLE)

        self.levents = pygame.event.get()
        self.clock = pygame.time.Clock()
        self.objectlist = []

    def add_object(self, object):
        self.objectlist.append(object)

    def events(self):
        self.levents = pygame.event.get()
        for event in self.levents:
            if event.type == pygame.QUIT:
                self.RUNNING = False
        self.controller.update(self.levents)
        if self.controller.get_press("escape"):
            self.RUNNING = False

    def update(self):
        self.fog.fill((0, 0, 0, self.fog_instensity))
        for i in range(len(self.objectlist)):
            self.objectlist[i].update(self)

    def draw(self):
        self.render.fill(self.BACKGROUND)
        for i in range(len(self.objectlist)):
            self.objectlist[i].draw(self.render)
        self.display.blit(pygame.transform.scale(self.render, (self.WIDTH, self.HEIGHT)), (0, 0))
        self.display.blit(pygame.transform.scale(self.fog, (self.WIDTH, self.HEIGHT)), (0, 0))
        pygame.display.update()
        self.clock.tick(self.FPS)


if __name__ == "__main__":
    game = Game(25*16, 4/5.0, (0, 0, 0), 60, "Pygame Boilerplate", Sheet("bank1.chr"))
    pygame.quit()
    quit()
