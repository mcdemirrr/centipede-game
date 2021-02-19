import pygame
from pygame.locals import*
pygame.init()
import  math
import random
import sys
import time


size = [600,500]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("ADSECTOR         By Dylan J. Raub", "ADSECTOR")
"""
icon = pygame.image.load("icon.ico")
pygame.display.set_icon(icon)
"""

class Section (object):
    
    def __init__(self, number, screen_size):

        self.dead = False
        self.number = number
        self.radius = 6
        self.diameter=self.radius*2
        self.pos = [self.diameter,self.diameter]
        self.direction = [0,0]
        self.speed = 3
        self.max_x = screen_size[0]/self.diameter
        self.destination = random.randint(1,self.max_x)*self.radius*2
        self.prev_dir = self.direction

    def update(self, sections):
        self.pos[0]+=self.speed*self.direction[0]
        self.pos[1]+=self.speed*self.direction[1]
        
        if self.pos[0]%self.diameter==0 and self.pos[1]%self.diameter==0: # if at grid point
            self.prev_dir = self.direction
         
            self.leader = None
            for section in sections:
                if section.number+1==self.number:
                    self.leader = section
                    self.destination = self.leader.destination
                    
            if self.leader == None:# if my leader is gone, I become a leader
                
                if self.direction == [0,1] or self.direction == [0,0] or self.pos[0]<0 or self.pos[0]>self.max_x*self.diameter:
                
                    self.destination=random.randint(0,self.max_x)*self.radius*2
                
                    if self.destination-self.pos[0]<0: # go left
                        self.direction = [-1,0]
                    elif self.destination-self.pos[0]>0: # go right
                        self.direction = [1,0]
                    else:
                        self.direction = [0,1]
                        
                if self.pos[0]==self.destination:
                    self.direction = [0,1]
                
            else:
                self.direction = self.leader.prev_dir

    def render(self, screen, pic):
        screen.blit(pic, [self.pos[0]-self.radius,self.pos[1]-self.radius])





class Bonus (object):
    
    def __init__(self, screen_size):

        self.radius = 5
        self.diameter = self.radius*2
        self.pos = [-self.radius*2, self.radius*2]
        self.speed= self.diameter*2
        self.delay = random.randint(8, 20)*100
        self.max_x = screen_size[0]/(self.diameter*2)
        self.max_y = screen_size[1]
        self.destination=random.randint(0,self.max_x)*self.diameter*2
        self.direction = [1,0]
        


    def update(self):
        self.delay-=1
        if self.delay<0:
            if self.pos[0]%self.diameter==0 and self.pos[1]%self.diameter==0:
                if self.direction == [0,1] or self.pos[0]<0 or self.pos[0]>self.max_x*self.radius*2:
                    self.destination=random.randint(0,self.max_x)*self.diameter
                
                    if self.destination-self.pos[0]<0: # go left
                        self.direction = [-1,0]
                    elif self.destination-self.pos[0]>0: # go right
                        self.direction = [1,0]
                    else:
                        self.direction = [0,1]
                        
                if self.pos[0]==self.destination:
                    self.direction = [0,1]
                
            self.pos[0]+=self.speed*self.direction[0]
            self.pos[1]+=self.speed*self.direction[1]
            
        if self.pos[1]>self.max_y:
            self.pos = [-self.radius*2, self.radius*2]
            self.delay = random.randint(8, 20)*100
            self.destination=random.randint(0,self.max_x)*self.diameter
                
        


    def render(self, screen):
        pygame.draw.circle(screen, [255,0,0], self.pos, self.radius)





class Shot(object):
    
    def __init__(self, pos):
        self.radius = 3
        self.speed = 7
        self.pos = pos
    def update(self):
        self.pos[1]-=self.speed
    def render(self, screen, pic):
        screen.blit(pic, [self.pos[0]-self.radius,self.pos[1]-self.radius])





class Explosion(object):
    
    def __init__(self, pos):
        self.org_life=20
        self.life = 20
        self.pos = pos
        self.particals = []
        for x in xrange(50):
            self.particals.append(Partical(pos, random_direction(), random.randint(1,50)/10.0, random.randint(93,100)/100.0))
    def render(self, screen):
        for dot in self.particals:
            dot.update()
            dot.render(screen)
        self.life-=1





