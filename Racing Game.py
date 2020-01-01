#coding=utf-8
import pygame
import random
from os import path

#檔案夾
img_folder = path.join(path.dirname(__file__), 'images')
sound_folder = path.join(path.dirname(__file__), 'sounds')

#參數規格
WIDTH = 600
HEIGHT = 700
SPEED = 3
FPS = 100
EDGE_LEFT = 70
EDGE_RIGHT = EDGE_LEFT + 260

#顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

GREEN_Grassland = (27,125,67)

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
        super().__init__()
        self.image = pygame.transform.scale(player_img_01, (20,40))
        # self.image = pygame.transform.scale(random.choice(car_imgs), (20,40))
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
        elif self.rect.top < HEIGHT *0.7:
            self.rect.top = HEIGHT *0.7

class Player2(Player):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_img_02, (35,65))

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img_orig = random.choice(rock_imgs)
        self.image = pygame.transform.rotozoom(self.img_orig, random.randint(0,360), random.uniform(0.2,0.7))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *.90 / 2)
        # 生成位置
        self.rect.x = random.randrange(EDGE_LEFT + 10 , EDGE_RIGHT - self.rect.width)
        self.rect.y = random.randrange(-200, -100)

    def update(self):
        self.rect.y += SPEED

        # 移到最頂
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(EDGE_LEFT + 10 , EDGE_RIGHT - self.rect.width)
            self.rect.y = random.randrange(-200, -100)

class Cones(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(cones_img, random.randint(0,360), 0.4)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *.90 / 2)
        # 生成位置
        self.rect.x = random.randrange(EDGE_LEFT + 10 , EDGE_RIGHT - self.rect.width)
        self.rect.y = random.randrange(-200, -100)

    def update(self):
        self.rect.y += SPEED

        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(EDGE_LEFT + 10 , EDGE_RIGHT - self.rect.width)
            self.rect.y = random.randrange(-200, -100)

class Moto(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img_orig = random.choice(moto_imgs)
        self.image = pygame.transform.scale(self.img_orig, (20,40))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *.90 / 2)
        # 移動變數
        self.movex_delay = 1000
        self.last_update = pygame.time.get_ticks()

        self.speedx = random.randint(-1,1)
        self.speedy = random.randint(1, SPEED)
        # 生成位置
        self.rect.x = random.randrange(EDGE_LEFT + 10 , EDGE_RIGHT - self.rect.width)
        self.rect.y = random.randrange(-200, -100)

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

        # 移到最頂
        if self.rect.top > HEIGHT:
            self.__init__()
            self.rect.x = random.randrange(EDGE_LEFT + 10 , EDGE_RIGHT - self.rect.width)
            self.rect.y = random.randrange(-150, -100)

###############################
# add class
def newRock():
    new_rock = Rock()
    all_sprites.add(new_rock)
    rock_group.add(new_rock)

def newMoto():
    new_moto = Moto()
    all_sprites.add(new_moto)
    moto_group.add(new_moto)

def newCones():
    new_cones = Cones()
    all_sprites.add(new_cones)
    cones_group.add(new_cones)

###############################
# 載入圖片
player_img_01 = pygame.image.load(path.join(img_folder, 'car1.png')).convert_alpha()
player_img_02 = pygame.image.load(path.join(img_folder, 'car2.png')).convert_alpha()

# cars & motos
car_imgs = []
moto_imgs = []
vehicle_color = ['black', 'blue', 'green', 'red', 'yellow']

for color in vehicle_color:
    #car
    for i in range(1,6):
        filename = 'car_{}_{}.png'.format(color, i)
        img = pygame.image.load(path.join(img_folder, filename)).convert_alpha()
        car_imgs.append(img)
    #moto
    filename = 'motorcycle_{}.png'.format(color)
    img = pygame.image.load(path.join(img_folder, filename)).convert_alpha()
    moto_imgs.append(img)

# road
road = pygame.image.load(path.join(img_folder, 'road.png')).convert_alpha()

# rock
rock_imgs = []
for i in range(1,4):
    filename = 'rock{}.png'.format(i)
    img = pygame.image.load(path.join(img_folder, filename)).convert_alpha()
    rock_imgs.append(img)

#cones
cones_img = pygame.image.load(path.join(img_folder, 'cones.png')).convert_alpha()

###############################
## Game loop
running = True
menu_display = True

lineY = 0
lineShift = road.get_height() - HEIGHT

while running:
    # 1.遊戲主畫面
    if menu_display:
        menu_display = False
        # 建立群組
        all_sprites = pygame.sprite.Group()
        rock_group = pygame.sprite.Group()
        moto_group = pygame.sprite.Group()
        cones_group = pygame.sprite.Group()

        # 建立玩家
        player = Player()
        all_sprites.add(player)

        # 建立障礙
        newRock()
        newMoto()
        newCones()

    # 2.幀數控制 輸入偵測
    clock.tick(FPS)
    for event in pygame.event.get():
        #關閉視窗
        if event.type == pygame.QUIT:
            running = False

        keyinput = pygame.key.get_pressed()
        
        # ESC 離開  
        if keyinput[pygame.K_ESCAPE]:
            running = False

    # 3.精靈更新
    all_sprites.update()

    # 4.畫面繪製
    screen.fill(GREEN_Grassland)

    lineY = ( lineY + SPEED ) % lineShift - lineShift
    screen.blit(road, (EDGE_LEFT, lineY))

    all_sprites.draw(screen)
    pygame.display.flip() 
    pygame.display.set_caption('競速賽車 ' + str(int(clock.get_fps())) + " fps")    

pygame.quit()
