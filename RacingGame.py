#coding=utf-8
import pygame
from network import Network
import random
import GameObject
from os import path

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
GREEN_Grassland = (58,185,108)

###############################

#初始化 & 創建視窗
def initGame():
    global screen
    global clock
    global score

    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('競速賽車')
    clock = pygame.time.Clock()     ## For syncing the FPS
    score = 0


#####################################
# 遊戲主畫面
def main_menu():
    global screen

    # 載入主畫面音樂
    playMUSIC('Menu BGM.mp3')

    # 背景圖片
    background = IMG(random.choice(('main2.jpg', 'main.jpg')))
    background = pygame.transform.scale(background, (WIDTH, HEIGHT), screen)#縮放
    screen.blit(background, (0,0))

    draw_text(screen, "按下 [ENTER] 開始遊戲", 30, WIDTH/2, 260)
    draw_text(screen, "or [Q] 離開", 30, WIDTH/2, 300)
    pygame.display.update()

    while True:
        event = pygame.event.poll() # 取一個事件
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:#進入遊戲
                break
            elif event.key == pygame.K_q:#離開
                pygame.quit()
                quit()
        elif event.type == pygame.QUIT:
                pygame.quit()
                quit()
    pygame.mixer.music.stop()  

# 遊戲結束畫面
def game_Over_screen():
    global screen

    screen.blit(GameObject.background, (0,0))
    if(game.playerLives[1 - playerID] <= 0):
        s = '恭喜:獲勝!'
    else:
        s = '你先死了，再加油!'
    draw_text(screen, s, 30, WIDTH/2, HEIGHT/2)
    draw_text(screen, "遊戲分數：" + str(score), 30, WIDTH/2, HEIGHT/2 + 40)
    pygame.display.update()

    while True:
        event = pygame.event.poll() # 取一個事件
        if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
            pygame.quit()
            quit()


###############################
# add class
def newPlayer():
    player = GameObject.Player(random.randrange(25))
    all_sprites.add(player)
    # game.addPlayer(playerID, player.imgNum, player.rect.center, player.lives)
    return player

def newRock():
    new_rock = GameObject.Rock()
    all_sprites.add(new_rock)
    rock_group.add(new_rock)

def newMoto():
    new_moto = GameObject.Moto()
    all_sprites.add(new_moto)
    moto_group.add(new_moto)

def newCones():
    new_cones = GameObject.Cones()
    all_sprites.add(new_cones)
    cones_group.add(new_cones)

def newgas():
    new_gas = GameObject.gas()
    all_sprites.add(new_gas)
    gas_group.add(new_gas)

def newTree():
    new_Tree = GameObject.Tree()
    all_sprites.add(new_Tree)

def newExplosion(center):
    random.choice(expl_sounds).play()
    expl = GameObject.Explosion(center)
    all_sprites.add(expl)
    Expl_group.add(expl)

###############################
def updatePlayer(playerID, lives, score, imgNum):
    s = str(playerID) + ' ' + str(lives) + ' ' + str(score) + ' ' + str(imgNum)
    n.send(s)
    return s

def updateRocks():
    game.clearRock()

    for rock in rock_group:
        game.addRock(rock.imgNum, rock.rect.center, rock.imgAngle, rock.imgScale)

def updateMoto():
    game.clearMoto()

    for moto in moto_group:
        game.addMoto(moto.imgNum, moto.rect.center, moto.speedy, moto.speedx)

def updateCones():
    game.clearCones()

    for cones in cones_group:
        game.addCones(cones.rect.center, cones.imgAngle)

def updateGas():
    game.clearGas()

    for gas in gas_group:
        game.addGas(gas.rect.center)

