import sys, time, pygame

pygame.init()
pygame.font.init()


class Game:
	SPRITE_FOLDER = "sprites/"
	surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
	timer = time.time()
	def __init__ (self):
		self.font = pygame.font.SysFont('Comic Sans MS', 30)
		self.WIDTH, self.HEIGHT = pygame.display.get_surface().get_size()
		self.background_color = (0, 0, 0)
		self.score = 0
		self.player = Player("player", self.SPRITE_FOLDER + "BattleBus.png", \
			self.WIDTH - 160, self.HEIGHT - 140, 160, 140)
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
				if enemy.x == 100:
					enemy.x += 1
					enemy.y -= 10
				if enemy.x == self.WIDTH - enemy.w:
					enemy.y -= 10
					enemy.x -= 1
			enemy.draw()
			
			
	def quit(self):
			pygame.quit() # Close the window
			sys.exit()
	
	def draw(self):
		for event in pygame.event.get():
				# Handle exit
				if event.type == pygame.QUIT:
						self.quit()
		
		# Handle bar movement using keysself.player = Player(self, "player",
		# "BattleBus.png", self.WIDTH - 160, self.HEIGHT - 140, 160, 140)
		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_RIGHT]:
				self.player.x += self.player.x_velocity
				self.player.direction_left = False
		if pressed[pygame.K_LEFT]:
				self.player.x -= self.player.x_velocity
				self.player.direction_left = True
		if pressed[pygame.K_SPACE]:
				self.player.shoot()

		pygame.display.flip() # Updates the display
		self.surface.fill(self.background_color) # Clear the screen, leave no smudges

		
class Sprite:
	def __init__(self, name, path, x, y, w, h, moving):
		self.name = name
		self.sprite = pygame.image.load(path)
		self.sprite = pygame.transform.scale(self.sprite, (w, h))
		self.x = x
		self.y = y
		self.w = w 
		self.h = h 
		self.x_velocity = 0
		self.y_velocity = 0
		self.moving = moving
	
	def move(self):
		self.x += self.x_velocity
		self.y += self.y_velocity
	
	def draw(self):
		if self.moving: self.move()
		Game.surface.blit(self.sprite, (self.x, self.y))

		
class Player(Sprite):
	bullets = []
	enemies = []
	def __init__(self, name, path, x, y, w, h, moving=True):
		super(Player, self).__init__(name, path, moving, x, y, w, h)
		self.direction_left = False
		self.flipped_sprite = pygame.transform.flip(self.sprite, True, False)
		self.bullets_per_second = 5
		self.x_velocity = 5
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
	  alien = Alien("alien", Game.SPRITE_FOLDER + "Spaceship.png", 100, 100)
	  gargoyle = Gargoyle("gargoyle", Game.SPRITE_FOLDER + "Gargoyle.png", 100, 100, 100, 100)
	  Player.enemies.extend((alien, gargoyle))

class Alien(Sprite):
	def __init__(self, name, path, x=100, y=100, w=100, h=100, moving=True):
		super(Alien, self).__init__(name, path, moving, x, y, w, h)
		self.x_velocity = 2
	
class Gargoyle(Sprite):
	def __init__(self, name, path, x=100, y=100, w=100, h=100, moving=True):
		super(Gargoyle, self).__init__(name, path, moving, x, y, w, h)
		self.x_velocity = 3.5
	
class Bullet(Sprite):
	def __init__(self, name, path, x, y, w, h, moving=True):
		super(Bullet, self).__init__(name, path, x, y, w, h, moving)
		self.x_velocity = 10

	def draw(self):
		self.x -= self.x_velocity
		super(Bullet, self).draw()

	def hit(self):
		pass
		
			
game = Game() 