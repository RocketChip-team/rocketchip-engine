import pygame


class Collision:
    def __init__(self, coords1, coords2, tag, id):
        self.area = pygame.Rect(0, 0, coords1[0]-coords2[0], coords1[1]-coords2[1]).normalize()
        self.tag = tag
        self.id = id
