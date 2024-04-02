import pygame, sys

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
      
  screen.fill("white")

  pygame.display.update()
  pygame.time.Clock().tick(60)