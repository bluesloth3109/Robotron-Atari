import pygame
from random import randint
pygame.init()

WIDTH, HEIGHT = 800, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robotron")
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#sizes
playerwidth = 22
playerheight = 32
width28 = 28
height36 = 36
no_34 = 34

#Images
playerimg_front = pygame.transform.scale(pygame.image.load('playerfront.png'), (22,32))
playerimg_left = pygame.transform.scale(pygame.image.load('playerleft.png'), (22,32))
playerimg_right = pygame.transform.scale(pygame.image.load('playerright.png'), (22,32))
playerimg_back = pygame.transform.scale(pygame.image.load('playerback.png'), (22,32))
enemyimg = pygame.transform.scale(pygame.image.load('enemyimg.png'), (32,32))
playimg = pygame.image.load('play.png')
#Hitboxes
#player_rect = pygame.draw.rect(win, (0, 0, 255,), player.hitbox, 2)
#enemy_rect = pygame.draw.rect(win, (255, 0, 0), enemy.hitbox, 2)

class Player(pygame.sprite.Sprite):
	playervel = 3
	playerwidth = 1
	playerheight = 1

	def __init__(self,image ,x, y, height, width):
		self.x = self.origin_x = x
		self.y = self.origin_y = y
		self.width = playerwidth
		self.height = playerheight
		self.hitbox = (self.x-2, self.y-2, 28,36)
		self.image = playerimg_front
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]

	def move_x(self, right=True):
		if right:
			self.x -= self.playervel
		else:
			self.x += self.playervel
	def move_y(self, up=True):
		if up:
			self.y -= self.playervel
		else:
			self.y += self.playervel
	def draw(self, win):
		self.hitbox = (self.x-2, self.y-2, 28,36)
		#pygame.draw.rect(win, (255,0,0), self.hitbox,2)
		win.blit(playerimg_front, (self.x, self.y))

	def create_bullet(self):
		return Bullet(self.x, self.y)

class Enemy(pygame.sprite.Sprite):
	def __init__(self, image, x, y):
		super().__init__()
		self.x = x
		self.y = y
		self.enemyvel = 1
		self.hitbox = (self.x, self.y, 34,34)
		self.image = enemyimg
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]

	def move_x(self, right=True):
		if right:
			self.x += self.enemyvel
		else:
			self.x -= self.enemyvel
	def move_y(self, Above=True):
		if Above:
			self.y += self.enemyvel
		else:
			self.y -= self.enemyvel
	def draw(self, win):
		self.hitbox = (self.x, self.y, 34,34)
		#pygame.draw.rect(win, (0,255,0), self.hitbox, 2)
		win.blit(enemyimg, (self.x, self.y))

def draw(win, player, enemy_group, bullet_group):
	win.fill(BLACK)
	pygame.draw.rect(win, (255, 255, 0), (0, 50, WIDTH, HEIGHT-50), 5)
	bullet_group.draw(win)
	player.draw(win)
	for curr_enemy in enemy_group:
		curr_enemy.draw(win)
	pygame.display.update()

def player_rotation(keys, player, win, x, y):
	if keys[pygame.K_w]:
		win.blit(playerimg_back, (x, y))
	if keys[pygame.K_s]:
		win.blit(playerimg_front, (x, y))
	if keys[pygame.K_d]:
		win.blit(playerimg_right, (x, y))
	if keys[pygame.K_a]:
		win.blit(playerimg_left, (x, y))
	pygame.display.update()

def player_movement(keys, player, bullet):
	if keys[pygame.K_w] and player.y - player.playervel - 1 >53:
		player.move_y(up=True)
	if keys[pygame.K_s] and player.y + player.playervel + 32 + 1 <= HEIGHT:
		player.move_y(up=False)

	if keys[pygame.K_a] and player.x - player.playervel - 1 >= 0:
		player.move_x(right=True)

	if keys[pygame.K_d] and player.x + player.playervel + 32 -8 <= WIDTH:
		player.move_x(right=False)

def enemy_movement(enemy_group, player):
	for curr_enemy in enemy_group:
		if player.y >= curr_enemy.y:
				curr_enemy.move_y(Above=True)
		if player.y <= curr_enemy.y:
				curr_enemy.move_y(Above=False)
		if player.x >= curr_enemy.x:
			curr_enemy.move_x(right=True)
		if player.x <= curr_enemy.x:
				curr_enemy.move_x(right=False)

def bullet_movemen(keys, bullet_group):
	for curr_bullet in bullet_group:
		if keys[pygame.K_w]:
			curr_bullet.move_y(up=True)
		if keys[pygame.K_s]:
			curr_bullet.move_y(up=False)
		if keys[pygame.K_d]:
			curr_bullet.move_x(right=True)
		if keys[pygame.K_a]:
			curr_bullet.move_x(right=False)
def bullet_movement(bullet):
	bullet.rect.x += bullet_vel

class Bullet(pygame.sprite.Sprite):
	bullet_vel = 5

	def __init__(self, x , y):
		super().__init__()
		self.image = pygame.Surface((3,3))
		self.image.fill((255,0,0))
		self.rect = self.image.get_rect(center = (x, y))

	def move_x(self, right = True):
		if right:
			self.rect.x += self.bullet_vel
		else:
			self.rect.x -= self.bullet_vel
	def move_y(self, up = True):
		if up:
			self.rect.y -= self.bullet_vel
		else:
			self.rect.y += self.bullet_vel
	
	def update(self):
		if self.rect.x >= WIDTH + 3 or self.rect.x <= -3:
			self.kill()

		elif self.rect.y >= HEIGHT + 3 or self.rect.y <= -3:
			self.kill()

	def draw(self, win):
		win.blit(self.image, (self.x, self.y))
	
def run_menu(menu):
	while menu:
		win.fill(BLACK)
		win.blit(playimg, (WIDTH//2, (HEIGHT-50)//2))
def main():
	run = True
	menu = False
	clock = pygame.time.Clock()

	#run_menu(menu)

	enemy_group = pygame.sprite.Group()
	player = Player("playerimg_front" ,WIDTH//2, HEIGHT//2, playerheight, playerwidth)
	for cnt in range(randint(1,10)):
		enemy = Enemy( "enemyimg.png" ,randint(0,WIDTH), randint(50,HEIGHT))
		enemy_group.add(enemy)

	bullet_group = pygame.sprite.Group()

	while menu == False:
		while run:
			clock.tick(FPS)
			draw(win, player, enemy_group, bullet_group)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
					break
				if event.type == pygame.MOUSEBUTTONDOWN:
					bullet_group.add(player.create_bullet())
					for curr_bullet in bullet_group:
						if keys[pygame.K_w]:
							curr_bullet.move_y(up=True)
						if keys[pygame.K_s]:
							curr_bullet.move_y(up=False)
						if keys[pygame.K_d]:
							curr_bullet.move_x(right=True)
						if keys[pygame.K_a]:
							curr_bullet.move_x(right=False)
			gets_hit = pygame.sprite.spritecollideany(player, enemy_group)
			print(gets_hit)
			
			keys = pygame.key.get_pressed()
			player_movement(keys, player, bullet_group)
			player_rotation(keys,player,win, player.x, player.y)
			enemy_movement(enemy_group, player)
			bullet_group.update()
		pygame.quit()

if __name__ == '__main__':
	main()