class Partical(object):
    
    def __init__(self, pos, direction, speed, slow_down_rate):
        self.slow_down_rate = slow_down_rate
        self.speed = speed
        self.direction = direction
        self.pos = [ float(pos[0]),float(pos[1]) ]
        self.colors = [ [255,0,0], [255,255,0],[255,255,255] ]
        random.shuffle(self.colors, random.random)
        for color in self.colors:
            random.shuffle(color, random.random)
    def update(self):
        self.pos[0]+=self.direction[0]*self.speed
        self.pos[1]+=self.direction[1]*self.speed
        
        self.speed*=self.slow_down_rate
        
        if self.speed<0.001:
            self.speed=0
            
        
    def render(self, screen):
        pygame.draw.rect(screen, self.colors[0], [int(self.pos[0]), int(self.pos[1]), 0 ,0])





class Ship:
    
    def __init__(self, screen_size):
        self.dead = False
        self.image = pygame.image.load("ship.gif")
        self.shoot_sound = pygame.mixer.Sound("shot.wav")
        self.pos = [ screen_size[0]/2,screen_size[1]-self.image.get_height()-40 ]
        self.max_x = screen_size[0]-self.image.get_width()
        self.speed = 6
        self.shot_delay = 0
        self.xspeed = 0
        
    def update(self, shot_list):
        if not self.dead:
            keys = pygame.key.get_pressed()

            if keys[K_LEFT] and self.pos[0]-self.image.get_width()/2>0:
                self.xspeed-=3
                self.shot_delay_length = 13
            elif keys[K_RIGHT] and self.pos[0]+self.image.get_width()/2<self.max_x:
                self.xspeed+=3
                self.shot_delay_length = 13
            else:
                self.shot_delay_length = 22
                if self.xspeed!=0:
                    self.xspeed-=(abs(self.xspeed)/float(self.xspeed))/3.0
                elif abs(self.xspeed)<1.0:
                    self.xspeed=0.0

            if abs(self.xspeed)>self.speed:
                self.xspeed=(abs(self.xspeed)/self.xspeed)*self.speed
                

            if keys[K_SPACE] and self.shot_delay==0:
                self.shot_delay = self.shot_delay_length
                self.shoot_sound.play()
                shot_list.append(Shot( [self.pos[0],self.pos[1]] ))

            if self.shot_delay>0:
                self.shot_delay-=1

        self.pos[0]+=self.xspeed

        if self.pos[0]>self.max_x+self.image.get_width()/2:
            self.pos[0]=self.max_x+self.image.get_width()/2
        elif self.pos[0]<self.image.get_width()/2:
            self.pos[0]=self.image.get_width()/2
                
            
    def render(self, screen):
        screen.blit(self.image, [self.pos[0]-self.image.get_width()/2,self.pos[1]-self.image.get_height()/2])



class AiShip:
    def __init__(self, screen_size):
        self.dead = False
        self.image = pygame.image.load("ship.gif")
        self.shoot_sound = pygame.mixer.Sound("shot.wav")
        self.pos = [ screen_size[0]/2,screen_size[1]-self.image.get_height()-40 ]
        self.max_x = screen_size[0]-self.image.get_width()
        self.max_y = screen_size[1]
        self.shot_delay = 0
        self.shot_delay_length = 13
        self.xspeed = 0
        
    def update(self, shot_list, chain):
        if not self.dead:
            closest=self.max_x
            closest_x=0
            closest_y=self.max_y
            
            for section in chain:
                if section.leader == None and abs(self.pos[0]-section.pos[0])<closest and abs(section.pos[1]-self.pos[1])<=closest_y:
                    closest = abs(self.pos[0]-section.pos[0])
                    closest_x = section.pos[0]
                    closest_y = abs(section.pos[1]-self.pos[1])

            if closest_x-self.pos[0]<0 and self.pos[0]-self.image.get_width()/2>0:
                self.xspeed-=random.randint(0,2)
            elif closest_x-self.pos[0]>0 and self.pos[0]+self.image.get_width()/2<self.max_x:
                self.xspeed+=random.randint(0,2)
            else:
                if self.xspeed!=0:
                    self.xspeed-=abs(self.xspeed)/self.xspeed

            if abs(self.xspeed)>6:
                self.xspeed=(abs(self.xspeed)/self.xspeed)*6
                

            if closest<20 and self.shot_delay==0:
                self.shot_delay = self.shot_delay_length
                self.shoot_sound.play()
                shot_list.append(Shot( [self.pos[0],self.pos[1]] ))

            if self.shot_delay>0:
                self.shot_delay-=1

        self.pos[0]+=self.xspeed
                
            
    def render(self, screen):
        screen.blit(self.image, [self.pos[0]-self.image.get_width()/2,self.pos[1]-self.image.get_height()/2])




