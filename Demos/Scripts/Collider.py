import pygame
from Scripts.Collision import *


class Collider:
    def __init__(self, offset, size, parent, tags, active=True, tag="default"):
        if parent:
            if hasattr(parent, "x") and hasattr(parent, "y"):
                self.box = pygame.Rect([parent.x+offset[0], parent.y+offset[1]], size)
            else:
                self.box = pygame.Rect(offset, size)
            if hasattr(parent, "tag"):
                self.tag = parent.tag
            else:
                self.tag = tag
        else:
            self.box = pygame.Rect(offset, size)
        self.active = active
        self.parent = parent
        self.tags = tags #tags to collide with

    def detect(self, collider):
        self.box.x = self.parent.x
        self.box.y = self.parent.y
        if self.active and collider.active and collider.tag in self.tags and not collider == self:
            if self.box.colliderect(collider.box):
                return Collision([self.box.x, self.box.y], [collider.box.x, collider.box.y], collider.tag, [id(self), id(collider)])
        return None

    def resolve(self, object):
        pass