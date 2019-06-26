import pygame


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