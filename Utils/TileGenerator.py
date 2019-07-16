#DISCONTINUED PROGRAM, IF YOU FIND UTILITY TO IT, THAT'S GOOD FOR YOU

import os, sys

class Main:
    def __init__(self, *argv):
        self.data = self.new()
        self.max = 1
        self.min = 1
        self.dis = 1
        self.corner = 2
        self.offx = 1
        self.offy = 1
        self.RUNNING = True

        if len(argv):
            if argv[0]:
                while self.RUNNING:
                    exec(input("command: "))


    def generate(self):
        self.data = self.new()
        for y in range(0, 8):
            for x in range(0, 8):
                if y+x-self.goffx-self.goffy > self.corner and (x > self.goffx and y > self.goffy):
                        self.data[y][x] = 2
                elif x+y-self.goffx-self.goffy >= self.corner and (x > self.goffx-1 and y > self.goffy-1):
                        self.data[y][x] = 3
        height = self.min
        for x in range(0, 8):


    def new(self):
        data = []
        for y in range(0, 128):
            data.append([])
            for x in range(0, 128):
                data[y].append(0)
        return data

    def save(self, path):
        file = open(path, "w")
        try:
            for y in range(0, len(self.data)):
                for x in range(0, len(self.data[y])):
                    file.write(str(self.data[y][x]))
            file.write(
                "this data and the programs associated with it are made by Team Rocket Chip, DON'T STEAL THEM, and credit me")
            file.close()
        except:
            pass

if __name__ == "__main__":
    if sys.argv:
        if sys.argv[1] == "-c":
            Main(True)


