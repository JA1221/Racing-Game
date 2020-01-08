#coding=utf-8
import pygame
import random
from os import path

WIDTH = 600
HEIGHT = 700
SPEED = 3
EDGE_LEFT = 70
EDGE_RIGHT = EDGE_LEFT + 260
randomY_min = -400
randomY_max = -50

# 檔案夾
img_folder = path.join(path.dirname(__file__), 'images')
sound_folder = path.join(path.dirname(__file__), 'sounds')

######################################
pygame.init()
screen = pygame.display.set_mode((10, 10))
clock = pygame.time.Clock()     ## For syncing the FPS

############## Func #################

def IMG(filename):
    return pygame.image.load(path.join(img_folder, filename)).convert_alpha()

def SOUND(filename):
    return pygame.mixer.Sound(path.join(sound_folder, filename))

def playMUSIC(filename):
    pygame.mixer.music.load(path.join(sound_folder, filename))
    pygame.mixer.music.play(-1)

############## 物件 #################
# 玩家
class Player(pygame.sprite.Sprite):
    def __init__(self, imgNum = 0):
        super().__init__()
        self.imgNum = imgNum
        self.image = pygame.transform.scale(car_imgs[imgNum], (20,40))
        # self.image = pygame.transform.scale(random.choice(car_imgs), (20,40))
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = EDGE_LEFT + (EDGE_RIGHT - EDGE_LEFT) / 2 + 5
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0 
        self.speedy = 0
        self.move_speed = 3

        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

    def update(self):
        # 隱藏
        if self.hidden:
            if self.lives > 0:
                if pygame.time.get_ticks() - self.hide_timer > 1000:
                    self.hidden = False
                    self.rect.centerx = EDGE_LEFT + (EDGE_RIGHT - EDGE_LEFT) / 2 + 5
                    self.rect.bottom = HEIGHT - 10
            return

        # 速度歸零
        self.speedx = 0
        self.speedy = 0

        # 偵測方向鍵
        keystate = pygame.key.get_pressed()     
        if keystate[pygame.K_LEFT]:
            self.speedx = -self.move_speed
        if keystate[pygame.K_RIGHT]:
            self.speedx = self.move_speed
        if keystate[pygame.K_UP]:
            self.speedy = -self.move_speed
        if keystate[pygame.K_DOWN]:
            self.speedy = self.move_speed

        # 移動
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # 保持 左右界線
        if self.rect.right > EDGE_RIGHT:
            self.rect.right = EDGE_RIGHT
        elif self.rect.left < EDGE_LEFT + 10:
            self.rect.left = EDGE_LEFT + 10

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        elif self.rect.top < HEIGHT *0.7:
            self.rect.top = HEIGHT *0.7

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (self.rect.centerx, HEIGHT + 200)

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.imgNum = random.randrange(len(rock_imgs))
        self.imgAngle = random.randint(0,360)
        self.imgScale = random.uniform(0.2,0.7)

        self.image = pygame.transform.rotozoom(rock_imgs[self.imgNum] , self.imgAngle, self.imgScale)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *.90 / 2)
        # 生成位置
        self.rect.x = random.randrange(EDGE_LEFT + 10 , EDGE_RIGHT - self.rect.width)
        self.rect.y = random.randrange(randomY_min, randomY_max)

    def update(self):
        self.rect.y += SPEED

        # 超出底部 移到最頂
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(EDGE_LEFT + 10 , EDGE_RIGHT - self.rect.width)
            self.rect.y = random.randrange(randomY_min, randomY_max)

class Cones(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.imgAngle = random.randint(0,360)

        self.image = pygame.transform.rotozoom(cones_img, self.imgAngle, 0.4)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *.90 / 2)
        self.speedy = SPEED
        # 生成位置
        self.rect.x = random.randrange(EDGE_LEFT + 10 , EDGE_RIGHT - self.rect.width)
        self.rect.y = random.randrange(randomY_min, randomY_max)
        # 碰撞
        self.hited = False
        self.hit_timer = pygame.time.get_ticks()

    def update(self):
        self.rect.y += self.speedy

        if self.hit and pygame.time.get_ticks() - self.hit_timer > 500:
            self.hited = False
            self.speedy = SPEED

        # 超出底部 移到最頂
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(EDGE_LEFT + 10 , EDGE_RIGHT - self.rect.width)
            self.rect.y = random.randrange(randomY_min, randomY_max)

    def hit(self):
        self.hited = True
        self.hit_timer = pygame.time.get_ticks()
        self.speedy = -1

