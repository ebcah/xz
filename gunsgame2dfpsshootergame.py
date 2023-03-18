import pygame as pg
from random import randint
import time
pg.init()
score=0
bossAnimation=0
window=pg.display.set_mode((800,600))
pg.display.set_caption("gunsgame2dfpsshootergame")
missEnemy=0

level=1
gameover="win.gif"

class GameSprite:
    def __init__(self, img, x, y, width, height, speed):
        self.image=pg.transform.scale(pg.image.load(img),(width,height))
        self.width=width
        self.height=height
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.speed=speed
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def control(self):
        keys=pg.key.get_pressed()
        if keys[pg.K_LEFT] and self.rect.x>0:
            self.rect.x-=self.speed
            self.rect.x-=self.speed
        if keys[pg.K_RIGHT] and self.rect.x<700:
            self.rect.x+=self.speed
            self.rect.x+=self.speed








class boss_enemy(GameSprite):
    def respawn(self):
        
        global bullets
        for i in bullets:
            if pg.sprite.collide_rect(self,i):
                if len(enemies2)>=1:
                    enemies2.remove(self)

    def move(self):
        global missEnemy
        if self.rect.y<600:
            self.rect.y+=self.speed
        else:
            missEnemy+=1
            self.respawn()
    
        
           









class Enemy(GameSprite):
    def respawn(self):
        self.rect.y=0
        self.rect.x=randint(0,700)

    def move(self):
        global missEnemy
        if self.rect.y<600:
            self.rect.y+=self.speed
        else:
            missEnemy+=1
            self.respawn()
    def dead(self):
        global bullets, score
        for i in bullets:
            if pg.sprite.collide_rect(self,i):
                score+=1
                self.respawn()
                bullets.remove(i)
class boss(GameSprite):
    def __init__(self, img, x, y, width, height, speed, health, direction):
        super().__init__(img, x, y, width, height, speed)
        self.health=health
        self.direction=direction
        


    def move(self):
        global bossAnimation
        if self.direction==1:
            self.rect.x+=self.speed
            #print("right")
            #print(self.rect.x)
        elif self.direction==2:
            self.rect.x-=self.speed
            #print("left")
            #print(self.rect.x)
        if self.rect.x<100 and self.direction!=1:
            self.direction-=self.direction
            self.direction+=1
            print("leftasd")
        elif self.rect.x>500 and self.direction!=2:
            self.direction-=self.direction
            self.direction+=2
            print("rightasd")
        
        
        
        
        
        
        
            self.rect.x-=self.speed
        self.image=pg.transform.scale(pg.image.load(f"boss/{bossAnimation}.png"),(self.width,self.height))
        bossAnimation+=1
        
        if bossAnimation==42:
            global enemies2
            a=randint(1,3)
            if a==1 and len(enemies2)==0:
                for i in range(randint(5,8)):
                    global e_bullets
                    e_bullets.append(Bullet_enemy("e_bullets.png", randint(1,700), Boss.rect.y+20, 30, 50, 10))
            elif a==2 and len(enemies2)==0:
                for i in range(randint(2,5)):
                    
                    enemies2.append(boss_enemy("enemy1.png",randint(0,700),0,100,100,randint(1,6)))
            else:
                ...
        if bossAnimation>44:
            bossAnimation=0
    def damage(self):
        global bullets
        for i in bullets:
            if pg.sprite.collide_rect(self,i):
                bullets.remove(i)
                self.health-=0.5

    

    


class Bullet(GameSprite):
    def move(self):
        self.rect.y-=self.speed
class Bullet_enemy(GameSprite):
    def move(self):
        self.rect.y+=self.speed
    

background=GameSprite("galaxy.png",0,0,800,600,0)
player=Player("11.png",400,500,100,100,5)
Boss=boss("boss/0.png",250,0,300,200,2,100,1)
enemies=[]
bullets=[]
e_bullets=[]
for i in range(10):
    enemies.append(Enemy("enemy1.png",randint(0,700),0,100,100,randint(1,3)))
game=True
music = pg.mixer.Sound("rok.mp3")
music.set_volume(0.75)
music.play(-1)
asd=0
enemies2=[]
while game:
    
    if asd==1:
        enemies.clear()
        asd=2
    if score>20:
        level+=1
        score=0
        
        
        
    pg.time.Clock().tick(30)
    for i in pg.event.get():
        if i.type==pg.QUIT:
            exit()
        if i.type==pg.MOUSEBUTTONDOWN:
            bullets.append(Bullet("bullet.png", player.rect.x+40, player.rect.y, 20, 35, 10))
    background.reset()
    if level>=3:
        Boss.reset()
        asd=1
        hp=GameSprite("hp.png", 0,0,Boss.health*8, 40, 0)
        hp.reset()
        Boss.damage()
        Boss.move()
        
    player.reset()
    player.control()
    if Boss.health<=0:
        gameover="win.gif"
        game=False
        
            
    for i in enemies2:
        i.reset()
        i.respawn()

        i.move()
        if pg.sprite.collide_rect(i,player) or missEnemy>3:
            gameover="lose.jpg"
            game=False
       




    for i in bullets:
        i.reset()
        i.move()
    for i in enemies:
        i.reset()
        i.move()
        i.dead()
        if pg.sprite.collide_rect(i,player) or missEnemy>3:
            gameover="lose.jpg"
            game=False
    for i in e_bullets:
        i.reset()
        i.move()
        if pg.sprite.collide_rect(i,player):
            gameover="lose.jpg"
            game=False
        
    
    label=pg.font.SysFont("Arial", 25).render(f"Score: {score}",True,(206, 106, 39))
    window.blit(label,(20,20))
    label=pg.font.SysFont("Arial", 25).render(f"LEVEL: {level}",True,(206, 106, 39))
    window.blit(label,(600,20))
    pg.display.flip()
music.stop()
bg=GameSprite(gameover,0,0,800,600,0)
while True:
    pg.time.Clock().tick(60)
    for i in pg.event.get():
        if i.type==pg.QUIT:
            exit()
    bg.reset()
    pg.display.flip()
