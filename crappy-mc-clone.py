import pygame
import sys
import random
from network import Network
from tkinter import *
import json

username_ = ""

root = Tk()
root.title("Username")
root.resizable(width = False, height = False)
root["bg"] = "white"

def username():
	global username_
	if ent.get() != "":
		username_ = ent.get()
		root.destroy()

lbl = Label(root, text = "Username", bg = "white", font = ("Arial", 18))
ent = Entry(root, font = ("Arial", 18))
lbl.grid(column = 0, row = 0)
ent.grid(column = 1, row = 0)
btn = Button(root, text = "Enter", font = ("Arial", 18), command = username)
btn.grid(column = 0, row = 1)

root.mainloop()

pygame.init()

res = width, height = 720, 560
display = pygame.display
screen = display.set_mode(res)
clock = pygame.time.Clock()
fps = 60


class Wall:
	def __init__(self, x, y, width, height):
		self.x, self.y, self.width, self.height = x, y, width, height
		self.x = self.x - (self.x % 60)
		self.y = self.y - (self.y % 60)
		self.x, self.y = int(self.x), int(self.y)

	def update(self): ...

	def draw(self):
		pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))


class TexturedBlock(Wall):
	def __init__(self, x, y, texture = "Resources/grass.png"):
		super().__init__(x, y, 60, 60)
		self.image = pygame.image.load(texture)
		self.image = pygame.transform.scale(self.image, (60, 60))
		self.texture = texture

	def draw(self):
		screen.blit(self.image, (self.x, self.y))


