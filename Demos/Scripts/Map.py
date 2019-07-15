from Scripts.Controller import *
from Scripts.Tile import *
from Scripts.GameObject import *
from Scripts.FogLight import *


class Map:
    def __init__(self):
        self.objets = []
        self.tilemap = []

    def load(self, map, pre):
        pass

    def create_object(self, preset, index):
        pass

    def draw(self, surface):
        pass