class LifeSystem(object):
    
    def __init__(self,screen):
        self.lifes = 3
        self.points_get_life_prev = 0
        self.pos = screen[1]
        self.max_x = screen[0]
        self.sound  =  pygame.mixer.Sound("life.wav")
        self.image = pygame.image.load("ship.gif")
    def update(self, points):
        if self.points_get_life_prev!=points/50000 and self.lifes!=3:
            self.lifes+=1
        self.points_get_life_prev = points/50000
    def render(self, screen):
        x = 0
        for y in xrange(self.lifes):
            screen.blit(self.image, [ self.max_x-((x+1)*self.image.get_width()) ,self.pos-self.image.get_height()])
            x+=1
    def remove_life(self):
        self.lifes-=1
        if self.lifes==0:
            return True
        return False
        




class DelaySwitch(object):
    
    def __init__(self, frame_rate):
        self.frame_rate = 1.0/(frame_rate/100.0) # should be in milliseconds
        self.time = 0
        self.prev_time = 0
        self.time_passed = 0
    def update(self):
        self.time=time.time()
        self.time_passed = self.time-self.prev_time
        if self.time_passed<self.frame_rate:
            time.sleep((self.frame_rate-self.time_passed)/100.0)
        self.prev_time = self.time

class PauseSwitch(object):
    
    def __init__(self):
        self.paused = False
        self.pressed = False
    def update(self):
        keys = pygame.key.get_pressed()
        
        if self.pressed and not keys[K_RETURN]:
            if self.paused:
                self.paused = False
            else:
                self.paused = True
        self.pressed = keys[K_RETURN]




        
class InputText(object):
    
    def __init__(self, pos):
        self.pos = pos
        self.text_size=13
        self.text = pygame.font.Font("Quadrit.ttf", self.text_size)
        self.letters = ["_","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P",
                        "Q","R","S","T","U","V","W","X","Y","Z","1","2","3","4","5","6","7","8","9","0"]
        self.type_pos = 0
        self.words = [0,0,0]
        self.press_delay=20
        self.delay=0
        self.done=False

        
    def update(self,screen):
        keys = pygame.key.get_pressed()
        
        # MOVE CURSER
        if keys[K_RIGHT] and self.type_pos!=2 and self.delay==0:
            self.delay=self.press_delay
            self.type_pos+=1
        elif keys[K_LEFT] and self.type_pos!=0 and self.delay==0:
            self.delay=self.press_delay
            self.type_pos-=1
        # CHANGE LETTERS
        elif keys[K_UP] and self.delay==0:
            if self.words[self.type_pos]==len(self.letters)-1:
                self.words[self.type_pos]=0
            else:
                self.words[self.type_pos]+=1

            self.delay=self.press_delay
        elif keys[K_DOWN] and self.delay==0:
            if self.words[self.type_pos]==0:
                self.words[self.type_pos]=len(self.letters)-1
            else:
                self.words[self.type_pos]-=1

            self.delay=self.press_delay
        # DONE
        elif keys[K_RETURN]:
            self.done=True

            
        if self.delay!=0:
            self.delay-=1

        x=0
        for letter in self.words:
            screen.blit(self.text.render(self.letters[letter], True, [255,255,255]), [self.pos[0]+x,self.pos[1]])
            x+=self.text_size

        pygame.draw.rect(screen,[255,255,255], [  self.pos[0]+self.type_pos*self.text_size,    self.pos[1]+self.text_size*2,   self.text_size-3,   3  ])

    def get_input(self):
        text=""
        for letter in self.words:
            text=text+self.letters[letter]
        return text


class HighScoreSystem(object):
    def __init__(self):
        self.highscores=[]
        self.info=file("highscores.ads")
        
    def read_highscores(self):
        import string
        self.highscores=[]
        self.info.seek(0)
        
        scores_level=9
        while scores_level!=0:
            line = string.split(self.info.readline(), " ")
            
            level=int(line[1])
            score=int(line[0])
            name=line[3]
            date=line[2]

            self.highscores.append([score, level, date, name])
            
    def add_highscore(self, level, score, name, date):
        self.highscores.pop()
        self.highscores.append([score, level, date, name])
        self.highscores.sort(highscore_sorter, reverse=True)

    def save_highscores(self):
        self.info.seek(0)

            ##########################
            
        
                
        
        
            
            
        


