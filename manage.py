#!/usr/bin/python3
# This sript will manage projects
import sys
import os
import platform
import datetime

project_name = "Test Project"
project_version = "v 0.1"
is_project_tested = "\033[31;1mNo\033[33;0m"
is_project_debug = "\033[31;1mTrue\033[33;0m"

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

Default_file = """import Engine.py
"""

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
         \033[33;1m':+S+-,/H#MMMMMMM@= ='\033[0m           \033[1mDate:\033[0m""",currentDT.strftime("%Y/%m/%d"),"""
               \033[33;1m=++%%%%+/:-.\033[0m               \033[1mTime:\033[0m""",currentDT.strftime("%H:%M:%S"),"""
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
        pass

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
