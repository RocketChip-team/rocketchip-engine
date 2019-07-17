import os
import pygame


class MButton:
    def __init__(self, x, y, w, h, tag, function):
        self.coords = (x, y, w, h)
        self.function = function
        self.tag = tag

    def update(self, mousePos):
        if mousePos[0] > self.coords[0] and mousePos[0] < self.coords[0] + self.coords[2]:
            if mousePos[1] > self.coords[1] and mousePos[1] < self.coords[1] + self.coords[3]:
                return self.function()
        return 0

    def draw(self, display, font, color=(255, 255, 255)):
        pygame.draw.rect(display, color,
                         (self.coords[0] - 2, self.coords[1] - 2, self.coords[2] + 4, self.coords[3] + 4))
        pygame.draw.rect(display, (255-color[0], 255-color[1], 255-color[2]), self.coords)
        text = font.render(self.tag, False, color)
        text = pygame.transform.scale(text, (self.coords[2] - 2, self.coords[3] - 2))
        textrect = text.get_rect()
        textrect.topleft = (self.coords[0] + 2, self.coords[1] + 2)
        display.blit(text, textrect)


class Main:
    def __init__(self, palette):
        pygame.init()
        self.display = pygame.display.set_mode((640, 480))
        self.minimap = pygame.Surface((128, 128))
        self.editor = pygame.Surface((8, 8))
        pygame.display.set_caption("Palette Editor")
        self.clock = pygame.time.Clock()
        self.data = self.new()
        self.mouse = [0, 0]
        self.currentsprite = [0, 0]
        self.cursor = 0
        self.palette = palette
        self.font = pygame.font.SysFont("", 20, bold=True)
        self.RUNNING = True
        self.btn_new = MButton(2, 2, 212, 100, "New", self.new)
        self.btn_open = MButton(214, 2, 212, 100, "Open", self.open)
        self.btn_save = MButton(428, 2, 212, 100, "Save", self.save)
        self.btn_colors = []
        for i in range(0, 8):
            self.btn_colors.append(MButton(2+(636/8)*i, 150, int(636/8), 290, str(i+1), self.color))
        self.button = [0, 0, 0]
        self.pos = [0, 0]
        self.handler()

    def color(self):
        root = Tk()
        color = tkcp.askcolor(color="red", parent=None, title=("Choose Color"), alpha=False)
        root.destroy()
        if not color[0] == None:
            return color[0]
        return 0

    def save(self):
        root = Tk()
        file = filedialog.asksaveasfile(initialdir=os.getcwd(), title='Choose a Folder to save file into',
                                        defaultextension=".pal")
        root.destroy()
        try:
            for y in range(0, len(self.data)):
                for x in range(0, len(self.data[y])):
                    data = str(self.data[y][x])
                    if len(data) == 1:
                        data = "00"+data
                    elif len(data) == 2:
                        data = "0"+data
                    file.write(data)
            file.write(
                "this data and the programs associated with it are made by Geek_Joystick, DON'T STEAL THEM, and credit me")
        except:
            pass

    def new(self):
        data = []
        for y in range(0, 8):
            data.append((255, 255, 255))
        return data

    def open(self):
        root = Tk()
        file = filedialog.askopenfile(initialdir=os.getcwd(), title='Choose a Palette file',
                                      filetypes=(("PAL files", "*.pal"), ("All files", "*.*")))
        root.destroy()
        try:
            data = file.read()
            file.close()
        except:
            pass
        else:
            temp = []
            for y in range(0, 8):
                temp.append((int(data[y*9+0:y*9+0+3]),int(data[y*9+3:y*9+3+3]), int(data[y*9+6:y*9+6+3])))
            return temp

    def handler(self):
        while self.RUNNING:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.RUNNING = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.RUNNING = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if event.pos[1] < 100:
                        openr = self.btn_open.update(event.pos)
                        if openr:
                            self.data = openr
                        newr = self.btn_new.update(event.pos)
                        if newr:
                            self.data = newr
                        palr = self.btn_save.update(event.pos)
                        if palr:
                            self.palette = palr
                    for i in range(0, 8):
                        color = self.btn_colors[i].update(event.pos)
                        if color:
                            self.data[i] = color
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.button = [0, 0, 0]

    def update(self):
        self.pos = pygame.mouse.get_pos()

    def draw(self):
        self.display.fill(self.palette[0])
        # draw buttons
        self.btn_new.draw(self.display, self.font)
        self.btn_open.draw(self.display, self.font)
        self.btn_save.draw(self.display, self.font)
        for i in range(0, 8):
            self.btn_colors[i].draw(self.display, self.font, color=self.data[i])

        # update dislpay
        pygame.display.update()


if __name__ == "__main__":
    from tkinter import *
    from tkinter import filedialog
    import tkcolorpicker as tkcp

    Main(((0, 0, 0), (255, 255, 255), (173, 173, 173), (81, 81, 81), (0, 0, 255), (255, 255, 0), (0, 255, 255),
          (255, 0, 255)))
    pygame.quit()
# this program was made ENTIERLY by Geek_Joystick, DON'T STEAL IT, and credit me.