class Moto(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.imgNum = random.randrange(len(moto_imgs))

        self.image = pygame.transform.scale(moto_imgs[self.imgNum], (20,40))
        self.rect = self.image.get_rect()
        # 移動變數
        self.movex_delay = 1000
        self.last_update = pygame.time.get_ticks()

        self.speedx = random.randint(-1,1)
        self.speedy = random.randint(1, SPEED)
        # 生成位置
        self.rect.x = random.randrange(EDGE_LEFT + 10 , EDGE_RIGHT - self.rect.width)
        self.rect.y = random.randrange(randomY_min, randomY_max)

    def update(self):
        # 左右隨機移動
        time_now = pygame.time.get_ticks()
        if time_now - self.last_update > self.movex_delay:
            self.last_update = time_now
            self.speedx = random.randint(-1,1)

        # 移動
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        # 保持 左右界線
        if self.rect.right > EDGE_RIGHT:
            self.rect.right = EDGE_RIGHT
        elif self.rect.left < EDGE_LEFT + 10:
            self.rect.left = EDGE_LEFT + 10

        # 超出底部 移到最頂
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(EDGE_LEFT + 10 , EDGE_RIGHT - self.rect.width)
            self.rect.y = random.randrange(randomY_min, randomY_max)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = explosion_imgs[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0 
        self.last_update = pygame.time.get_ticks()
        self.frame_delay = 75 # 每張圖片間距時間

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_imgs):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_imgs[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class gas(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(gas_img, (25,25))
        self.rect = self.image.get_rect()
        # 生成位置
        self.rect.x = random.randrange(EDGE_LEFT + 10 , EDGE_RIGHT - self.rect.width)
        self.rect.bottom = 0

    def update(self):
        self.rect.y += SPEED

        if self.rect.top > HEIGHT:
            self.kill()

class Tree(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(tree_img, random.randint(0,360), random.uniform(0.2,0.6))
        self.rect = self.image.get_rect()
        # 生成位置
        self.rect.x = random.randrange(0 - self.rect.width, WIDTH)
        self.rect.bottom = 0

    def update(self):
        self.rect.y += SPEED

        if self.rect.top > HEIGHT or self.isOnRoad():
            self.kill()

    def isOnRoad(self):
        return self.rect.right > EDGE_LEFT and self.rect.left < EDGE_RIGHT + 10

###################################################
# 載入圖片
background = IMG('Grassland.png')

player_img_01 = IMG('car1.png')
player_img_02 = IMG('car2.png')

# cars & motos
car_imgs = []
moto_imgs = []
vehicle_color = ['black', 'blue', 'green', 'red', 'yellow']

for color in vehicle_color:
    #car
    for i in range(1,6):
        filename = 'car_{}_{}.png'.format(color, i)
        img = IMG(filename)
        car_imgs.append(img)
    #moto
    filename = 'motorcycle_{}.png'.format(color)
    img = IMG(filename)
    moto_imgs.append(img)

# road
road = IMG('road.png')

# rock
rock_imgs = []
for i in range(1,4):
    filename = 'rock{}.png'.format(i)
    img = IMG(filename)
    rock_imgs.append(img)

#cones
cones_img = IMG('cones.png')

# Explosion
explosion_imgs = []
for i in range(8):
    filename = 'Explosion0{}.png'.format(i)
    img = IMG(filename)
    img = pygame.transform.scale(img, (50,50))
    explosion_imgs.append(img)

# gas
gas_img = IMG('gas.png')

# tree
tree_img = IMG('tree.png')
#######################################################