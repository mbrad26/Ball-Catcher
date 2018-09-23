import sys
import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group
import random
from time import sleep

WIDTH = 700
HEIGHT = 800
RED = (255, 0, 0)
BLUE = (0, 0, 255)


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Catch The Ball')
bg_color = (255, 255, 255)
catch_sound = pygame.mixer.Sound('sounds/Pickup_Coin4.wav')
drop_sound = pygame.mixer.Sound('sounds/Blip_Select16.ogg')


class Player(Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 35))
        self.rect = self.image.get_rect()
        self.image.fill(RED)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0.5
        self.speedx = 0

    def update(self):
        self.speedx = 0.00
        key_list = pygame.key.get_pressed()
        if key_list[pygame.K_RIGHT]:
            self.speedx += 1
        if key_list[pygame.K_LEFT]:
            self.speedx -= 1
        self.rect.centerx += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


class Ball(Sprite):

    def __init__(self):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load('images/sphere-04.png').convert()
        self.image = pygame.transform.scale(self.image, (35, 35))
        # self.image = pygame.Surface((25, 25))
        # self.image = pygame.draw.circle(self.screen, BLUE, (0, 0), 14)
        # self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, - self.rect.height)
        self.speedy = float(self.rect.centery)
        self.speed_y = 0.3

    def update(self):
        self.speedy += self.speed_y
        self.rect.y = self.speedy


def spawn_ball(ball):
    ball.kill()
    ball = Ball()
    balls.add(ball)


def update_ball():
    global balls_dropped
    for ball in balls.sprites():
        if ball.rect.top > HEIGHT:
            balls_dropped += 'a'
            drop_sound.play()
            spawn_ball(ball)
            sleep(0.5)
        elif pygame.sprite.groupcollide(player_group, balls, False, True):
            catch_sound.play()
            spawn_ball(ball)


def game_over():
    if len(balls_dropped) < 3:
        return True
    else:
        return False


balls_dropped = ''
player = Player()
player_group = Group()

player_group.add(player)

balls = Group()

ball = Ball()
balls.add(ball)


while game_over():

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            sys.exit()

    # Update
    player.update()
    balls.update()
    update_ball()

    # Draw
    screen.fill(bg_color)
    balls.draw(screen)
    player_group.draw(screen)

    pygame.display.flip()

