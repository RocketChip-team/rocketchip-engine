#!/usr/bin/python3
# This sript will manage projects
import sys
import os
import platform
import datetime
import subprocess

# TODO: setup data from a json or xml file
project_name = "Test Project"
project_version = "v 0.1"
is_project_tested = "\033[31;1mNo\033[33;0m"
is_project_debug = "\033[31;1mTrue\033[33;0m"
project_name="Test"

#Content of file needed for a RocketChipEngine project :

Engine = """#! /usr/bin/python3
from Scripts.Controller import *
from Scripts.GameObject import *
from Scripts.FogLight import *

class Game:
    def __init__(self, width, ratio, background, fps, title, sheet, scale=1, gravity=0):
        self.width = width
        self.height = int(width*ratio)
        self.WIDTH = self.width * scale
        self.HEIGHT = self.height * scale
        self.BACKGROUND = background
        self.RUNNING = True
        self.FPS = fps
        self.TITLE = title
        self.sheet = sheet
        self.controller = Controller(0)
        self.fog_instensity = 0
        self.gravity = gravity

        pygame.init()
        self.scale = scale
        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        self.render = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.fog = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
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
"""

Controller = """#! /usr/bin/python3
class Controller:#key input manager, it can allow for object control assignement, easier multiplayer, ect.
    def __init__(self, id):#initialization, id is mostly for recognizing different key maps
        self.id = id#identifiers
        self.controls = {"up":[273, -1], "down":[274, -1], "left":[276, -1], "right":[275, -1], "return":[13, -1], "escape":[27, -1]}
        #controlled keys, in the format : [key, timestamp] where the timestamp records how long a key has been pressed,
        #if it is just pressed, it was just released or simply not pressed at the time.
        self.controltags = ["up", "down", "left", "right", "return", "escape"]
        #this keeps track of all the keys in self.controls, so that humans can put actual name on it
        #and increase code readability

    def bind(self, name, key):#this can bind a new key into the controller, that way you can add keys
        self.controls[name] = [key, -1]#add a new key in the self.control, by default being unheld
        self.controltags.append(name)#add the given key name in the self.controltags, allowing it to be
        #updated each self.update() call, more on that later

    def unbind(self, name):#unbind the given key name (or index)
        if name.__class__.__name__ == "str":#if the key is given by name
            self.controls.pop(name)
            self.controltags.remove(name)
        if name.__class__.__name__ == "int":#if the key is given by index
            self.controls.pop(self.controltags[name])
            self.controltags.pop(name)

    def update(self, events):#update the keys' states with a given "pygame.EventList" object
        for event in events:#for each event in the given list
            #event types are checked in int so that we don't have to import the pygame library for this class

            if event.type == 2:#if the event's type corresponds to a button press
                for key in self.controltags:#checks each key in self.control if it is the pressed key
                    if event.key == self.controls[key][0]:#if it is:
                        self.controls[key][1] = 0#then we set it in the "just pressed" state

            if event.type == 3:#if the event's type corresponds to a button release
                for key in self.controltags:#checks each key in self.control if it is the released key
                    if event.key == self.controls[key][0]:#if it is:
                        self.controls[key][1] = -3#then we set it in the "just released" state

        for key in self.controltags:#then the function updates each key's hold time
            if self.controls[key][1] < -1:#if the key is in "just released" state:
                self.controls[key][1] += 1#then we set the key in the "released" state

            if self.controls[key][1] >= 0:#if the key is in "just pressed" state:
                self.controls[key][1] += 1#then we set the key in the "pressed" state

    def get_press(self, name):#we get if a key is in the "just pressed" state, by name or index
        if name.__class__.__name__ == 'str':#if the key is given by name
            if self.controls[name][1] == 1:#return True if it is just pressed
                return True
        elif name.__class__.__name__ == 'int':#if the key is given by index
            if self.controls[self.controltags[name]][1] == 1:#return True is it is just pressed
                return True
        return False#or if it isn't, then we return False

    def get_hold(self, name):#we get if a key is in the "pressed" state, by name or index
        if name.__class__.__name__ == 'str':#if the key is given by name
            if self.controls[name][1] > 1:#return True is it is pressed
                return True
        elif name.__class__.__name__ == 'int':#if the key is given by index
            if self.controls[self.controltags[name]][1] > 1:#return True is it is pressed
                return True
        return False#or if it isn't, then we return False

    def get_unpress(self, name):#we get if a key is in the "just released" state, by name or index
        if name.__class__.__name__ == 'str':#if the key is given by name
            if self.controls[name][1] == -2:#return True is it is just released
                return True
        elif name.__class__.__name__ == 'int':#if the key is given by index
            if self.controls[self.controltags[name]][1] == -2:#return True is it is just released
                return True
        return False#or if it isn't, then we return False

    def get_unhold(self, name):#we get if a key is in the "released" state, by name or index
        if name.__class__.__name__ == 'str':
            if self.controls[name][1] == -1:
                return True
        elif name.__class__.__name__ == 'int':
            if self.controls[self.controltags[name]][1] == -1:
                return True
        return False#or if it isn't, then we return False

    def get_time_hold(self, name):#we get the number of frames a key has been held
        if name.__class__.__name__ == 'str':#if the key is given by name
            if self.controls[name][1] > -1:#if the value isn't a "key" value
                return self.controls[name][1]#we return the hold time
        elif name.__class__.__name__ == 'int':#if the key is given by index
            if self.controls[self.controltags[name]][1] > -1:#if the value isn't a "key" value
                return self.controls[self.controltags[name]][1]#we return the hold time
        return 0#or the hold value isn't a "key" value, then we return 0

    def get_bind_name(self, id):#return a name by index
        return self.controltags[id]

    def get_bind_id(self, name):#return an index by name
        try:
            return self.controltags.index(name)
        except:
            return -1

if __name__ == "__main__":#demonstration code, not commented
    import pygame
    pygame.init()
    scr = pygame.display.set_mode((20, 20))
    control = Controller(0)
    control.unbind("up")
    control.bind("0", pygame.K_0)
    run = True
    clk = pygame.time.Clock()
    frames = 0
    while run:
        frames += 1
        control.update(pygame.event.get())
        print("FRAME " + str(frames) + ":")
        for i in range(len(control.controltags)):
            if control.get_press(i):
                print(" "+control.get_bind_name(i)+" was just pressed")
            elif control.get_hold(i):
                print(" " + control.get_bind_name(i) + " has been held for "+str(control.get_time_hold(i))+" frames")
            elif control.get_unpress(i):
                print(" "+control.get_bind_name(i)+" was just released")
            elif control.get_unhold(i):
                print(" "+control.get_bind_name(i)+" is currently released")
            if control.get_bind_name(i) == "escape":
                if control.get_press(i):
                    run = False
        clk.tick(10)
"""

