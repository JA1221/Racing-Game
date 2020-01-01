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
randomY_min = -400
randomY_max = -50

#顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

GREEN_Grassland = (58,185,108)

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
        self.image = pygame.transform.rotozoom(cones_img, random.randint(0,360), 0.4)
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
        self.img_orig = random.choice(moto_imgs)
        self.image = pygame.transform.scale(self.img_orig, (20,40))
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

        if self.rect.top > HEIGHT or (self.rect.right > EDGE_LEFT and self.rect.left < EDGE_RIGHT + 10):
            print('kill')
            self.kill()

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

def newgas():
    new_gas = gas()
    all_sprites.add(new_gas)
    gas_group.add(new_gas)

def newTree():
    new_Tree = Tree()
    all_sprites.add(new_Tree)
###############################
#顯示 文字
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font("msjh.ttf", size)
    font.set_bold(True)
    text_surface = font.render(text, False, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

###############################
# 載入圖片
background = pygame.image.load(path.join(img_folder, 'Grassland.png')).convert()
background_rect = background.get_rect()

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

# Explosion
explosion_imgs = []
for i in range(8):
    filename = 'Explosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_folder, filename)).convert_alpha()
    img = pygame.transform.scale(img, (50,50))
    explosion_imgs.append(img)

# gas
gas_img = pygame.image.load(path.join(img_folder, 'gas.png')).convert_alpha()

# tree
tree_img = pygame.image.load(path.join(img_folder, 'tree.png')).convert_alpha()

###################################################
#載入音樂

expl_sounds = []
for i in range(2):
    filename = 'Car crash_0{}.ogg'.format(i)
    expl_sounds.append(pygame.mixer.Sound(path.join(sound_folder, filename)))

get_gas = pygame.mixer.Sound(path.join(sound_folder, 'get gas.ogg'))
slip = pygame.mixer.Sound(path.join(sound_folder, 'slip.ogg'))

pygame.mixer.music.set_volume(0.2)

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
        gas_group = pygame.sprite.Group()

        # 建立玩家
        player = Player()
        all_sprites.add(player)

        # 建立障礙
        newRock()
        newRock()
        newRock()
        newMoto()
        newCones()

        # 分數
        score = 0

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

    # 4.偵測碰撞
    #rock
    hits = pygame.sprite.spritecollide(player, rock_group, True, pygame.sprite.collide_circle)
    for hit in hits:
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center)
        all_sprites.add(expl)
        expl = Explosion(player.rect.center)
        all_sprites.add(expl)
        newRock()
        player.lives -= 1
        player.hide()

    #moto
    hits = pygame.sprite.spritecollide(player, moto_group, True)
    for hit in hits:
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center)
        all_sprites.add(expl)
        expl = Explosion(player.rect.center)
        all_sprites.add(expl)
        newMoto()
        player.lives -= 1
        player.hide()

    #cones
    hits = pygame.sprite.spritecollide(player, cones_group, False)
    for hit in hits:
        slip.play()
        hit.hit()

    # 5.加分計算
    hits = pygame.sprite.spritecollide(player, gas_group, True)
    for hit in hits:
        get_gas.play()
        score += 1000;
    if not player.hidden:
        score += 2;

    # 6.機率性掉落 加分物 gas
    if random.random() < 0.001:
        newgas()

    # 7.畫面繪製
    if random.random() < 0.1:
        newTree()
    # 底圖
    screen.fill(GREEN_Grassland)
    # screen.blit(background, background_rect)

    # 賽道shift
    lineY = ( lineY + SPEED ) % lineShift - lineShift
    screen.blit(road, (EDGE_LEFT, lineY))
    # 繪製精靈
    all_sprites.draw(screen)
    # 繪製文字訊息
    draw_text(screen, 'Score : ' + str(score), 18, EDGE_RIGHT + (WIDTH - EDGE_RIGHT )/2, 50)

    pygame.display.flip() 
    pygame.display.set_caption('競速賽車 ' + str(int(clock.get_fps())) + " fps")    

pygame.quit()
