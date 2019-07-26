from copy import copy
from Scripts.Tile import *


class GameObject:
    def __init__(self, x, y, sheet, palette, size, animated, tag, behaviours, latency=5, ignore_off_bounds=False):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.animated = animated
        if animated == True:
            self.sprite = AnimatedMetaTile(0, 0, sheet, palette, size, tag, latency, swap=0, flipy=0, flipx=0)
        else:
            indexes = []
            flips = []
            for y in range(0, size[1]):
                for x in range(0, size[0]):
                    indexes.append(0)
                    flips.append(0)
            self.sprite = MetaTile(0, 0, sheet, palette, indexes, flips, size, tag)
        self.colliders = []
        self.collisions = []
        self.oldcollisions = []
        self.controller = None
        self.light = None
        self.behaviours = behaviours
        self.behnames = self.behaviours.keys()
        self.surface = pygame.Surface((size[0]*8, size[1]*8), pygame.SRCALPHA)
        self.tag = tag
        self.ignore_off_bounds = ignore_off_bounds

    def test_collision_stay(self, tag):
        for c in self.collisions:
            if c:
                if c.tag == tag and c in self.oldcollisions:
                    return c
        return None

    def test_collision_enter(self, tag):
        for c in self.collisions:
            if c:
                if c.tag == tag and not c in self.oldcollisions:
                    return c
        return None

    def test_collision_quit(self, tag):
        for c in self.oldcollisions:
            if c:
                if c.tag == tag and not c in self.collisions:
                    return c
        return None

    def add_behaviour(self, name, behaviour):
        self.behaviours[name] = behaviour
        self.behnames.append(name)

    def rem_behaviour(self, name):
        self.behaviours.pop(name)
        self.behnames.remove(name)

    def duplicate(self):
        return copy(self)

    def set_coords(self, coords):
        self.x = coords[0]
        self.y = coords[1]

    def update(self, game):
        if self.controller:
            self.controller.update(game.levents)
        if self.colliders:
            self.oldcollisions = self.collisions
            newcoll = []
            for box in self.colliders:
                for layer in game.objectlist:
                    for obj in layer:
                        if hasattr(obj, "colliders"):
                            for obox in obj.colliders:
                                collision = box.detect(obox)
                                if not collision == None:
                                    newcoll.append(collision)
            r = 0
            for i in range(len(newcoll)):
                for j in range(len(self.collisions)):
                    if newcoll[i-r].id == self.collisions[j].id:
                        newcoll.pop(i)
                        newcoll.append(self.collisions[j])
                    else:
                        pass
            self.collisions = newcoll

        for i in self.behnames:
            exec(self.behaviours[i])
        if self.light:
            self.light.draw(game.fog, game.fog_color)

    def draw(self, surface):
        self.surface.fill((0,0,0,0))
        self.sprite.draw(self.surface)
        surface.blit(self.surface, (self.x, self.y))