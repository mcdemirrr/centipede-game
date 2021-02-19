import pygame,random,time,pygame.event

from Player import *
from Fire import *
from Spider import *
from Bomb import *
from LilCenti import *
from Expo import *

pygame.init()
bg =(25,25,25)
level=1
game_map=[]
empty=pygame.Surface([20,20])
empty.fill(bg)
mushroom_image = pygame.image.load('shroom1.png')
mushroom_image2 = pygame.image.load('shroom2.png')
mushroom_image3 = pygame.image.load('shroom3.png')
mushroom_image.set_colorkey((0,0,0))
mushroom_image2.set_colorkey((0,0,0))
mushroom_image3.set_colorkey((0,0,0))

def setup_game_map():
    global game_map
    game_map = []
    for x in range(40):
        arrayOfZeros = [0]*30
        game_map.append(arrayOfZeros)
    for x in range (30):
        randomX=random.randint(0,29)
        randomY=random.randint(0,27)
        game_map[randomX][randomY] = 1

def draw_game_map():
        for column in range(30):
            for row in range(40):
                spot = game_map[row][column]
                if spot == 1:
                    screen.blit(empty,[column*20, row*20])
                    screen.blit(mushroom_image, [column*20, row*20])
                if spot == 2:
                    screen.blit(empty,[column*20, row*20])
                    screen.blit(mushroom_image2, [column*20, row*20])
                if spot == 3:
                    screen.blit(empty,[column*20, row*20])
                    screen.blit(mushroom_image3, [column*20, row*20])
                if spot == 4:
                    screen.blit(empty,[column*20, row*20])
                    game_map[row][column] = 0

def get_key():
    while 1:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            return event.key
        else:
            pass
size=[600,800]
screen=pygame.display.set_mode(size)
pygame.display.set_caption("Centipede")

player=Player(300,700)
fire=Fire()
bomb=Bomb()
fireGroup=pygame.sprite.Group()
fireGroup.add(fire)
clock=pygame.time.Clock()
going=True

background=pygame.Surface(size)
background.fill(bg)
screen.blit(background,(0,0))

allsprites=pygame.sprite.Group()
allsprites.add(player)
allsprites.add(fireGroup)
allsprites.add(bomb)

expos=pygame.sprite.Group()

centis=pygame.sprite.Group()
for m in range(12):
    centi=LilCenti(20*m,-20)
    centis.add(centi)

spider=Spider()
allsprites.add(spider)
allsprites.add(centis)
allsprites.add(expos)
setup_game_map()
clock_tick=20
game_mode='menu'
tickCounter=0

gameOverFont = pygame.font.Font('ARDARLING.ttf' ,70)
clickToStart = pygame.font.Font('ARDARLING.ttf',40)
highScore = pygame.font.Font('ARDARLING.ttf',50)

menu_header=[]
menu_header.append(pygame.image.load("menu_centi1.png"))
menu_header.append(pygame.image.load("menu_centi2.png"))
menu_high=[]
menu_high.append(pygame.image.load("menu_high1.png"))
menu_high.append(pygame.image.load("menu_high2.png"))
menu_ins=[]
menu_ins.append(pygame.image.load("menu_ins1.png"))
menu_ins.append(pygame.image.load("menu_ins2.png"))
menu_play=[]
menu_play.append(pygame.image.load("menu_play1.png"))
menu_play.append(pygame.image.load("menu_play2.png"))
menu_quit=[]
menu_quit.append(pygame.image.load("menu_quit1.png"))
menu_quit.append(pygame.image.load("menu_quit2.png"))
menu_footer=pygame.image.load("menu_footer.png")

inst_space=[]
for i in range(1,5):
    inst_space.append(pygame.image.load("instructions%d.png" % i))
inst_up=[]
for i in range(1,5):
    inst_up.append(pygame.image.load("instructions_up%d.png" % i))