###############################
#顯示 文字
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font("msjh.ttf", size)
    font.set_bold(True)
    text_surface = font.render(text, False, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

#顯示生命數
def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect= img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def IMG(filename):
    return GameObject.IMG(filename)

def SOUND(filename):
    return GameObject.SOUND(filename)

def playMUSIC(filename):
    GameObject.playMUSIC(filename)

def updateConnect():
    global game
    # 偵測連線
    try:
        game = n.send("get")
    except:
        run = False
        print("Couldn't get game")
        return False
    return True
###################################################
#載入音樂

expl_sounds = []
for i in range(2):
    filename = 'Car crash_0{}.ogg'.format(i)
    expl_sounds.append(SOUND(filename))

get_gas = SOUND('get gas.ogg')
slip = SOUND('slip.ogg')

# pygame.mixer.music.set_volume(0.3)

###############################
## Game loop

def main():
    initGame()
    running = True
    menu_display = True

    lineY = 0
    lineShift = GameObject.road.get_height() - HEIGHT

    global n, playerID, game
    n = Network()
    playerID = int(n.getP())
    print("You are player", playerID)

    while running:
        # 1.遊戲主畫面
        if menu_display:
            main_menu()

            screen.fill(BLACK)
            draw_text(screen, '等待對手加入中...', 30, WIDTH/2, HEIGHT/2)
            pygame.display.flip() 

            n.send("ready")

            if not updateConnect():
                break

            while not game.begin():
                updateConnect()

            # pygame.time.wait(3000)
            menu_display = False

            # 播放 遊戲音樂
            playMUSIC('BGM.mp3')

            # 建立群組
            global all_sprites
            global rock_group
            global moto_group
            global cones_group
            global gas_group
            global Expl_group
            all_sprites = pygame.sprite.Group()
            rock_group = pygame.sprite.Group()
            moto_group = pygame.sprite.Group()
            cones_group = pygame.sprite.Group()
            gas_group = pygame.sprite.Group()
            Expl_group = pygame.sprite.Group()

            # 建立玩家
            player = newPlayer()

            # 建立障礙
            newRock()
            newRock()
            newRock()
            newMoto()
            newCones()

            # 分數
            global score
        
        updateConnect()
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
        # rock
        hits = pygame.sprite.spritecollide(player, rock_group, True, pygame.sprite.collide_circle)
        for hit in hits:
            newExplosion(hit.rect.center)
            newExplosion(player.rect.center)
            newRock()
            player.lives -= 1
            player.hide()

        # moto
        hits = pygame.sprite.spritecollide(player, moto_group, True)
        for hit in hits:
            newExplosion(hit.rect.center)
            newExplosion(player.rect.center)
            newMoto()
            player.lives -= 1
            player.hide()

        # cones
        hits = pygame.sprite.spritecollide(player, cones_group, False)
        for hit in hits:
            slip.play()
            hit.hit()

        # 6.檢查生命數
        if player.lives <= 0 and len(Expl_group)<=0:
            running = False
            game.updatePlayer(playerID, player.lives, score, player.imgNum)
            game_Over_screen()
            continue

        # 7.加分計算
        hits = pygame.sprite.spritecollide(player, gas_group, True)
        for hit in hits:
            get_gas.play()
            score += 1000;
        if not player.hidden:
            score += 1;
        updatePlayer(playerID, player.lives, score, player.imgNum)

        # 8.機率性掉落 加分物 gas
        if random.random() < 0.001:
            newgas()

        # updateOnlineAll()

        # 9.畫面繪製
        if random.random() < 0.1:
            newTree()
        # 底圖
        screen.fill(GREEN_Grassland)
        # screen.blit(GameObject.background,(0, 0))

        # 賽道shift
        lineY = ( lineY + SPEED ) % lineShift - lineShift
        screen.blit(GameObject.road, (EDGE_LEFT, lineY))
        # 繪製精靈
        all_sprites.draw(screen)
        # 繪製分數 生命數
        draw_text(screen, '分數 : ' + str(score), 20, 465, 100)
        draw_lives(screen, player.lives, player.image, 430, 150)

        orig_img = GameObject.car_imgs[game.playerImgNum[1-playerID]]
        draw_text(screen, '敵人分數 : ' + str(game.playerScore[1-playerID]), 20, 465, 200)
        draw_lives(screen, game.playerLives[1-playerID], pygame.transform.scale(orig_img, (20,40)), 430, 250)

        pygame.display.flip() 
        pygame.display.set_caption('競速賽車 ' + str(int(clock.get_fps())) + " fps")
    pygame.quit()

if __name__ == "__main__":
    main()