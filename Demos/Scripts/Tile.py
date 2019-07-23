import pygame, random, math
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
                surface.set_at((b+x, a+y), palette[self.data[int((index & 240) / 2)+7*l+ t][int((index & 15) * 8)+7*f+ s]])#the lower and gets pixel data with it

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