GameObject = """#! /usr/bin/python3
from copy import copy
from Scripts.Tile import *


class GameObject:
    def __init__(self, x, y, sheet, palette, size, animated, tag, behaviours, latency=5):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.animated = animated
        if animated == True:
            self.sprite = AnimatedMetaTile(0, 0, sheet, palette, size, "p", latency, swap=0, flipy=0, flipx=0)
        else:
            indexes = []
            flips = []
            for y in range(0, size[1]):
                for x in range(0, size[0]):
                    indexes.append(0)
                    flips.append(0)
            self.sprite = MetaTile(0, 0, sheet, palette, indexes, flips, size, tag)
        self.colliders = []
        self.controller = None
        self.light = None
        self.behaviours = behaviours
        self.behnames = self.behaviours.keys()
        self.surface = pygame.Surface((size[0]*8, size[1]*8), pygame.SRCALPHA)

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
            self.colliders.update(game)
        for i in self.behnames:
            exec(self.behaviours[i])
        if self.light:
            self.light.draw(game.fog)

    def draw(self, surface):
        self.surface.fill((0,0,0,0))
        self.sprite.draw(self.surface)
        surface.blit(self.surface, (self.x, self.y))"""

Default_file = """from Engine import *

if __name__ == "__main__":
    sheet = Sheet("Sheets/path/to/your/sheet")
    game = Game(10*16, 4/5.0, (255, 255, 255), 60, "Your window title", sheet, scale=2)
    game.fog_instensity = 0
    palette = pal_load("Palettes/path/to/your/palette")

    while game.RUNNING:
        game.events()
        game.update()
        game.draw()
    pygame.quit()
    quit()
"""
Tile = """import pygame, random, math
#sprite editor furnished with this program

def pal_load(filename):#load a palette
    temp = []
    file = open(filename, "r").read()
    for y in range(0, 8):
        temp.append((int(file[y * 9 + 0:y * 9 + 0 + 3]), int(file[y * 9 + 3:y * 9 + 3 + 3]),
                     int(file[y * 9 + 6:y * 9 + 6 + 3])))
    return temp

tile_rules = {"wtop":[[[0, 4, 0, 0], [0, 4, 2, 6],
                [0, 0, 2, 2], [0, 0, 0, 0],
                [0, 4, 2, 6], [0, 0, 0, 4],
                [0, 4, 0, 4], [0, 4, 0, 4],
                [0, 4, 0, 4]], [[0, 4, 0, 4, 1, 3, 1, 2], [0, 4, 0, 4, 1, 5, 1, 2],
             [6, 4, 6, 4, 7, 8, 7, 2], [6, 4, 6, 4, 7, 8, 7, 2]]], "plain":
    [[[0, 4, 0, 0], [0, 4, 2, 6],
                [0, 0, 2, 2], [0, 0, 0, 0],
                [0, 4, 2, 6], [0, 4, 0, 4]], [1, 5, 1, 5, 2, 4, 2, 3]], "block":
    [[[0, 4, 2, 6], [0, 4, 2, 6],
                [0, 4, 2, 6], [0, 4, 2, 6],
                [0, 4, 2, 6]], [0, 0, 0, 0, 0, 0, 0, 0]]}

class Sheet:#graphics holder and drawer class
    def __init__(self, filename):
        if filename[-4:] == ".chr":#checks if you give it a filename or raw data
            sheet = open(filename).read()
        else:
            sheet = filename
        self.data = []
        for y in range(0, 128):#process the data
            self.data.append([])
            for x in range(0, 128):
                self.data[y].append(int(sheet[y * 128 + x]))

    def draw(self, surface, x, y, index, palette, flipx=0, flipy=0, swap=0):
        surf = pygame.Surface((8, 8), pygame.SRCALPHA)
        surf.fill((255,255,255,0))
        for a in range(0, 8):
            for b in range(0, 8):
                if swap:#doing flips and swaps
                    t = b
                    s = a
                    f = flipy
                    l = flipx
                    if flipx:
                        t = -t
                    if flipy:
                        s = -s
                else:
                    t = a
                    s = b
                    f = flipx
                    l = flipy
                    if flipx:
                        s = -s
                    if flipy:
                        t = -t
                surf.set_at((b, a), palette[self.data[int((index & 240) / 2)+7*l+ t][int((index & 15) * 8)+7*f+ s]])#the lower and gets pixel data with it

        surface.blit(surf, (x, y))#blits the temporary surface to the given surface as well as scaling it up, for speed

class Tile:#Basic tile class, a tile can ONLY be 8x8 pixels
    def __init__(self, x, y, sheet, palette, index, tag, flipx=0, flipy=0, swap=0):
        self.x = x#data
        self.y = y#data
        self.sheet =  sheet#sheet class
        self.palette = palette#palette to draw tile in
        self.scale = 1#scale
        self.index = index#data
        self.flipx = flipx#data
        self.flipy = flipy#data
        self.swap = swap#data
        self.tag = tag#data

    def draw(self, surface):#draw method yaaaay
        self.sheet.draw(surface, self.x, self.y, self.index, self.palette, flipx=self.flipx, flipy=self.flipy, swap=self.swap)

class AdaptiveTile(Tile):#an alternative of the tile class, an adaptative one! don't use it alone, it is used in the adaptative metasprite class
    def __init__(self, x, y, sheet, palette, rules, posrules, tag, origin):#and you can't really use it unless you modify it to be independent
        Tile.__init__(self, x, y, sheet, palette, 0, tag)
        self.rules = rules#adapt rules
        self.posrules = posrules#flipping rules
        self.origin = origin

    def tile(self, blocks, x, y, posx, posy):#adaptation method
        tiling = 0
        try:
            if blocks[(((y)//(16*self.scale)+posy+1))][(((x)//(16*self.scale)+1))].tag == self.tag:
                tiling += 1
        except:
            pass
        try:
            if blocks[(((y)//(16*self.scale)+posy+1))][(((x)//(16*self.scale)+posx+1))].tag == self.tag:
                tiling += 2
        except:
            pass
        try:
            if blocks[(((y)//(16*self.scale)+1))][(((x)//(16*self.scale)+posx+1))].tag == self.tag:
                tiling += 4
        except:
            pass
        self.index = self.rules[tiling]+self.origin
        x = ((posx*-1)-1)//-2
        y = ((posy*-1)-1)//-2
        if self.posrules[y*2+x].__class__.__name__ == "list":
            self.flipx = (self.posrules[self.index-self.origin][y*2+x]& 4) // 4
            self.flipy = (self.posrules[self.index-self.origin][y*2+x] & 2) // 2
            self.swap = (self.posrules[self.index-self.origin][y*2+x] & 1)
        elif self.posrules[y*2+x].__class__.__name__ == "int":
            self.flipx = (self.posrules[y*2+x] & 4) // 4
            self.flipy = (self.posrules[y*2+x] & 2) // 2
            self.swap = (self.posrules[y*2+x] & 1)

    def draw(self, surface):#draw method yaaay
        Tile.draw(self, surface)

class MetaTile:#the basic metatile class, can be of any size
    def __init__(self, x, y, sheet, palette, indexes, flips, size, tag):#size argument in tiles, not in pixels
        self.x = x
        self.y = y
        self.tiles = []
        self.scale = 1
        self.surface = pygame.Surface((8*size[0], 8*size[1]), pygame.SRCCOLORKEY)
        self.surface.set_colorkey(palette[0])
        self.tag = tag
        for t in range(0, size[1]):#creating basic tiling
            for s in range(0, size[0]):
                self.tiles.append(Tile((8*s), (8*t), sheet, palette, indexes[t*size[0]+s], tag))
                if flips[t*size[0]+s].__class__.__name__ == "list":
                    self.tiles[t*size[0]+s].flipx = flips[t*size[0]+s][0]
                    self.tiles[t*size[0]+s].flipy = flips[t*size[0]+s][1]
                    self.tiles[t*size[0]+s].swap = flips[t*size[0]+s][2]
                elif flips[t*size[0]+s].__class__.__name__ == "int":
                    self.tiles[t * size[0] + s].flipx = (flips[t * size[0] + s]&4)//4
                    self.tiles[t * size[0] + s].flipy = (flips[t * size[0] + s]&2)//2
                    self.tiles[t * size[0] + s].swap = (flips[t * size[0] + s]&1)
        self.size = size
        self.drawtiles()#pre-render tiles

    def setiles(self, indexes, flips):#set the tiles indexes and flips
        for t in range(0, self.size[1]):
            for s in range(0, self.size[0]):
                self.tiles[t*self.size[0]+s].index = indexes[t*self.size[0]+s]
                if flips[t * self.size[0] + s].__class__.__name__ == "list":
                    self.tiles[t * self.size[0] + s].flipx = flips[t * self.size[0] + s][0]
                    self.tiles[t * self.size[0] + s].flipy = flips[t * self.size[0] + s][1]
                    self.tiles[t * self.size[0] + s].swap = flips[t * self.size[0] + s][2]
                elif flips[t * self.size[0] + s].__class__.__name__ == "int":
                    self.tiles[t * self.size[0] + s].flipx = (flips[t * self.size[0] + s] & 4) // 4
                    self.tiles[t * self.size[0] + s].flipy = (flips[t * self.size[0] + s] & 2) // 2
                    self.tiles[t * self.size[0] + s].swap = (flips[t * self.size[0] + s] & 1)
        self.drawtiles()

    def getpalette(self):#gets the palette of the tiles
        return self.tiles[0].palette

    def setpalette(self, palette):#sets the global tiles palette
        for i in range(len(self.tiles)):
            self.tiles[i].palette = palette
        self.drawtiles()

    def drawtiles(self):#pre-render tiles
        self.surface.fill((0, 0, 0, 0))
        for i in range(len(self.tiles)):
            self.tiles[i].draw(self.surface)

    def draw(self, surface):#display tiles
        surface.blit(self.surface, (self.x, self.y))

class AdaptiveMetaTile(MetaTile):#adaptative metatile, ya know, the daddy of the adaptative tile
    def __init__(self, x, y, sheet, palette, rules, posrules, tag, origin):
        MetaTile.__init__(self, x, y, sheet, palette, [0, 0, 0, 0], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], (2, 2), tag)
        self.tiles = []#this daddy can only have 4 kids, no less no more
        for t in range(0, 2):
            for s in range(0, 2):
                if rules[0].__class__.__name__ == "list":
                    self.tiles.append(AdaptiveTile((4*s*scale), (4*t*scale), sheet, palette, rules[t*2+s], posrules, tag, origin))
                else:
                    self.tiles.append(AdaptiveTile((4*s*scale), (4*t*scale), sheet, palette, rules, posrules, tag, origin))
        self.rules = rules
        self.drawtiles()


    def tile(self, blocks):#adaptation method, you just give a metatile listlist and it does the job, no more hours of well placing blocks!
        for y in range(0, self.size[0]):
            for x in range(0, self.size[1]):
                self.tiles[y*self.size[0]+x].tile(blocks, self.x, self.y, (x*-2+1)*-1, (y*-2+1)*-1)
        self.drawtiles()

    def drawtiles(self):#pre-render method
        MetaTile.drawtiles(self)

    def draw(self, surface):#draw method, yaaay
        MetaTile.draw(self, surface)

class AnimatedMetaTile(MetaTile):#an animated metatile, can be of any size
    #you need to manually create frames and animations
    def __init__(self, x, y, sheet, palette, size, tag, latency, flipx=0, flipy=0, swap=0):
        indexes = []
        flips = []
        for s in range(size[1]):#empty indexes and flips of the tiles
            for t in range(size[0]):
                indexes.append(0)
                flips.append([0, 0, 0])
        self.flipx = flipx#get personal flips
        self.flipy = flipy
        self.swap = swap
        self.oldswap = 0#it's for updating the draw method, just technical thing
        MetaTile.__init__(self, x, y, sheet, palette, indexes, flips, size, tag)
        #init the basic metatile
        self.tiles = []#and immediatly replace the tiles with others
        for y in range(0, self.size[1]):
            for x in range(0, self.size[0]):
                self.tiles.append(Tile(0, 0, sheet, palette, 0, tag, flipx=flipx, flipy=flipy, swap=swap))

        self.frames = []
        self.blankframe = []#the code creates a blank frame, for a blank animation
        for y in range(self.size[1]):
            self.blankframe.append([])
            for x in range(self.size[0]):
                self.blankframe[y].append(0)
        self.addframe(self.blankframe)#adds the blank frame, index 0 in the self.frames list
        self.animations = {}
        self.animation = "None"#adds a blank animation
        self.addanimation("None")
        self.index = 0#sets the index
        self.latency = 0#the latency is the number of frames before increasing the index
        self.maxlatency = latency
        self.drawtiles()#pre-rendering of the tiles

    def addframe(self, frame):#method to add a frame
        self.frames.append(frame)

    def color_a_dinosaur(self):#method to color a dinosaur, and yes, it is extra useless data
        pass

    def addanimation(self, name, indexes=[0]):#method to add an animation, by default it adds a blank animation, specify!
        self.animations[name] = indexes

    def playanimation(self, name):#plays the given animation if it exists, else it continues playing the current one.
        anim = self.animation
        try:
            self.animation = name
            self.animations[self.animation]
        except:
            self.animation = anim
        else:
            self.index = 0
            self.latency = 0

    def drawtiles(self):#modified pre-render function, with flipping and ect
        self.surface.fill((0, 0, 0, 255))
        if not self.swap == self.oldswap:
            self.surface = pygame.Surface((8*self.size[self.swap], 8*self.size[~self.swap&1]), pygame.SRCALPHA)
            self.oldswap = self.swap
        for y in range(0, self.size[1]):
            for x in range(0, self.size[0]):
                if self.swap:
                    a = y
                    b = x
                else:
                    a = x
                    b = y
                if self.flipx:
                    a = (self.size[self.swap]-a-1)
                if self.flipy:
                    b = (self.size[~self.swap&1]-b-1)
                self.tiles[y*self.size[0]+x].x = a*8*self.scale
                self.tiles[y*self.size[0]+x].y = b*8*self.scale
                self.tiles[y*self.size[0]+x].draw(self.surface)

    def draw(self, surface):#modified draw method, if the index is modified, the code automagically makes a new pre-render
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                self.tiles[y*self.size[0]+x].flipx = self.flipx
                self.tiles[y*self.size[0]+x].flipy = self.flipy
                self.tiles[y*self.size[0]+x].swap = self.swap
        self.latency += 1
        if self.latency >= self.maxlatency:
            self.latency = 0
            self.index += 1
            if self.index >= len(self.animations[self.animation]):
                self.index = 0
            for y in range(self.size[1]):
                for x in range(self.size[0]):
                    self.tiles[y*self.size[0]+x].index = self.frames[self.animations[self.animation][self.index]][y][x]
            self.drawtiles()
        MetaTile.draw(self, surface)



if __name__ == "__main__":#technical demo code, just for showing off a bit of possibilities
    #no I won't comment that, I don't want to.
    pygame.init()
    sheet = Sheet("Sheets/bank1.chr")
    scale=2
    display = pygame.Surface((25*16, 20*16))
    window = pygame.display.set_mode((25*16*scale, 20*16*scale))
    screen = []

    palette = pal_load("Palettes/grass.pal")
    rpalette = pal_load("Palettes/snow.pal")
    bpalette = pal_load("Palettes/summer.pal")
    for y in range(0, 22):
        screen.append([])
        for x in range(0, 27):
            screen[y].append(AdaptiveMetaTile((x-1)*16, (y-1)*16, sheet, rpalette, [0, 0, 0, 0, 0, 0, 0, 0], tile_rules["wtop"][0], " ", 0))
    animmetatile = AnimatedMetaTile(0, 8, sheet, palette, (2, 3), "p", 6, swap=1, flipy=1, flipx=1)
    metatile = MetaTile(23*8, 8, sheet, bpalette, [1, 2, 1, 1, 2, 1], [0, 0, 4, 2, 2, 6], (3, 2), "e")
    animmetatile.addframe([[6, 7], [8, 9], [10, 11]])
    animmetatile.addframe([[12, 13], [14, 15], [16, 17]])
    animmetatile.addframe([[18, 13], [14, 15], [16, 17]])
    animmetatile.addframe([[6, 19], [8, 9], [20, 21]])
    animmetatile.addanimation("IDLE", indexes=[1, 2, 3, 4])
    animmetatile.playanimation("IDLE")
    flips = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 0, 1], [1, 1, 1]]
    index = 0
    latency = 0
    maxlatency = 60
    running = True
    clock = pygame.time.Clock()
    mouse = [0, 0, 0, 0, 0, 0]
    for y in range(len(screen)):
        for x in range(len(screen[y])):
            screen[y][x].tile(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse[0] = 1
                if event.button == 3:
                    mouse[1] = 1
                if event.button == 2:
                    mouse[4] = 1
                if event.button == 8:
                    mouse[5] = 1
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse[0] = 0
                if event.button == 3:
                    mouse[1] = 0
                if event.button == 2:
                    mouse[4] = 0
                if event.button == 8:
                    mouse[5] = 0

        if mouse[0] or mouse[1] or mouse[4] or mouse[5]:
            mouse[2], mouse[3] = pygame.mouse.get_pos()
            if mouse[0]:
                screen[mouse[3]//(16*scale)+1][mouse[2]//(16*scale)+1] = AdaptiveMetaTile((mouse[2]//(16*scale))*(16), (mouse[3]//(16*scale))*(16), sheet, palette, tile_rules["plain"][1], tile_rules["plain"][0], "m", 0)
            if mouse[1]:
                screen[mouse[3]//(16*scale)+1][mouse[2]//(16*scale)+1] = AdaptiveMetaTile((mouse[2]//(16*scale))*(16), (mouse[3]//(16*scale))*(16), sheet, palette, tile_rules["block"][1], tile_rules["block"][0], "p", 1)
            if mouse[4]:
                screen[mouse[3]//(16*scale)+1][mouse[2]//(16*scale)+1] = AdaptiveMetaTile((mouse[2]//(16*scale))*(16), (mouse[3]//(16*scale))*(16), sheet, rpalette, [0, 0, 0, 0, 0, 0, 0, 0], tile_rules["wtop"][0], " ", 0)
            if mouse[5]:
                screen[mouse[3]//(16*scale)+1][mouse[2]//(16*scale)+1] = AdaptiveMetaTile((mouse[2]//(16*scale))*(16), (mouse[3]//(16*scale))*(16), sheet, bpalette, tile_rules["wtop"][1], tile_rules["wtop"][0], "p", 32)
            for y in range(0, 3):
                for x in range(0, 3):
                    screen[(mouse[3]//(16*scale)+y)][(mouse[2]//(16*scale)+x)].tile(screen)

        display.fill((0, 0, 0))
        for y in range(1, len(screen)-1):
            for x in range(1, len(screen[y])-1):
                screen[y][x].draw(display)
        latency += 1
        if latency >= maxlatency:
            index += 1
            if index >= len(flips):
                index = 0
            latency = 0
            animmetatile.flipx = flips[index][0]
            animmetatile.flipy = flips[index][1]
            animmetatile.swap = flips[index][2]
        animmetatile.draw(display)
        if metatile.getpalette() == bpalette:
            metatile.setpalette(palette)
        elif metatile.getpalette() == palette:
            metatile.setpalette(rpalette)
        elif metatile.getpalette() == rpalette:
            metatile.setpalette(bpalette)
        metatile.drawtiles()
        metatile.draw(display)
        window.blit(pygame.transform.scale(display, (25*16*scale, 20*16*scale)), (0, 0))
        pygame.display.flip()
    pygame.quit()
#this program was made ENTIERLY by Geek_Joystick, DON'T STEAL IT, and credit me.
"""


