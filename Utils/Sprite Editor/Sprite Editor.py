import os
import pygame
class MButton:
	def __init__(self, x, y, w, h, tag, function):
		self.coords = (x, y, w, h)
		self.function = function
		self.tag = tag

	def update(self, mousePos):
		if mousePos[0] > self.coords[0] and mousePos[0] < self.coords[0]+self.coords[2]:
			if mousePos[1] > self.coords[1] and mousePos[1] < self.coords[1]+self.coords[3]:
				return self.function()

		return 0

	def draw(self, display, font):
		pygame.draw.rect(display, (255, 255, 255), (self.coords[0]-2, self.coords[1]-2, self.coords[2]+4, self.coords[3]+4))
		pygame.draw.rect(display, (0, 0, 0), self.coords)
		text = font.render(self.tag, False, (255, 255, 255))
		text = pygame.transform.scale(text, (self.coords[2]-2, self.coords[3]-2))
		textrect = text.get_rect()
		textrect.topleft = (self.coords[0]+2, self.coords[1]+2)
		display.blit(text, textrect)

class Main:
	def __init__(self, palette):
		pygame.init()
		self.display = pygame.display.set_mode((640, 480))
		self.minimap = pygame.Surface((128, 128))
		self.editor = pygame.Surface((8, 8))
		pygame.display.set_caption("Sprite Editor")
		self.clock = pygame.time.Clock()
		self.data = self.new()
		self.mouse = [0, 0]
		self.currentsprite = [0, 0]
		self.color = 1
		self.cursor = 0
		self.palette = palette
		self.font = pygame.font.SysFont("", 20, bold=True)
		self.RUNNING = True
		self.btn_new = MButton(2, 2, 212, 100, "New", self.new)
		self.btn_open = MButton(214, 2, 212, 100, "Open", self.open)
		self.btn_palette = MButton(428, 2, 212, 100, "Palette", self.pal)
		self.btn_save = MButton(2, self.display.get_height()-88, self.display.get_width()-4, 86, "Save", None)
		self.button = [0, 0, 0]
		self.pos = [0,0]
		self.handler()

	def save(self):
		root = Tk()
		file = filedialog.asksaveasfile(initialdir=os.getcwd(),title='Choose a Folder to save file into',defaultextension=".chr")
		root.destroy()
		try:
			for y in range(0, len(self.data)):
				for x in range(0, len(self.data[y])):
					file.write(str(self.data[y][x]))
			file.write("this data and the programs associated with it are made by Team Rocket Chip, DON'T STEAL THEM, and credit me")
		except:
			pass
	def new(self):
		data = []
		for y in range(0,128):
			data.append([])
			for x in range(0,128):
				data[y].append(0)
		return data

	def open(self):
		root = Tk()
		file = filedialog.askopenfile(initialdir=os.getcwd(),title='Choose a Sprite file',filetypes=(("CHR files", "*.chr"), ("All files", "*.*")))
		root.destroy()
		try:
			data = file.read()
			file.close()
		except:
			pass
		else:
			temp = []
			for y in range(0, 128):
				temp.append([])
				for x in range(0, 128):
					try:
						temp[y].append(int(data[y*128+x]))
					except:
						temp[y].append(0)
			return temp

	def pal(self):
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
				temp.append((int(data[y * 9 + 0:y * 9 + 0 + 3]), int(data[y * 9 + 3:y * 9 + 3 + 3]),
							 int(data[y * 9 + 6:y * 9 + 6 + 3])))
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
				if event.button == 4:
					self.color -= 1
					if self.color < 0:
						self.color = len(self.palette)-1
				if event.button == 5:
					self.color += 1
					if self.color == len(self.palette):
						self.color = 0
				
				if event.button == 1:
					if event.pos[1] < 100:
						openr = self.btn_open.update(event.pos)
						if openr:
							self.data = openr
							self.refresh()
						newr = self.btn_new.update(event.pos)
						if newr:
							self.data = newr
							self.refresh()
						palr = self.btn_palette.update(event.pos)
						if palr:
							self.palette = palr
							self.refresh()
					
					if event.pos[1] > self.display.get_height()-100:
						self.save()
					elif event.pos[0]-344 > 0 and event.pos[0]-344 < self.editor.get_rect().w*32:
						if event.pos[1]-120 > 0 and event.pos[1]-120 < self.editor.get_rect().h*32:
							self.button = [1, event.pos[0], event.pos[1]]
					elif (event.pos[0]-20) > 0 and (event.pos[0]-20) < self.minimap.get_rect().w*2:
						if (event.pos[1]-120) > 0 and (event.pos[1]-120) < self.minimap.get_rect().h*2:
							self.currentsprite = [int((event.pos[0]-20)/16), int((event.pos[1]-120)/16)]
							if self.currentsprite[0] > 15:
								self.currentsprite[0] = 15
							if self.currentsprite[1] > 15:
								self.currentsprite[1] = 15
			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					self.button = [0, 0, 0]
	def update(self):
		self.pos = pygame.mouse.get_pos()
		if self.button[0] and self.pos[0]-344 > 0 and self.pos[0]-344 < self.editor.get_rect().w*32 and self.pos[1]-120 > 0 and self.pos[1]-120 < self.editor.get_rect().h*32:
			self.button[1] = self.pos[0]
			self.button[2] = self.pos[1]
		
		self.cursor += 1
		if self.cursor == len(self.palette):
			self.cursor = 0
		if self.button[0]:
			self.data[self.currentsprite[1]*8+int((self.button[2]-120)/32)][self.currentsprite[0]*8+int((self.button[1]-344)/32)] = self.color
	def refresh(self):
		for y in range(0, 128):
			for x in range(0, 128):
				pygame.draw.rect(self.minimap, self.palette[self.data[y][x]], (x, y, 1, 1))
	def draw(self):
		self.display.fill(self.palette[0])
		#draw buttons
		self.btn_new.draw(self.display, self.font)
		self.btn_open.draw(self.display, self.font)
		self.btn_palette.draw(self.display, self.font)
		self.btn_save.draw(self.display, self.font)

		#draw minimap
		for y in range(self.currentsprite[1]*8, (self.currentsprite[1]*8)+8):
			for x in range(self.currentsprite[0]*8, (self.currentsprite[0]*8)+8):
				pygame.draw.rect(self.minimap, self.palette[self.data[y][x]], (x, y, 1, 1))
		
		for y in range(self.currentsprite[1]*8, (self.currentsprite[1]*8)+8):
			for x in range(self.currentsprite[0]*8, (self.currentsprite[0]*8)+8):
				pygame.draw.rect(self.editor, self.palette[self.data[y][x]], (x-self.currentsprite[0]*8, y-self.currentsprite[1]*8, 1, 1))
		
		pygame.draw.rect(self.display, (255, 255, 255), (18, 118, 260, 260))
		pygame.draw.rect(self.display, (255, 255, 255), (342, 118, self.editor.get_rect().w*32+4, self.editor.get_rect().h*32+4))
		self.display.blit(pygame.transform.scale(self.minimap, (self.minimap.get_rect().w*2, self.minimap.get_rect().h*2)), (20, 120))
		self.display.blit(pygame.transform.scale(self.editor, (self.editor.get_rect().w*32, self.editor.get_rect().h*32)), (344, 120))

		#draw cursor around selected sprite

		#####
		#1#3#
		##S##
		#2#4#
		#####
		
		#upper left corner
		pygame.draw.line(self.display, self.palette[self.cursor], (19+(self.currentsprite[0]*16), 119+self.currentsprite[1]*16), (22+(self.currentsprite[0]*16), 119+self.currentsprite[1]*16))
		pygame.draw.line(self.display, self.palette[self.cursor], (19+(self.currentsprite[0]*16), 119+self.currentsprite[1]*16), (19+(self.currentsprite[0]*16), 121+self.currentsprite[1]*16))
		#lower left corner
		pygame.draw.line(self.display, self.palette[self.cursor], (19+(self.currentsprite[0]*16), 136+self.currentsprite[1]*16), (21+(self.currentsprite[0]*16), 136+self.currentsprite[1]*16))
		pygame.draw.line(self.display, self.palette[self.cursor], (19+(self.currentsprite[0]*16), 136+self.currentsprite[1]*16), (19+(self.currentsprite[0]*16), 134+self.currentsprite[1]*16))
		#upper right corner
		pygame.draw.line(self.display, self.palette[self.cursor], (36+(self.currentsprite[0]*16), 119+self.currentsprite[1]*16), (34+(self.currentsprite[0]*16), 119+self.currentsprite[1]*16))
		pygame.draw.line(self.display, self.palette[self.cursor], (36+(self.currentsprite[0]*16), 119+self.currentsprite[1]*16), (36+(self.currentsprite[0]*16), 121+self.currentsprite[1]*16))
		#lower right corner
		pygame.draw.line(self.display, self.palette[self.cursor], (36+(self.currentsprite[0]*16), 136+self.currentsprite[1]*16), (34+(self.currentsprite[0]*16), 136+self.currentsprite[1]*16))
		pygame.draw.line(self.display, self.palette[self.cursor], (36+(self.currentsprite[0]*16), 136+self.currentsprite[1]*16), (36+(self.currentsprite[0]*16), 134+self.currentsprite[1]*16))

		for i in range (0, 8):
			if self.color == i:
				pygame.draw.rect(self.display, self.palette[1], (298, 120+30*i, 26, 26))
				pygame.draw.rect(self.display, self.palette[i], (300, 122+30*i, 22, 22))
			else:
				pygame.draw.rect(self.display, self.palette[1], (304, 124+30*i, 14, 14))
				pygame.draw.rect(self.display, self.palette[i], (306, 126+30*i, 10, 10))
		
		
		#update dislpay
		pygame.display.update()

if __name__ == "__main__":
	from tkinter import *
	from tkinter import filedialog
	Main(((0, 0, 0), (255, 255, 255), (173, 173, 173), (81, 81, 81), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)))
	pygame.quit()
#this program was made ENTIERLY by Geek_Joystick, DON'T STEAL IT, and credit me.
