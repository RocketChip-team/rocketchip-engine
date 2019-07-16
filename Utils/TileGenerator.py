import os, sys

class Main:
    def __init__(self, *argv):
        self.data = self.new()
        self.max = 1
        self.min = 1
        self.corner = 2
        self.RUNNING = True

        if len(argv):
            if argv[0]:
                while self.RUNNING:
                    exec(input("command: "))


    def generate(self):
        self.data = self.new()
        for y in range(0, 8):
            for x in range(0, 8):
                if y < self.corner:
                    if x >= self.corner and x <= 7+self.corner:
                        self.data[y][x] = 3
                elif x < self.corner:
                    if y >= self.corner and y <= 7+self.corner:
                        self.data[y][x] = 3
                else:
                    if x >= self.corner and y >= self.corner and x <= 7+self.corner and y <= 7+self.corner:
                        self.data[y][x] = 2

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
    if len(sys.argv):
        if sys.argv[1] == "-c":
            Main(True)