FogLight = """import pygame

class FogLight:
    def __init__(self, object, radius):
        self.object = object
        self.radius = radius
        self.intensity = 255
        self.surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)

    def draw(self, surface):
        self.surface.fill((0, 0, 0))
        for i in range(8, 0, -1):
            pygame.draw.circle(self.surface, (0, 0, 0, int((self.intensity/8)*i)), (self.radius, self.radius), int(self.radius/8)+int((self.radius/16/8)*i-1))
        surface.blit(self.surface, (self.object.x+int(self.object.sprite.size[0]/2*8)-self.radius, self.object.y+int(self.object.sprite.size[0]/2*8)-self.radius), special_flags=pygame.BLEND_RGBA_MIN)
"""
Log = """class Log:
    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, "w")

    def start_text(self):
        self.addentry("log started")
        pass #TODO

    def submiterror(self, err, function="unknown"):
        self.file.write("Erreur in " + function + "() function > " + err + "\n")

    def addentry(self, text):
        self.file.write(text + "\n")

    def end(self):
        self.file.close()
"""

#End of files contebt

#begining of the manager code

def getRAMinfo():
    try:
        p = os.popen('free')
        i = 0
        while 1:
            i = i + 1
            line = p.readline()
            if i==2:
                data = line.split()[1:4]
                data[0] = data[0][0:4]
                data[0] = str(data[0])+" MB"
                return(data)
    except:
        return(["unknow"])

