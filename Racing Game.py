#coding=utf-8
import pygame
import random
from os import path

#檔案夾
img_folder = path.join(path.dirname(__file__), 'images')
sound_folder = path.join(path.dirname(__file__), 'sounds')

#參數規格
WIDTH = 500
HEIGHT = 700
FPS = 60
EDGE_LEFT = 70
EDGE_RIGHT = WIDTH - EDGE_LEFT - 10

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
        self.image = pygame.transform.scale(player_img_01, (20,40))
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
        if self.rect.right > EDGE_RIGHT:
            self.rect.right = EDGE_RIGHT
        elif self.rect.left < EDGE_LEFT + 10:
            self.rect.left = EDGE_LEFT + 10

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        elif self.rect.top < HEIGHT *0.75:
            self.rect.top = HEIGHT *0.75

class Player2(Player):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_img_02, (35,65))

###############################
# 載入圖片
player_img_01 = pygame.image.load(path.join(img_folder, 'car1.png')).convert_alpha()
player_img_02 = pygame.image.load(path.join(img_folder, 'car2.png')).convert_alpha()
edge_line_left = pygame.image.load(path.join(img_folder, 'edge line_left.png')).convert_alpha()
edge_line_right = pygame.image.load(path.join(img_folder, 'edge line_right.png')).convert_alpha()
###############################
## Game loop
running = True
menu_display = True

lineY = 0
lineShift = edge_line_left.get_height() - HEIGHT

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

    #畫面繪製
    screen.fill(BLACK)
    lineY = ( lineY + 2 ) % lineShift - lineShift
    screen.blit(edge_line_left, (EDGE_LEFT, lineY))
    screen.blit(edge_line_right, (EDGE_RIGHT, lineY))

    all_sprites.draw(screen)
    pygame.display.flip() 
    pygame.display.set_caption('競速賽車 ' + str(int(clock.get_fps())) + " fps")    

pygame.quit()
