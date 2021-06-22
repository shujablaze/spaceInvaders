import pygame
import sys
import random
import math
from pygame import mixer
import time

pygame.init()
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Cock-Busters")

# GAME VARIABLES
score1 = 0
player_x = 350
player_x_change = 0
playing = True
boss_level = False


class element_img:
    def __init__(self):
        self.background = pygame.image.load('background.png').convert()
        self.rocket = pygame.image.load('rocket.png')
        self.laser = pygame.image.load('laser.png')
        self.score_style = pygame.font.Font('freesansbold.ttf', 32)
        self.boss_health_style = pygame.font.Font('freesansbold.ttf', 30)


class Enemies:
    def __init__(self):
        self.coor_x = random.randint(20, 734)
        self.coor_y = random.randint(10, 300)
        self.change = 0.8
        self.pic = pygame.image.load('enemy.png')

    def display(self):
        screen.blit(self.pic, (self.coor_x, self.coor_y))

    def is_collision(self, laser_x, laser_y):
        self.distance = math.sqrt(math.pow(laser_x - self.coor_x, 2) + math.pow(laser_y - self.coor_y, 2))
        if self.distance < 39:
            return True
        else:
            return False


class Boss:
    def __init__(self):
        self.coor_x = 0
        self.coor_y = 0
        self.coor_dx = 1
        self.coor_dy = 1
        self.health = 15
        self.image1 = pygame.image.load('boss1.png')
        self.rect = self.image1.get_rect(center=(350, -150))

    def display(self):
        screen.blit(self.image1, self.rect)

    def is_collision(self, laser_x, laser_y):
        self.distance = math.sqrt(math.pow(laser_x - self.rect.centerx, 2) + math.pow(laser_y - self.rect.centery, 2))
        if self.distance < 39:
            return True
        else:
            return False


# GAME CHARACTERS

# BOSSES
boss1 = Boss()

# ENEMIES
enemy1 = Enemies()
enemy2 = Enemies()
enemy3 = Enemies()
enemy_list = [enemy1, enemy2, enemy3]

# GAME UTILITIES
char = element_img()

# LASER COORDINATES
state = 'ready'
laser_y = 510  # As player y is fixed at 510 px
laser_x = 0


def player(player_x):
    screen.blit(char.rocket, (player_x, 520))


def laser_reset():
    global laser_y, laser_x, state
    state = 'ready'
    laser_y = 510
    laser_x = 0


def laser(laser_x):
    screen.blit(char.laser, (laser_x + 20, laser_y))  # To center the laser to rocket's middle


def scoreBoard():
    score = char.score_style.render("Score: " + str(score1), True, (255, 255, 255))
    screen.blit(score, (10, 10))


def boss_health():
    health = char.boss_health_style.render("Health: " + str(boss1.health), True, (255, 255, 255))
    screen.blit(health, (10, 10))


def gameover():
    global playing
    playing = False
    screen.fill((0, 0, 0))

    game_over = pygame.font.Font("freesansbold.ttf", 64)
    game_over_text = game_over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (200, 250))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


def end_game():
    global playing
    playing = False
    screen.fill((0, 0, 0))

    game_over = pygame.font.Font("freesansbold.ttf", 64)
    game_over_text = game_over.render("Thanks for Playing", True, (255, 255, 255))
    screen.blit(game_over_text, (100, 250))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


def bosstext():
    # global boss_level
    screen.fill((0, 0, 0))
    intro_text_type = pygame.font.Font("freesansbold.ttf", 32)
    intro_text = intro_text_type.render("BOSS TAKKAL", True, (255, 255, 255))
    screen.blit(intro_text, (200, 250))
    pygame.display.update()
    time.sleep(2)


# New Enemy Generation
BOSSATTACK = pygame.USEREVENT + 2
add_enemy = pygame.USEREVENT + 1
pygame.time.set_timer(add_enemy, 7000)

while True:

    screen.fill((0, 0, 0))
    screen.blit(char.background, (0, 0))
    boss_health() if boss_level == True else scoreBoard()

    if not playing:
        gameover()

    if playing:

        # KEYBOARD INPUTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_x_change = -2
                if event.key == pygame.K_RIGHT:
                    player_x_change = 2
                if event.key == pygame.K_RCTRL:
                    if state == 'ready':
                        mixer.Sound('laser.wav').play()
                        state = 'fire'
                        laser_x = player_x
            if event.type == add_enemy and len(enemy_list) < 12:
                new_enemy = Enemies()
                enemy_list.append(new_enemy)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_x_change = 0

        # Player Movement
        player(player_x)
        player_x += player_x_change

        if player_x > 736:
            player_x = 736
        elif player_x < 0:
            player_x = 0

        if not boss_level:
            # Enemy Movement
            for enemy in enemy_list:
                enemy.display()
                enemy.coor_x += enemy.change

                if enemy.coor_x > 736:
                    enemy.coor_x = 736
                    enemy.change = -0.9
                    enemy.change -= 0.15
                    enemy.coor_y += 30
                elif enemy.coor_x < 0:
                    enemy.coor_x = 0
                    enemy.change = 0.9
                    enemy.change += 0.15
                    enemy.coor_y += 30

                if enemy.is_collision(laser_x, laser_y):
                    laser_reset()
                    enemy.coor_x = random.randint(20, 734)
                    enemy.coor_y = random.randint(10, 300)
                    # pygame.mixer.Sound('explode.wav').play()
                    if not score1 == 2:
                        score1 += 1
                    else:
                        score = 0
                        boss_level = True
                        bosstext()

                # ENEMY REACHES LOC
                if enemy.coor_y > 410:
                    gameover()

        if boss_level:

            pygame.time.set_timer(BOSSATTACK, random.randint(2000, 4000))

            # BOSS MOVEMENT
            boss1.display()

            if boss1.rect.top < 10:
                boss1.rect.top += 1
                boss1.coor_dy *= -1

            if boss1.rect.top > 0 and boss1.rect.right < 801 and boss1.rect.right > 0 and boss1.rect.bottom < 450:
                boss1.rect.centerx += boss1.coor_dx
                boss1.rect.centery += boss1.coor_dy

            if boss1.rect.right >= 800 or boss1.rect.left <= 0:
                boss1.coor_dx *= -1

            if boss1.rect.bottom >= 450:
                boss1.rect.bottom = 449
                boss1.coor_dy *= -1

            if boss1.is_collision(laser_x, laser_y):
                laser_reset()
                boss1.health -= 1
                if boss1.health == 0:
                    mixer.Sound('explosion.wav').play()
                    time.sleep(1)
                    end_game()

        # Laser Movement
        if state == 'fire':
            laser_y -= 1
            laser(laser_x)
        if laser_y < 0:
            laser_reset()

        pygame.display.flip()

pygame.exit()
