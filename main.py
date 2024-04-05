import pygame, sys

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")

# player
class Player():
  def __init__(self):
    self.image = pygame.image.load("assets/player.png").convert_alpha()
    self.rect = self.image.get_rect(midbottom=(screen_width // 2, screen_height))
    self.speed = 7
    self.ammos = []
    self.ready = True
    self.shoot_time = 0
    self.cooldown = 400

  def move(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
      self.rect.right += self.speed if self.rect.right < screen_width else 0
    elif keys[pygame.K_LEFT]:
      self.rect.left -= self.speed if self.rect.left >= 0 else 0
    if keys[pygame.K_SPACE] and self.ready:
      self.shoot()
      self.ready = False
      self.shoot_time = pygame.time.get_ticks()
  
  def recharge(self):
    if not self.ready:
      curr_time = pygame.time.get_ticks()
      if curr_time - self.shoot_time >= self.cooldown:
        self.ready = True

  def shoot(self):
    self.ammos.append(Ammo(self.rect.center))
  
# ammo
class Ammo:
  def __init__(self, pos):
    self.image = pygame.Surface((4, 20))
    self.image.fill("white")
    self.rect = self.image.get_rect(midbottom=pos)
    self.speed = -9

# enemies
class Enemy:
  def __init__(self):
    pass

# create instances
player = Player()

def update():
  screen.blit(player.image, player.rect)
  player.recharge()
  player.move()
  for ammo in player.ammos:
    screen.blit(ammo.image, ammo.rect)
    ammo.rect.y += ammo.speed
    # delete ammo when out of bound
    if ammo.rect.bottom <= 0:
      player.ammos.remove(ammo)
      del ammo

def run():
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    screen.fill("black")
    update()
    pygame.display.flip()
    pygame.time.Clock().tick(60)
  
if __name__ == "__main__":
  run()