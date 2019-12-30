#coding=utf-8
import pygame
import random
from os import path

#檔案夾
img_folder = path.join(path.dirname(__file__), 'images')
sound_folder = path.join(path.dirname(__file__), 'sounds')

#參數規格
WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000
BAR_LENGTH = 100
BAR_HEIGHT = 15

#顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

###############################

#初始化 & 創建視窗
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('競速賽車')
clock = pygame.time.Clock()     ## For syncing the FPS

############## 物件 #################
# 玩家
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (35,65))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0 
        self.speedy = 0

    def update(self):
        # 速度歸零
        self.speedx = 0
        self.speedy = 0

        # 偵測方向鍵
        keystate = pygame.key.get_pressed()     
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_UP]:
            self.speedy = -5
        if keystate[pygame.K_DOWN]:
            self.speedy = 5

        # 移動
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # 保持 左右界線
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        elif self.rect.top < HEIGHT *0.75:
            self.rect.top = HEIGHT *0.75

###############################
# 載入圖片
player_img = pygame.image.load(path.join(img_folder, 'car1.png')).convert_alpha()

###############################
## Game loop
running = True
menu_display = True

while running:
    # 1.遊戲主畫面
    if menu_display:
        menu_display = False
        # 建立群組
        all_sprites = pygame.sprite.Group()
        # 建立玩家
        player = Player()
        all_sprites.add(player)

    # 2.幀數控制 輸入偵測
    clock.tick(FPS)
    for event in pygame.event.get():
        #關閉視窗
        if event.type == pygame.QUIT:
            running = False

        keyinput = pygame.key.get_pressed()
        print(keyinput)
        
        # ESC 離開  
        if keyinput[pygame.K_ESCAPE]:
            running = False
    # 3.精靈更新
    all_sprites.update()

    screen.fill(BLACK)

    all_sprites.draw(screen)
    pygame.display.flip() 
    pygame.display.set_caption('競速賽車 ' + str(int(clock.get_fps())) + " fps")    

pygame.quit()
