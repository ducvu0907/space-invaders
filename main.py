import pygame, sys
from random import randint
pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")

class Player():
  def __init__(self):
    self.image = pygame.image.load("assets/player.png").convert_alpha()
    self.rect = self.image.get_rect(midbottom=(screen_width // 2, screen_height))
    self.speed = 7
    self.ammos = []
    self.ready = True
    self.shoot_time = 0
    self.cooldown = 400
    self.lives = 5
    self.healthbar = [1, 1, 1, 1, 1]

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
  
class Ammo:
  def __init__(self, pos):
    self.image = pygame.Surface((4, 20))
    self.image.fill("white")
    self.rect = self.image.get_rect(midbottom=pos)
    self.speed = -9
  def collide_enemy(self):
    for i, row in enumerate(enemies):
      for j, enemy in enumerate(row):
        if isinstance(enemy, Enemy):
          if pygame.Rect.colliderect(self.rect, enemy.rect):
            row[j] = None
            return True
    return False
  def collide_player(self):
    if pygame.Rect.colliderect(self.rect, player.rect):
      return True
    return False

class Enemy:
  def __init__(self, color, pos):
    self.enemies = []
    self.image = pygame.image.load(f"assets/{color}.png").convert_alpha()
    self.rect = self.image.get_rect(center=pos)
    self.ammo = None
  def move(self, dir):
    self.rect.x += dir
  def shoot(self):
    self.ammo = Ammo(self.rect.center)

# game components
player = Player()
score = 0
font = pygame.font.Font("font/Pixeled.ttf", 14)
enemies_formation = [
  ['yellow' for _ in range(10)],
  ['green' for _ in range(10)],
  ['green' for _ in range(10)],
  ['red' for _ in range(10)],
  ['red' for _ in range(10)],
  ['red' for _ in range(10)],
]
enemies = [
  ['yellow' for _ in range(10)],
  ['green' for _ in range(10)],
  ['green' for _ in range(10)],
  ['red' for _ in range(10)],
  ['red' for _ in range(10)],
  ['red' for _ in range(10)],
]
enemy_movement = pygame.USEREVENT + 1
enemy_shooting = pygame.USEREVENT + 2 # random enemy shooting
enemy_regen = pygame.USEREVENT + 3
pygame.time.set_timer(enemy_movement, 1000)
pygame.time.set_timer(enemy_shooting, 500)
pygame.time.set_timer(enemy_regen, 50000) # regen all enemies every 50s
direction = 1

# update game
def check_endgame():
  if player.lives == 0:
    print("You lost!")
    return True
  elif all(all(not enemy for enemy in row) for row in enemies):
    print("You won!")
    return True
  return False

def update():
  def update_player():
    screen.blit(player.image, player.rect)
    player.recharge()
    player.move()
    for i, health in enumerate(player.healthbar):
      if health == 1:
        pygame.draw.rect(screen, "red", (screen_width - (i + 1) * 30, 0, 30, 20))
      pygame.draw.rect(screen, "white", (screen_width - (i + 1) * 30, 0, 30, 20), 2)
  def update_ammo():
    for ammo in player.ammos:
      screen.blit(ammo.image, ammo.rect)
      ammo.rect.y += ammo.speed
      if ammo.collide_enemy():
        global score
        score += 50
        player.ammos.remove(ammo)
        del ammo
      elif ammo.rect.bottom <= 0:
        player.ammos.remove(ammo)
        del ammo
  def update_score():
    score_sf = font.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_sf.get_rect(topleft=(0, 0))
    screen.blit(score_sf, score_rect)
  def update_enemies():
    for i, row in enumerate(enemies):
      for j, enemy in enumerate(row):
        if isinstance(enemy, str):
          enemy = Enemy(enemy, (j * 70 + 55, i * 50 + 60))
          row[j] = enemy
        elif isinstance(enemy, Enemy):
          enemy.move(direction)
          if enemy.ammo is not None:
            enemy.ammo.rect.bottom -= enemy.ammo.speed
            screen.blit(enemy.ammo.image, enemy.ammo.rect)
            if enemy.ammo.collide_player():
              enemy.ammo = None
              player.lives -= 1
              player.healthbar[player.lives] = 0
              print("You took damage!")
            elif enemy.ammo.rect.top >= screen_height:
              enemy.ammo = None
          screen.blit(enemy.image, enemy.rect)
  update_player()
  update_ammo()
  update_score()
  update_enemies()

def run():
  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == enemy_movement:
        global direction
        direction *= -1
      if event.type == enemy_shooting:
        x, y = randint(0, 5), randint(0, 9)
        while not isinstance(enemies[x][y], Enemy):
          x, y = randint(0, 5), randint(0, 9)
        enemies[x][y].shoot()
      if event.type == enemy_regen:
        for i, row in enumerate(enemies):
          for j, enemy in enumerate(row):
            if enemy is None:
              row[j] = enemies_formation[i][j]

    if check_endgame():
      running = False
      print(f"Your score is ${score}")

    screen.fill("black")
    update()
    pygame.display.flip()
    pygame.time.Clock().tick(60)
  
if __name__ == "__main__":
  run()