class Background:
	def __init__(self, texture = "Resources/background-grass.png", size = 60):
		self.image = pygame.image.load(texture)
		self.image = pygame.transform.scale(self.image, (size, size))
		self.cols, self.rows = width // size, height // size
		self.size = size

	def draw(self):
		for i in range(width // self.size + 1):
			for j in range(height // self.size + 1):
				screen.blit(self.image, (i * self.size, j * self.size))



walls = []



class Player:
	def __init__(self, main = False, x = width // 2, y = height // 2, tag = f"Player {random.randint(1000, 10000)}"):
		self.tag = tag
		self.x = x
		self.y = y
		self.speed = 4
		self.dx, self.dy = 0, 0
		
		self.player_up_1 = pygame.image.load("Resources/boy_up_1.png")
		self.player_up_1 = pygame.transform.scale(self.player_up_1, (60, 60))
		self.player_up_2 = pygame.image.load("Resources/boy_up_2.png")
		self.player_up_2 = pygame.transform.scale(self.player_up_2, (60, 60))
		self.player_down_1 = pygame.image.load("Resources/boy_down_1.png")
		self.player_down_1 = pygame.transform.scale(self.player_down_1, (60, 60))
		self.player_down_2 = pygame.image.load("Resources/boy_down_2.png")
		self.player_down_2 = pygame.transform.scale(self.player_down_2, (60, 60))
		self.player_left_1 = pygame.image.load("Resources/boy_left_1.png")
		self.player_left_1 = pygame.transform.scale(self.player_left_1, (60, 60))
		self.player_left_2 = pygame.image.load("Resources/boy_left_2.png")
		self.player_left_2 = pygame.transform.scale(self.player_left_2, (60, 60))
		self.player_right_1 = pygame.image.load("Resources/boy_right_1.png")
		self.player_right_1 = pygame.transform.scale(self.player_right_1, (60, 60))
		self.player_right_2 = pygame.image.load("Resources/boy_right_2.png")
		self.player_right_2 = pygame.transform.scale(self.player_right_2, (60, 60))

		self.frame = 1
		self.framecounter = 0
		self.lastdrawn = None
		self.clicked = False
		self.main = main

	def move(self):
		self.dx, self.dy = 0, 0
		keys = pygame.key.get_pressed()
		if keys[pygame.K_w]:
			self.dy -= self.speed
			hit = False
			nextx = self.x + self.dx
			nexty = self.y + self.dy
			if walls != []:
				for wall in walls:
					if pygame.Rect(nextx - 30, nexty - 30, 60, 60).colliderect(pygame.Rect(wall.x, wall.y, wall.width, wall.height)):
						hit = True
						break
			if hit:
				self.dy = 0

		elif keys[pygame.K_s]:
			self.dy += self.speed
			hit = False
			nextx = self.x + self.dx
			nexty = self.y + self.dy
			if walls != []:
				for wall in walls:
					if pygame.Rect(nextx - 30, nexty - 30, 60, 60).colliderect(pygame.Rect(wall.x, wall.y, wall.width, wall.height)):
						hit = True
						break
			if hit:
				self.dy = 0

		elif keys[pygame.K_a]:
			self.dx -= self.speed
			hit = False
			nextx = self.x + self.dx
			nexty = self.y + self.dy
			if walls != []:
				for wall in walls:
					if pygame.Rect(nextx - 30, nexty - 30, 60, 60).colliderect(pygame.Rect(wall.x, wall.y, wall.width, wall.height)):
						hit = True
						break
			if hit:
				self.dx = 0

		elif keys[pygame.K_d]:
			self.dx += self.speed
			hit = False
			nextx = self.x + self.dx
			nexty = self.y + self.dy
			if walls != []:
				for wall in walls:
					if pygame.Rect(nextx - 30, nexty - 30, 60, 60).colliderect(pygame.Rect(wall.x, wall.y, wall.width, wall.height)):
						hit = True
						break
			if hit:
				self.dx = 0

		self.x += self.dx
		self.y += self.dy


	def mousehandler(self):
		for i in pygame.event.get():
			if i.type == pygame.MOUSEBUTTONDOWN and self.clicked == False:
				self.clicked = True

				mouse = pygame.mouse.get_pressed()
				if mouse[2]:
					wall = TexturedBlock(*pygame.mouse.get_pos())
					walls.append(wall)
					#print(walls)
					
				elif mouse[0]:
					for wall in walls:
						if wall.x == pygame.mouse.get_pos()[0] - (pygame.mouse.get_pos()[0] % 60) and wall.y == pygame.mouse.get_pos()[1] - (pygame.mouse.get_pos()[1] % 60):
							walls.remove(wall)
							break
			
			if i.type == pygame.MOUSEBUTTONUP:
				self.clicked = False

			if i.type == pygame.QUIT:
				pygame.quit()
				sys.exit()


	def draw(self):
		if self.framecounter >= 15:
			if self.frame == 1: self.frame = 2
			else: self.frame = 1
			self.framecounter = 0

		if self.dy < 0:
			if self.frame == 1:
				screen.blit(self.player_up_1, (self.x - 30, self.y - 30, 60, 60))
				self.lastdrawn = self.player_up_1
			elif self.frame == 2:
				screen.blit(self.player_up_2, (self.x - 30, self.y - 30, 60, 60))
				self.lastdrawn = self.player_up_2
		elif self.dy > 0:
			if self.frame == 1:
				screen.blit(self.player_down_1, (self.x - 30, self.y - 30, 60, 60))
				self.lastdrawn = self.player_down_1
			elif self.frame == 2:
				screen.blit(self.player_down_2, (self.x - 30, self.y - 30, 60, 60))
				self.lastdrawn = self.player_down_2
		elif self.dx < 0:
			if self.frame == 1:
				screen.blit(self.player_left_1, (self.x - 30, self.y - 30, 60, 60))
				self.lastdrawn = self.player_left_1
			elif self.frame == 2:
				screen.blit(self.player_left_2, (self.x - 30, self.y - 30, 60, 60))
				self.lastdrawn = self.player_left_2
		elif self.dx > 0:
			if self.frame == 1:
				screen.blit(self.player_right_1, (self.x - 30, self.y - 30, 60, 60))
				self.lastdrawn = self.player_right_1
			elif self.frame == 2:
				screen.blit(self.player_right_2, (self.x - 30, self.y - 30, 60, 60))
				self.lastdrawn = self.player_right_2

		else:
			if self.lastdrawn != None:
				screen.blit(self.lastdrawn, (self.x - 30, self.y - 30, 60, 60))
			else:
				screen.blit(self.player_down_1, (self.x - 30, self.y - 30, 60, 60))

		font = pygame.font.Font("freesansbold.ttf", 16)
		text = font.render(self.tag, True, "black")
		rect = text.get_rect()
		screen.blit(text, (self.x - rect.width // 2, self.y - 40 - rect.height))

		self.framecounter += 1

	def update(self):
		if self.main:
			self.move()
			self.mousehandler()
		

def read_pos(string):
	string = string.split(",")
	return int(string[0]), int(string[1]), int(string[2]), int(string[3]), str(string[4])

def make_pos(tup):
	return f"{tup[0]}, {tup[1]}, {tup[2]}, {tup[3]}, {tup[4]}"

n = Network()
startpos = read_pos(n.get_pos())

player = Player(x = startpos[0], y = startpos[1], main = True, tag = username_)
player2 = Player(x = startpos[0], y = startpos[1])
background = Background()

def update():
	player.update()
	player2.update()
	if walls != []:
		for wall in walls:
			wall.update()

def draw():
	background.draw()
	player.draw()
	player2.draw()
	if walls != []:
		for wall in walls:
			wall.draw()

def send_walls():
	global walls
	newlst = []
	for el in walls:
		newlst.append((el.x, el.y, el.texture))
	recvwalls = json.loads(n.send(json.dumps(newlst)))
	newlst_ = []
	for el in recvwalls:
		newlst_.append(TexturedBlock(int(el[0]), int(el[1]), texture = str(el[2])))
	walls = newlst_

while True:
	player2pos = read_pos(n.send(make_pos((player.x, player.y, player.dx, player.dy, player.tag))))
	player2.x, player2.y, player2.dx, player2.dy, player2.tag = player2pos
	send_walls()

	screen.fill((0, 0, 0))
	update()
	draw()

	for ev in pygame.event.get():
		if ev.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	display.update()
	clock.tick(fps)