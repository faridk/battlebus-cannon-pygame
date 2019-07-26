import sys, time, pygame

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
		self.speed = 0

	def draw(self):
		Game.surface.blit(self.sprite, (self.x, self.y))

	
class Player(Sprite):
	bullets = []
	enemies = []
	def __init__(self, name, path, x, y, w, h):
		super(Player, self).__init__(name, path, x, y, w, h)
		self.direction_left = False
		self.flipped_sprite = pygame.transform.flip(self.sprite, True, False) 
		self.bullets_per_second = 5
		self.speed = 5
		self.add_enemies()

	def draw(self):
		if self.direction_left:
			# Draw flipped
			Game.surface.blit(self.flipped_sprite, (self.x, self.y))
		else:
			# Draw normal
			super(Player, self).draw()
	
	def shoot(self):
		bullet = Bullet("bullet", Game.SPRITE_FOLDER + "Bullet.png", self.x + self.w // 2, self.y, 4, 10)
		print(time.time() - Game.timer)
		if time.time() - Game.timer > 1 / self.bullets_per_second:
			Player.bullets.append(bullet)
			Game.timer = time.time()
		
	def add_enemies(self):
		alien = Alien("alien", Game.SPRITE_FOLDER + "Spaceship.png", 100, 25, 100, 100)
		gargoyle = Gargoyle("gargoyle", Game.SPRITE_FOLDER + "Gargoyle.png", 100, 100, 100, 100)
		Player.enemies.append(alien)
	

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
	def __init__(self, name, path, x, y, w, h):
		super(Alien, self).__init__(name, path, x, y, w, h)
		self.speed = 1

	
class Gargoyle(Enemy):
	def __init__(self, name, path, x, y, w, h):
		super(Gargoyle, self).__init__(name, path, x, y, w, h)
		self.speed = 200
class Bullet(Sprite):
	def __init__(self, name, path, x, y, w, h):
		super(Bullet, self).__init__(name, path, x, y, w, h)
		self.speed = 10
	
	def draw(self):
		self.y -= self.speed
		super(Bullet, self).draw()

	def hit(self):
		pass
	
game = Game()