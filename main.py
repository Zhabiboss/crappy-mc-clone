import pygame
import sys
import random

pygame.init()

res = width, height = 720, 560
display = pygame.display
screen = display.set_mode(res)
clock = pygame.time.Clock()
fps = 60

def roundnumber(n, n2):
	if n < n2 / 2: return 0
	else: return n2
	

class Wall:
	def __init__(self, x, y, width, height):
		self.x, self.y, self.width, self.height = x, y, width, height
		if self.x < 1: self.x = 0
		elif self.x == 60: self.x = 60
		elif self.x > 60: 
			tmp = self.x // 60
			remainder = self.x - tmp * 60
			tmp1 = self.x - remainder
			remainder = roundnumber(remainder, 60)
			self.x = tmp1 + remainder
		if self.y < 1: self.y = 0
		elif self.y == 60: self.y = 60
		elif self.y > 60: 
			tmp = self.y // 60
			remainder = self.y - tmp * 60
			tmp1 = self.y - remainder
			remainder = roundnumber(remainder, 60)
			self.y = tmp1 + remainder
		self.x, self.y = int(self.x), int(self.y)

	def update(self): ...

	def draw(self):
		pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))


class TexturedBlock(Wall):
	def __init__(self, x, y, texture = "Resources/grass.png"):
		super().__init__(x, y, 60, 60)
		self.image = pygame.image.load(texture)
		self.image = pygame.transform.scale(self.image, (60, 60))

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



walls = [TexturedBlock(0, 0), TexturedBlock(width - 150, height - 150)]



class Player:
	def __init__(self, tag = f"Player {random.randint(1000, 10000)}"):
		self.tag = tag
		self.x = width // 2
		self.y = height // 2
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
				screen.blit(self.player_up_1, (self.x - 30, self.y - 30, 60, 60))

		self.framecounter += 1

	def update(self):
		self.move()

	def __repr__(self):
		return (self.tag, (self.x, self.y))



player = Player()
background = Background()

def update():
	player.update()
	if walls != []:
		for wall in walls:
			wall.update()

def draw():
	background.draw()
	player.draw()
	if walls != []:
		for wall in walls:
			wall.draw()

while True:
	screen.fill((0, 0, 0))
	update()
	draw()

	for ev in pygame.event.get():
		if ev.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	display.update()
	clock.tick(fps)