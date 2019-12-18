#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  4 15:04:37 2019

@author: frankzhou
"""
import random
import pygame
import time
pygame.init()

win = pygame.display.set_mode((528,402))
pygame.display.set_caption("Running-Man")

#clock var
clock = pygame.time.Clock()

game_over = pygame.image.load('imgs/game_over.png')

class Player(object):
    walkRight = [pygame.image.load('imgs/R1.png'), pygame.image.load('imgs/R2.png'), pygame.image.load('imgs/R3.png'), pygame.image.load('imgs/R4.png'), pygame.image.load('imgs/R5.png'), pygame.image.load('imgs/R6.png'), pygame.image.load('imgs/R7.png'), pygame.image.load('imgs/R8.png'), pygame.image.load('imgs/R9.png')]
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.isJump = False
        self.walkCount = 0
        self.jumpCount = 9
        self.hitbox = (self.x+17, self.y+11 ,29,52)
    def walk(self):
        
        self.walkCount = (self.walkCount+1)%len(self.walkRight)
        
    def jump(self):
        man.walkCount = 0
        if self.jumpCount >= -9:
            neg = 1
            if self.jumpCount < 0:
                neg = -1
            self.y -= self.jumpCount**2 * 0.6*neg 
            self.jumpCount -= 1.5
        else:
            self.isJump = False
            self.jumpCount = 9
            
    def draw(self,win):
        win.blit(self.walkRight[self.walkCount],(self.x,self.y))
        self.hitbox = (self.x+17, self.y+11 ,29,52)
#        pygame.draw.rect(win,(255,0,0),self.hitbox,2)

class Background(object):
    bg = pygame.image.load('imgs/bg.jpg')
    def __init__(self,x,y,width,height,vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        
        
    def move(self):
        if self.x > -528:
            self.x -= self.vel
        else:
            self.x = 528
            
    def draw(self,win):
        win.blit(self.bg,(self.x,self.y))
    
class Cloud(object):
    cloud = pygame.image.load('imgs/cloud.png')
    def __init__(self,width,height,vel):
        self.x = 528
        self.y = random.randint(0,200)
        self.width = width
        self.height = height
        self.vel = vel
    
    def move(self):
        self.x -= self.vel
    
    def draw(self,win):
        win.blit(self.cloud,(self.x,self.y))

class Projectile(object):
    def __init__(self,x,y,radius,color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 8
    
    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)        

class Barrier(object):
    barrier = pygame.image.load('imgs/barrier.png')
    def __init__(self,x,y,width,height,vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.hitbox = [[self.x,self.y+self.height],[self.x+self.width,self.y+self.height],[self.x+self.width//2,self.y]]
        self.isHit = False
        
    
    def move(self):
        self.x -= self.vel
    def draw(self,win):
        win.blit(self.barrier,(self.x,self.y))
        
        self.hitbox =  [[self.x,self.y+self.height],[self.x+self.width,self.y+self.height],[self.x+self.width//2,self.y]]
        
#        pygame.draw.polygon(win, (255,0,0), self.hitbox, 5)
    
    def hit(self,other):
        if (self.x < other.hitbox[0]+other.hitbox[2]-5 < self.x + self.width  or self.x < other.hitbox[0]  < self.x + self.width) and (self.y < other.hitbox[1] + other.hitbox[3] < self.y + self.height+100):
            self.isHit = True
    

class Bird(object):
    bird = pygame.image.load('imgs/bird.png')
    def __init__(self,x,y,width,height,vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.hitbox = (self.x+10, self.y+18, self.width-20, self.height-18)
        self.isShot = False
        self.isHit = False
        self.counter = 0
    
    def move(self):
        self.x -= self.vel
        
    def draw(self,win):
        win.blit(self.bird,(self.x,self.y))
        self.hitbox = (self.x+10, self.y+18, self.width-20, self.height-18)
#        pygame.draw.rect(win,(255,0,0),self.hitbox,2)
    
    def shot(self,other):
        if self.hitbox[0] < other.x < (self.hitbox[0]+self.hitbox[2]) and self.hitbox[1]< other.y < self.hitbox[1]+self.hitbox[3]:
            self.isShot = True
    
        
        
            
    
        
def drawWindow():
    for each in bgs:
        each.draw(win)
        each.move()
        
    if barriers == []:           
        barriers.append(Barrier(528 + 20, 330, 20, 20, 10))
    elif barriers[-1].x < random.randint(100,200):
        for i in range(random.randint(1,3)):           
            barriers.append(Barrier(528 + 20*i, 330, 20, 20, 10))
    for each in barriers:
        each.draw(win)
        each.move()
        each.hit(man)
        if each.x<-(each.width+10):
            barriers.remove(each)
        

    if len(clouds) == 0:
        clouds.append(Cloud(152,100,2))
    elif len(clouds) < 3 and clouds[-1].x <300:
        clouds.append(Cloud(152,100,2))
    for each in clouds:
        each.draw(win)
        each.move()
        if each.x<-(each.width+10):
            clouds.remove(each)
        
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE and len(bullets) <10:
            bullets.append(Projectile(round(man.x+man.width//2),round(man.y+man.height//2 + 5),3,(0,0,0)))
        if event.key == pygame.K_UP:
            man.isJump = True
            man.walkCount = 0
    

    
    for bullet in bullets:
        if bullet.x >= 528:
            bullets.pop(bullets.index(bullet))
        for bird in birds:
            bird.shot(bullet)
            if bird.isShot:
                bullets.pop(bullets.index(bullet))
            
            
        else:
            bullet.x += bullet.vel
            
        bullet.draw(win)
    
    for bird in birds:
        bird.move()
        if not bird.isShot:
            bird.draw(win)
        else:
            bird.counter += 1
            if bird.counter % 3 == 0:
                bird.draw(win)
            if bird.counter >= 27:
                birds.pop()
                birds.append(Bird(1000, 235, 80, 107, 10))
            
    man.draw(win)
    man.walk()
    if man.isJump:
        man.jump()


        

    pygame.display.update()
    


man = Player(80,290,64,64)
bgs = [Background(0,0,528,402,10),Background(528,0,528,402,10)]
clouds = []
bullets = []
barriers = []
birds = [Bird(600, 235, 80, 107, 10)]
#b = Barrier(528,330,20,20,20)
run = True
gameOver = False
totalTime = 0
printCount = 0
while run:
    clock.tick(27)
    
    #check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    if not gameOver:
        
        drawWindow()
        for each in barriers:
            if each.isHit:
                gameOver = True
        totalTime += 0.04
    else:
        
        win.blit(game_over,(0,0))
        pygame.display.update() 
        if printCount == 0:
#            print(round(totalTime))
            printCount+=1


pygame.quit()

    
    
    