class Manager():
    def __init__(self, argv=None):
        self.argv = argv
        self.argc = len(argv)

    def status(self):
        currentDT = datetime.datetime.now()
        print("Status :") #The aperture logo will change in the final release
        print("""
              \033[33;1m.,-:;//;:=,\033[0m                \033[7m  Pygine Terminal Info                \033[0m
          \033[33;1m. :H@@@MM@M#H/.,+%;,\033[0m           
       \033[33;1m,/X+ +M@@M@MM%=,-%HMMM@X/,\033[0m         \033[1mProcessor:\033[0m unknow
     \033[33;1m-+@MM; SM@@MH+-,;XMMMM@MMMM@+-\033[0m       \033[1mRAM memory:\033[0m""", getRAMinfo()[0] ,"""
    \033[33;1m;@M@@M- XM@X;. -+XXXXXHHH@M@M#@/.\033[0m     \033[1mOS:\033[0m""", platform.system() ,"""
  \033[33;1m,%MM@@MH ,@%=            .---=-=:=,.\033[0m    \033[1m(c) Rocket chip 2019\033[0m
  \033[33;1m=@#@@@MX .,              -%HXSS%%%+;\033[0m
 \033[33;1m=-./@M@MS                  .;@MMMM@MM:\033[0m  \033[7m  Project Monitor                     \033[0m
 \033[33;1mX@/ -SMM/                    .+MM@@@MS\033[0m
\033[33;1m,@M@H: :@:                    . =X#@@@@-\033[0m  \033[1mProject name:\033[0m      """+project_name+"""        
\033[33;1m,@@@MMX, .                    /H- ;@M@M=\033[0m  \033[1mProject version:\033[0m   """+project_version+"""    
\033[33;1m.H@@@@M@+,                    %MM+..%#S.\033[0m                          
 \033[33;1m/MMMM@MMH/.                  XM@MH; =;\033[0m   \033[1mTested:\033[0m            """+ is_project_tested+""" 
  \033[33;1m/%+%SXHH@S=              , .H@@@@MX,\033[0m    \033[1mDEBUG:\033[0m             """+is_project_debug+"""
   \033[33;1m.=--------.           -%H.,@@@@@MX,\033[0m    \033[1mPygine version:\033[0m    v 0.1 Development version
    \033[33;1m.%MM@@@HHHXXSSS%+- .:MMX =M@@MM%.\033[0m                               
     \033[33;1m=XMMM@MM@MM#H;,-+HMM@M+ /MMMX=\033[0m      \033[7m  Date and Time                        \033[0m
       \033[33;1m=%@M@M#@S-.=S@MM@@@M; %M%=\033[0m     
         \033[33;1m' :+S+-,/H#MMMMMMM@= ='\033[0m           \033[1mDate:\033[0m""",currentDT.strftime("%Y/%m/%d"),"""
               \033[33;1m=++%%%%+/:-.\033[0m              \033[1mTime:\033[0m""",currentDT.strftime("%H:%M:%S"),"""
""")

    def startproject(self):
        self.project_name = input("Project name : ")
        self.utils = input("Do you want to enable utils for creating 8-bit Sprites and palletes? (y/n): ")
        if self.utils.lower() == "y":
            self.utils = True
        else:
            self.utils = False
        os.mkdir(self.project_name)
        os.mkdir(self.project_name+"/Sprites")
        os.mkdir(self.project_name+"/Scripts")
        os.mkdir(self.project_name+"/Scenes")
        os.mkdir(self.project_name+"/Behaviours")
        if self.utils == True:
            os.mkdir(self.project_name+"/Utils")
        with open(self.project_name + "/Engine.py", "w") as engine:
            engine.write(Engine)
        with open(self.project_name + "/"+self.project_name+".py", "w") as default_file:
            default_file.write(Default_file)
        with open(self.project_name + "/README.md", "w") as readme:
            readme.write("Readme for "+self.project_name)
        with open(self.project_name + "/Scripts/GameObject.py", "w") as readme:
            readme.write(GameObject)
        with open(self.project_name + "/Scripts/Controller.py", "w") as readme:
            readme.write(Controller)
        with open(self.project_name + "/Scripts/Tile.py", "w") as readme:
            readme.write(Tile)
        with open(self.project_name + "/Scripts/FogLight.py", "w") as readme:
            readme.write(FogLight)
        with open(self.project_name + "/Scripts/Log.py", "w") as readme:
            readme.write(Log)

    def shell(self):
        RUNNING = True
        print("Pygine 0.1 Development version (June 27 2019)")
        print("[Python "+platform.python_version()+"] on "+ platform.system())
        print('Type "help", "copyright", "credits" or "license" for more information.')
        while RUNNING:
            input(">>>")


    def help(self):
        helps = {'test' : 'Just a command for test if the help work correctly'}
        try:
            print(helps[self.argv[self.argc-1]])
        except KeyError:
            if self.argv[self.argc-1] == 'help' or self.argc == 1:
                self.short_help()
            else:
                print("Sorry but there is no help for command : "+self.argv[self.argc-1])

    def short_help(self):
        print('manage.py v O.1')
        print('Usage : python3 manage.py <command> <args> [--verbose]')

    def make_executable(self):
        agree = input("You will integrate your python script in an executable (.exe) using pyinstaller, it might be not very optimized and the executable will be fat because it have to load with it the python interpreter. This method works but sometimes it better to share the source code directly. Your source code won't be erase. Do you want to proceed? (y/n) : ")
        if agree.lower() == "y":
            try:
                if os.system("cd " + project_name + " && pyinstaller "+ project_name +".py --onefile") == 0:
                    print("Congratulations, you succesfully 'compile' your script to an executable. DON'T FORGET TO MOVE IT FROM DIST TO THE ORIGINAL PLACE OF YOUR SCRIPT, ELSE IT WON'T WORK. After it you can remove dist if you want.")
                else:
                    print("Error, please check if the folder and your projects file(s) are correctly setting up or if pyinstaller is correctly installed (doing pip install pyinstaller). If you can't fix this error, you can contact us directly or do it manually with pyinstaller or other programs")
            except:
                print("Unknow error, if you can't fix this error, you can do you're 'compilation' manually with pyinstaller (https://www.pyinstaller.org/) or other programs.")

    def execute(self):
        try:
            self.subcommand = self.argv[1]
            for arg in self.argv:
                try:
                    if arg[0] == '-' and arg[1] == '-':
                        exec("self." +arg[1:len(arg)]+" = True")
                except:
                    print("Invalid argument : "+arg)
        except IndexError:
            self.subcommand = 'help'# Display help if no arguments were given.

        try:
            if self.argv[1][0] != '-' and self.argv[1][1] != '-':
                exec('self.'+self.subcommand+'()')
        except AttributeError:
            print("No command named "+self.subcommand)
            self.short_help()
        except IndexError:
            self.short_help()

if __name__ == "__main__":
    manager = Manager(sys.argv)
    manager.execute()