class Game(object):
    def __init__(self,screen_size, Ai_ship=False):
        self.Ai_ship = Ai_ship
        self.screen_size=screen_size
        self.level=1
        self.lifesystem=LifeSystem(self.screen_size)
        self.score=0
        self.gameover=False

        self.chain_pic = pygame.image.load("chain.gif")
        self.shot_pic = pygame.image.load("shot.gif")
        self.boom_sound = pygame.mixer.Sound("boom.wav")

        self.text = pygame.font.Font("Quadrit.ttf", 13)

        self.Pause = PauseSwitch()
        self.reset()
        
    def reset(self):
        self.chain=[]
        self.shots=[]
        self.booms=[]
        self.bonus=Bonus(self.screen_size)
        self.stars=[]
        
        if not self.Ai_ship:
            self.player=Ship(self.screen_size)
        else:
            self.player=AiShip(self.screen_size)

        for x in xrange(50+self.level):#chain
            self.chain.append(Section(x, self.screen_size))
        for x in xrange(100): #stars
            speed = (random.randint(5,25)+random.randint(-3,3))/22.0
            color = (speed*22-1)/28.0*255
            self.stars.append(Partical( [ random.randint(0,self.screen_size[0]),random.randint(0,self.screen_size[1]) ] , [0,1], speed, 1.0) )
            self.stars[-1].colors= [ [color,color,color] ]
            
    def update(self):
        if self.level==200 and not self.player.dead:
                 player.dead = True
    
        # UPDATES
        if not self.Pause.paused:
            if not self.player.dead:

                
                self.bonus.update()


                
                for section in self.chain:
                    if section.dead:
                        self.chain.remove(section)
                        self.score+=50
                    else:
                        if section.pos[1]>self.screen_size[1]-40:
                            self.player.dead = True
                        section.update(self.chain)


      
            if not self.Ai_ship:
                self.player.update(self.shots)
            else:
                self.player.update(self.shots, self.chain)
                


    
            for shot in self.shots:
                shot.update()
                
                if shot.pos[1]>2:
                    
                    for section in self.chain:
                        if math.sqrt(  (shot.pos[0]-section.pos[0])**2 + (shot.pos[1]-section.pos[1])**2 ) <= shot.radius+section.radius:
                            section.dead = True
                            try : self.booms.append(Explosion(shot.pos)), self.shots.remove(shot), self.boom_sound.play()
                            except : pass
                            
                    if math.sqrt(  (shot.pos[0]-self.bonus.pos[0])**2 + (shot.pos[1]-self.bonus.pos[1])**2 ) <= shot.radius+self.bonus.radius:
                        try :
                            self.booms.append(Explosion(self.bonus.pos))
                            self.bonus = Bonus(self.screen_size)
                            self.score+=5000
                            self.shots.remove(shot)
                            self.boom_sound.play()
                        except : pass
                else:
                    self.shots.remove(shot)



            for star in self.stars:
                star.update()
                if star.pos[1]>self.screen_size[1]:
                    star.pos[1]=0
                    star.pos[0]=random.randint(0,self.screen_size[0])



            if self.player.dead and self.lifesystem.lifes!=0:
                time.sleep(0.5)
                self.lifesystem.remove_life()
                print self.lifesystem.lifes
                self.reset()
            elif self.lifesystem.lifes==0:
                self.gameover=True
        
                
            self.lifesystem.update(self.score)


            if len(self.chain)==0:
                time.sleep(0.2)
                self.score+=1000
                self.level+=1
                self.reset()

        self.Pause.update()


        
    def render(self,screen):
        # RENDERING
        self.bonus.render(screen)
        
        for boom in self.booms:
            boom.render(screen)
            if boom.life<=0:
                self.booms.remove(boom)
                
        for section in self.chain:
            section.render(screen, self.chain_pic)
            
        if not self.player.dead : self.player.render(screen)
        
        for shot in self.shots:
            shot.render(screen, self.shot_pic)
            
        for star in self.stars:
            star.render(screen)
            
        pygame.draw.rect(screen, [0,0,0], [0,self.screen_size[1]-40,self.screen_size[0],self.screen_size[1]])
        self.lifesystem.render(screen)
        
        screen.blit(self.text.render(str(self.score), True, [255,255,255]), [5,self.screen_size[1]-25])
        screen.blit(self.text.render(str(self.level), True, [255,255,255]), [300,self.screen_size[1]-25])

    



def random_direction():
    angle = math.radians(random.randint(0,360))
    x = math.sin(angle)
    y = math.cos(angle)
    return [x,y]

def highscore_sorter(highscore):
    return highscore[0]

    


############################
############################
        
game = Game(size, True)
Clock=DelaySwitch(80)

while True:
    # === ANTI-CRASH ===
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT or keys[K_ESCAPE]:
            pygame.quit(); sys.exit()

    # DELAY
    Clock.update()

    # DISPLAY UPDATE
    game.update()
    game.render(screen)
    
    pygame.display.flip()
    screen.fill([0,0,0])

         
 
                
            
                    
