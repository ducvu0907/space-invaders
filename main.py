import pygame, sys

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

# player
class Player():
  def __init__(self):
    self.image = pygame.image.load("home/kira/workspace/projects/space_invaders/assets/player.png").convert_alpha()
    self.rect = self.image.get_rect()
    self.speed = 5

# enemies
class Enemy:
  def __init__(self):
    pass

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
      
  screen.fill("white")

  pygame.display.update()
  pygame.time.Clock().tick(60)