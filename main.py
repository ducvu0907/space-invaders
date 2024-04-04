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
    self.ammo = None
    self.speed = 7

  def move(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
      self.rect.right += self.speed if self.rect.right < screen_width else 0
    elif keys[pygame.K_LEFT]:
      self.rect.left -= self.speed if self.rect.left >= 0 else 0
    if keys[pygame.K_SPACE]:
      self.shoot()
  
  def shoot(self):
    print('shooting')

# enemies
class Enemy:
  def __init__(self):
    pass

# create instances
player = Player()

def update():
  screen.blit(player.image, player.rect)
  player.move()

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