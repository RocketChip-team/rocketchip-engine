import pygame
import random


class FogLight:
    def __init__(self, object, radius, blur):
        self.object = object
        self.radius = radius
        self.over_radius = radius + 12
        self.actradius = radius+random.randint(0, self.over_radius-self.radius)
        self.modspeed = .2
        self.modspeed_ts = .2
        self.intensity = 255
        self.blur = blur
        self.blur_radius = 16
        self.state = "I"
        self.surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)

    def change_radius(self, new_radius, speed, over_radius):
        self.radius = new_radius
        self.modspeed_ts = self.modspeed
        self.modspeed = speed
        self.over_radius = over_radius
        self.state = "I"

    def update(self):
        if self.state == "I":
            if self.over_radius >= self.actradius:
                self.actradius += self.modspeed
                if self.over_radius <= self.actradius:
                    self.actradius = self.over_radius
                    self.state = "D"
            elif self.over_radius <= self.actradius:
                self.actradius -= self.modspeed
                if self.over_radius >= self.actradius:
                    self.actradius = self.over_radius
                    self.state = "D"
        elif self.state == "D":
            if self.radius >= self.actradius:
                self.actradius += self.modspeed
                if self.radius <= self.actradius:
                    self.actradius = self.radius
                    self.state = "I"
                    if not self.modspeed == self.modspeed_ts:
                        self.modspeed = self.modspeed_ts
            elif self.radius <= self.actradius:
                self.actradius -= self.modspeed
                if self.radius >= self.actradius:
                    self.actradius = self.radius
                    self.state = "I"
                    if not self.modspeed == self.modspeed_ts:
                        self.modspeed = self.modspeed_ts

    def draw(self, surface, color):
        self.update()
        self.surface.fill(color)
        for i in range(self.blur, 0, -1):
            pygame.draw.circle(self.surface, (color[0], color[1], color[2], int((self.intensity/self.blur)*(i-1))), (int(self.actradius), int(self.actradius)), int(self.actradius/self.blur_radius)+int((self.actradius/self.blur_radius/self.blur)*i-1))
        surface.blit(self.surface, (self.object.x+int(self.object.sprite.size[0]/2*8)-int(self.actradius), self.object.y+int(self.object.sprite.size[0]/2*8)-int(self.actradius)), special_flags=pygame.BLEND_RGBA_MULT)