import sys, time, pygame
from decimal import Decimal
from random import random, randint

pygame.init()
pygame.font.init()


class Game:
	SPRITE_FOLDER = 'sprites/'
	surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
	timer = time.time()
	def __init__ (self):
		self.font = pygame.font.SysFont('Comic Sans MS', 30)
		Game.WIDTH, Game.HEIGHT = pygame.display.get_surface().get_size()
		self.background_color = (0, 0, 0)
		self.score = 0
		self.player = Player("player", Game.SPRITE_FOLDER + "BattleBus.png", self.WIDTH - 160, self.HEIGHT - 140, 160, 140)
		self.start()

	def start(self):
		while True:
			self.draw()
			self.player.draw()
	
			# Draw all bullets in the air
			for bullet in Player.bullets:
				bullet.draw()

			# Draw all enemies of the Player
			for enemy in Player.enemies:
				enemy.draw()

	def quit(self):
		pygame.quit() # Close window
		sys.exit()

	def draw(self):
		for event in pygame.event.get():
			# Handle exit
			if event.type == pygame.QUIT:
				self.quit()
	
		# Handle bar movement using keysself.player = Player(self, "player", Game.SPRITE_FOLDER + "BattleBus.png", self.WIDTH - 160, self.HEIGHT - 140, 160, 140)
		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_q] or pressed[pygame.K_ESCAPE]:
			self.quit()
		if pressed[pygame.K_RIGHT]:
			self.player.x += self.player.speed
			self.player.direction_left = False
		if pressed[pygame.K_LEFT]:
			self.player.x -= self.player.speed
			self.player.direction_left = True
		if pressed[pygame.K_SPACE]:
			self.player.shoot()

		pygame.display.flip() # Updates the display
		self.surface.fill(self.background_color) # Clear the screen, leave no smudges
	
class Sprite:
	def __init__(self, name, path, x, y, w, h):
		self.name = name
		self.sprite = pygame.image.load(path)
		self.sprite = pygame.transform.scale(self.sprite, (w, h))
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.speed = 1
		self.debug_font = pygame.font.SysFont("monospace", 15)

	def draw(self):
		Game.surface.blit(self.sprite, (self.x, self.y))
		self.draw_debug_labels()
	
	# Draws debug info (like print but on the screen)
	def draw_debug_labels(self):
		TWOPLACES = Decimal(10) ** -2
		x = Decimal(self.x).quantize(TWOPLACES)
		y = Decimal(self.y).quantize(TWOPLACES)
		speed = Decimal(self.speed).quantize(TWOPLACES)
		location_label = self.debug_font.render('X: %s Y: %s' % (x, y), 1, (255, 255, 0))
		speed_label = self.debug_font.render('V: %s' % (speed), 1, (255, 255, 0))
		count_label = self.debug_font.render('Count: %s' % (Alien.instance_count), 1, (255, 255, 0))
		Game.surface.blit(location_label, (self.x + self.w, self.y + self.h))
		Game.surface.blit(speed_label, (self.x + self.w, self.y + self.h + 20))
		Game.surface.blit(count_label, (self.x + self.w, self.y + self.h + 40))


class Player(Sprite):
	bullets = []
	enemies = []
	def __init__(self, name, path, x, y, w, h):
		super(Player, self).__init__(name, path, x, y, w, h)
		self.direction_left = False
		self.flipped_sprite = pygame.transform.flip(self.sprite, True, False) 
		self.bullets_per_second = 5
		self.speed = 5
		self.add_enemies(2, 2)

	def draw(self):
		if self.direction_left:
			# Draw flipped
			Game.surface.blit(self.flipped_sprite, (self.x, self.y))
		else:
			# Draw normal
			super(Player, self).draw()

	def shoot(self):
		bullet = Bullet("bullet", Game.SPRITE_FOLDER + "Bullet.png", self.x + self.w // 2, self.y, 4, 10)
		# print(time.time() - Game.timer)
		if time.time() - Game.timer > 1 / self.bullets_per_second:
			Player.bullets.append(bullet)
			Game.timer = time.time()
		
	def add_enemies(self, alien_count, gargoyle_count):
		for i in range(alien_count):
			alien = Alien("alien", Game.SPRITE_FOLDER + "Spaceship.png", randint(0, Game.WIDTH), randint(0, Game.HEIGHT // 4), 100, 100)
			alien.speed = random() + 0.5
			Player.enemies.append(alien)
		for i in range(gargoyle_count):
			gargoyle = Gargoyle("gargoyle", Game.SPRITE_FOLDER + "Gargoyle.png", randint(0, Game.WIDTH), randint(0, Game.HEIGHT // 4), 100, 100)
			gargoyle.speed = random() + 0.5
			Player.enemies.append(gargoyle)

class Enemy(Sprite):
	def __init__(self, name, path, x, y, w, h):
		super(Enemy, self).__init__(name, path, x, y, w, h)
		self.right = True
		self.left = False
		self.up = False
		self.down = False
		self.last_y = 0
	
	def draw(self):
		super(Enemy, self).draw()
		# Move in a defined direction
		if self.right:
			self.x += self.speed
		elif self.left:
			self.x -= self.speed
		if self.up:
			self.y -= self.speed
		elif self.down:
			self.y += self.speed
		# Bounce by setting directions
		if self.x > Game.WIDTH - self.w:
			self.right = False
			# Move down
			self.down = True
		if self.x < 0:
			self.left = False
			# Move down
			self.down = True
		# Move down only 100 pixels
		if self.y - self.last_y > 100:
			self.down = False
			self.last_y = self.y
			if self.x < 0:
				self.right = True
			if self.x > Game.WIDTH - self.w:
				self.left = True


class Alien(Enemy):
	instance_count = 0
	def __init__(self, name, path, x, y, w, h):
		super(Alien, self).__init__(name, path, x, y, w, h)
		Alien.instance_count += 1

	def draw(self):
		super(Alien, self).draw()


class Gargoyle(Enemy):
	instance_count = 0
	def __init__(self, name, path, x, y, w, h):
		super(Gargoyle, self).__init__(name, path, x, y, w, h)
		Gargoyle.instance_count += 1

class Bullet(Sprite):
	def __init__(self, name, path, x, y, w, h):
		super(Bullet, self).__init__(name, path, x, y, w, h)
		self.speed = 2
	
	def draw(self):
		self.y -= self.speed
		super(Bullet, self).draw()

	def hit(self):
		pass
	
game = Game()