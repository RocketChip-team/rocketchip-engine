from Scripts.Controller import *
from Scripts.GameObject import *
from Scripts.FogLight import *
from Scripts.Collider import *

class Game:
    def __init__(self, width, ratio, background, fps, title, sheet, scale=1, gravity=0, ignorex=16, ignorey=16):
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
        self.fog_color = [0, 0, 0]
        self.gravity = gravity
        self.ignorex = ignorex
        self.ignorey = ignorey

        pygame.init()
        self.scale = scale
        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        self.render = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.fog = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.display.set_caption(self.TITLE)

        self.levents = pygame.event.get()
        self.clock = pygame.time.Clock()
        self.objectlist = []

    def add_object(self, object, layer):
        while layer > len(self.objectlist)-1:
            self.objectlist.append([])
        self.objectlist[layer].append(object)

    def set_title(self, title):
        pygame.display.set_caption(title)

    def events(self):
        self.levents = pygame.event.get()
        for event in self.levents:
            if event.type == pygame.QUIT:
                self.RUNNING = False
        self.controller.update(self.levents)
        if self.controller.get_press("escape"):
            self.RUNNING = False

    def update(self):
        self.fog.fill((self.fog_color[0], self.fog_color[1], self.fog_color[2], self.fog_instensity))
        for i in range(len(self.objectlist)):
            for j in range(len(self.objectlist[i])):
                if self.on_screen(self.objectlist[i][j]):
                    self.objectlist[i][j].update(self)

    def on_screen(self, object):
        if object.x > -self.ignorex and object.x < self.width + self.ignorex and object.y > -self.ignorey and object.y < self.height + self.ignorey:
            return True
        else:
            if hasattr(object, "ignore_off_bounds"):
                if object.ignore_off_bounds:
                    return True
        return False

    def draw(self):
        self.render.fill(self.BACKGROUND)
        for i in range(len(self.objectlist)):
            for j in range(len(self.objectlist[i])):
                if self.on_screen(self.objectlist[i][j]):
                    self.objectlist[i][j].draw(self.render)
        self.display.blit(pygame.transform.scale(self.render, (self.WIDTH, self.HEIGHT)), (0, 0))
        self.display.blit(pygame.transform.scale(self.fog, (self.WIDTH, self.HEIGHT)), (0, 0))
        pygame.display.update()
        self.clock.tick(self.FPS)


if __name__ == "__main__":
    game = Game(25*16, 4/5.0, (0, 0, 0), 60, "Pygame Boilerplate", Sheet("bank1.chr"))
    pygame.quit()
    quit()