inst_shroom=[]
for i in range(1,7):
    inst_shroom.append(pygame.image.load("instructions_shroom%d.png" % i))
inst_bomb=[]
for i in range(1,5):
    inst_bomb.append(pygame.image.load("instructions_bomb%d.png" % i))
inst_spider=[]
for i in range(1,5):
    inst_spider.append(pygame.image.load("instructions_sp%d.png" % i))
inst_centi=[]
for i in range(1,5):
    inst_centi.append(pygame.image.load("instructions_centi%d.png" % i))
inst_footer=pygame.image.load("instructions_footerAAA.png")


high_footer=pygame.image.load("high_footer.png")

playerNames=['AAA','AAA','AAA','AAA','AAA','AAA','AAA','AAA','AAA']
playerScores=[999,888,777,666,555,444,333,22,1]

currentUser=['A','A','A']
currentCharacter=0
currentScore=0
lastScore=0

menu_selection=1
slowDownAnimation=0
while going:   
    clock.tick(clock_tick)
    tickCounter+=1
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            going=False
    if game_mode=='savescore':
        lastScore=currentScore
        currentCharacter=0
        userText=''
        for i in range(len(currentUser)):
            userText+=currentUser[i]
        text = gameOverFont.render(userText, True, (255,255,255))
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        screen.blit(text, [text_x, text_y+300])
        pygame.display.flip()
        while currentCharacter<3:
            inkey=get_key()
            if inkey == pygame.K_RETURN:
                game_mode='menu'
                break
            userText=''
            if inkey == pygame.K_BACKSPACE:
                currentUser=currentUser[0:-1]
            elif inkey <= 127:
                currentUser[currentCharacter]=chr(inkey-32)
                currentCharacter+=1
                
                for i in range(len(currentUser)):
                    userText+=currentUser[i]
                    
                text = gameOverFont.render(userText, True, (255,255,255))
                text_rect = text.get_rect()
                text_x = screen.get_width() / 2 - text_rect.width / 2
                refresh=pygame.Surface([text_rect.width,text_rect.height])
                refresh.fill(bg)
                screen.blit(refresh,[text_x, text_y+300])
                screen.blit(text, [text_x, text_y+300])
                pygame.display.flip()

        print('name done')
        print(lastScore)
        print(userText)
        for i in range(9):
            if lastScore>=playerScores[i]:
                playerScores.insert(i,lastScore)
                playerNames.insert(i,userText)
                print(userText)
                break
        game_mode='menu'        
    if game_mode=='high':
        pygame.display.set_caption("Centipede")
        title=gameOverFont.render('High Scores',True,(255,255,255))
        screen.blit(high_footer,(0,719))

        title_rect = title.get_rect()
        title_x = screen.get_width() / 2 - title_rect.width / 2
        title_y = 40
        screen.blit(title, [title_x, title_y])
        for i in range(9):
            name = highScore.render(str(i+1)+'. '+playerNames[i],True,(255,255,255))
            text_rect = name.get_rect()
            name_x = screen.get_width() / 4 - text_rect.width / 2
            name_y = 150 + 60*(i)
            screen.blit(name,[name_x,name_y])

        for i in range(9):
            name = highScore.render(str(playerScores[i]),True,(255,255,255))
            text_rect = name.get_rect()
            name_x = 3*(screen.get_width() / 4) - text_rect.width / 2
            name_y = 150 + 60*(i)
            screen.blit(name,[name_x,name_y])
        keys=pygame.key.get_pressed()
        if(keys[pygame.K_ESCAPE]):
            game_mode='menu'
            refresh=pygame.Surface([600,800])
            refresh.fill(bg)
            screen.blit(refresh,[0,0])
            menu_selection=2
        
        
    if game_mode=='inst':
        pygame.display.set_caption("Centipede")
        if(tickCounter%10==0):
            slowDownAnimation+=1
            screen.blit(inst_footer,(0,600))
            screen.blit(inst_space[slowDownAnimation%4],(0,0))
            screen.blit(inst_up[slowDownAnimation%4],(300,0))
            screen.blit(inst_shroom[slowDownAnimation%6],(0,200))
            screen.blit(inst_bomb[slowDownAnimation%4],(300,200))
            screen.blit(inst_spider[slowDownAnimation%4],(0,400))
            screen.blit(inst_centi[slowDownAnimation%4],(300,400))
        keys=pygame.key.get_pressed()
        if(keys[pygame.K_ESCAPE]):
            game_mode='menu'
            refresh=pygame.Surface([600,800])
            refresh.fill(bg)
            screen.blit(refresh,[0,0])
            menu_selection=3
            slowDownAnimation=0

    if game_mode=='menu':
        pygame.display.set_caption("Centipede")
        keys=pygame.key.get_pressed()
        if(keys[pygame.K_DOWN] and menu_selection<4):
            menu_selection+=1

        if(keys[pygame.K_UP] and menu_selection>1):
            menu_selection-=1
        
        screen.blit(menu_header[tickCounter%2],(0,0))
        screen.blit(menu_footer,(0,625))
        if menu_selection==1:
            screen.blit(menu_play[1],(0,200))
        else:
            screen.blit(menu_play[0],(0,200))

        if menu_selection==2:
            screen.blit(menu_high[1],(0,325))
        else:
            screen.blit(menu_high[0],(0,325))

        if menu_selection==3:
            screen.blit(menu_ins[1],(0,425))
        else:
            screen.blit(menu_ins[0],(0,425))

        if menu_selection==4:
            screen.blit(menu_quit[1],(0,525))
        else:
            screen.blit(menu_quit[0],(0,525))

        if(keys[pygame.K_RETURN]):
            refresh=pygame.Surface([600,800])
            refresh.fill(bg)
            screen.blit(refresh,[0,0])
            if menu_selection==1:
                game_mode='play'
            elif menu_selection==2:
                game_mode='high'
            elif menu_selection==3:
                game_mode='inst'
            elif menu_selection==4:
                going=False
    elif game_mode=='gameover':

        lastScore = currentScore
        
        text = gameOverFont.render("GAME OVER!", True, (255,255,255))
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        text_y = screen.get_height() / 2 - text_rect.height / 2
        screen.blit(text, [text_x, text_y-200])

        text = clickToStart.render("Hit [S] to Save", True, (255,255,255))
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        screen.blit(text, [text_x, text_y+210])
        
        text = clickToStart.render("Hit Enter to Start Again", True, (255,255,255))
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        screen.blit(text, [text_x, text_y+90])

        text = clickToStart.render("Hit Escape for Menu", True, (255,255,255))
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        screen.blit(text, [text_x, text_y+150])
        
        keys=pygame.key.get_pressed()
        if(keys[pygame.K_RETURN]):
            game_mode='play'
            refresh=pygame.Surface([600,800])
            refresh.fill(bg)
            screen.blit(refresh,[0,0])
            centis=pygame.sprite.Group()
            for m in range(12):
                centi=LilCenti(20*m,-20)
                centis.add(centi)
                setup_game_map()
                allsprites.add(centis)
            allsprites=pygame.sprite.Group()
            allsprites.add(player)
            allsprites.add(fireGroup)
            allsprites.add(bomb)
            allsprites.add(spider)
            allsprites.add(centis)
            allsprites.add(expos)
            spider.deactivate()
            bomb.deactivate()
            fire.deactivate()
        if(keys[pygame.K_ESCAPE]):
            game_mode='menu'
            refresh=pygame.Surface([600,800])
            refresh.fill(bg)
            screen.blit(refresh,[0,0])

            centis=pygame.sprite.Group()
            for m in range(12):
                centi=LilCenti(20*m,-20)
                centis.add(centi)
                setup_game_map()
                allsprites.add(centis)
            allsprites=pygame.sprite.Group()
            allsprites.add(player)
            allsprites.add(fireGroup)
            allsprites.add(bomb)
            allsprites.add(spider)
            allsprites.add(centis)
            allsprites.add(expos)
            spider.deactivate()
            bomb.deactivate()
            fire.deactivate()
            menu_selection=1

        if(keys[pygame.K_s]):
            game_mode='savescore'

            centis=pygame.sprite.Group()
            for m in range(12):
                centi=LilCenti(20*m,-20)
                centis.add(centi)
                setup_game_map()
                allsprites.add(centis)
            allsprites=pygame.sprite.Group()
            allsprites.add(player)
            allsprites.add(fireGroup)
            allsprites.add(bomb)
            allsprites.add(spider)
            allsprites.add(centis)
            allsprites.add(expos)
            spider.deactivate()
            bomb.deactivate()
            fire.deactivate()
    if game_mode=='play':
        shootTileX=int(fire.x/20)
        shootTileY=int(fire.y/20)

        keys=pygame.key.get_pressed()
        if(keys[pygame.K_SPACE] and fire.canFire):
            fire.activate(player.rect.x+8,player.rect.y+6)
        for c in centis:
            if c.left_right==1 and c.rect.x<580:
                if game_map[int(c.rect.y/20)][int(c.rect.x/20)+1]:
                    c.collide()
            else:
                if game_map[int(c.rect.y/20)][int(c.rect.x/20)-1]:
                    c.collide()

            if c.rect.x==fire.rect.x-8 and c.rect.y==fire.rect.y-6:
                c.kill()
                game_map[shootTileY-1][shootTileX]=1
                currentScore+=10
                fire.deactivate()

        if game_map[shootTileY-1][shootTileX]>0:
            game_map[shootTileY-1][shootTileX]=game_map[shootTileY-1][shootTileX]+1
            currentScore+=3
            fire.deactivate()
        

        if spider.isActive==0:
            rnd=random.randint(0,500/level)
            if rnd==0:
                spider.activate()

        if pygame.sprite.spritecollide(spider,fireGroup,False):
            expo=Explode(spider.rect.x,spider.rect.y)
            allsprites.add(expo)
            expos.add(expo)
            spider.deactivate()
            fire.deactivate()
            currentScore+=50

        if bomb.isActive==0:
            rnd=random.randint(0,10/level)
            if rnd==0:
                bomb.activate()
        else:        
            if(bomb.drop):
                rnd=random.randint(1,5)

                if(rnd==1 and bomb.ay>0 and bomb.isActive):
                    game_map[int(bomb.ay/20)+1][int(bomb.ax/20)]=1
                    bomb.drop=0

        if pygame.sprite.spritecollide(bomb,fireGroup,False):
            expo=Explode(bomb.rect.x,bomb.rect.y)
            allsprites.add(expo)
            expos.add(expo)
            bomb.deactivate()
            fire.deactivate()
            currentScore+=30

        if pygame.sprite.spritecollide(player,centis,False):
            expo=Explode(player.rect.x,player.rect.y)
            allsprites.add(expo)
            expos.add(expo)
            game_mode='gameover'
        if pygame.sprite.collide_rect(player,spider):
            expo=Explode(player.rect.x,player.rect.y)
            allsprites.add(expo)
            expos.add(expo)
            game_mode='gameover'
        if pygame.sprite.collide_rect(player,bomb):
            expo=Explode(player.rect.x,player.rect.y)
            allsprites.add(expo)
            expos.add(expo)
            game_mode='gameover'



        if(tickCounter%3==0):
                player.update(keys)

        pygame.display.set_caption("Score : "+str(currentScore))
        
        allsprites.clear(screen,background)
        fire.update()
        spider.update()
        bomb.update()
        centis.update()
        expos.update()
        draw_game_map()
        allsprites.draw(screen)
    pygame.display.flip()
pygame.quit()
