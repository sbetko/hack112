import random, math, copy
import numpy as np
import pygame
import sys
from bpmextract import *
pygame.init()

screenWidth = 0
screenHeight = 0
# FULLSCREEN for fullscreen
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)

pygame.display.set_caption("First Game")


directory = str(sys.path[0]) + '/Audio.ogg'
pygame.mixer.music.load(directory)


class Player(object):
    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.color = color
        self.vel = 27
        self.y = screen.get_height()/2
        self.x = screen.get_width()/2
        self.worldX = self.x
        self.jumping = False
        self.dy = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def jump(self):
        if self.jumping == False:
            self.jumping = True
            self.dy = -30

    def updateXPos(self, scrollX):
        self.move(self.vel, 0)
    
    def move(self, dx, dy):
        self.y += dy
        self.worldX += dx
        #self.rect = self.rect.move(dx, dy)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def doPhysics(self):
        if self.jumping == True:
            self.move(0, self.dy)
            self.dy += 3

        if self.y >= screen.get_height()/2:
            self.jumping = False
            self.y = screen.get_height()/2

    def timerFired(self, scrollX):
        doPhysics()
        updateXPos(scrollX)
        updatePyGameRect(scrollX)

    def draw(self, screen):
        cx = self.x- self.width/2
        cy = self.y - self.height/2
        pygame.draw.rect(screen, self.color, (cx, cy, self.width, self.height))
    
    def getBounds(self):
        x0 = self.worldX
        y0 = self.y
        x1 = x0 + self.width
        y1 = y0 + self.height
        return (x0, y0, x1, y1)

class Dot(object):
    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y
        self.r = r
        self.color = color

    def draw(self, screen, scrollX):
        x = self.x - scrollX
        y = self.y
        pygame.draw.circle(screen, self.color, (x, y), self.r)

class Background(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.dots = [ self.randomDot(self.width, self.height, 30) for dot in range(200) ]

    def randomDot(self, mx, my, mr):
        dot = Dot(
            random.randint(1, mx),
            random.randint(1, my),
            random.randint(1, mr),
            randomColor()
        )
        return dot

    def draw(self, screen, scrollX):
        for dot in self.dots:
            dot.x = dot.x
            dot.draw(screen, scrollX)

class Block(object):
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.h = 50
        self.rect = pygame.Rect(x, y, self.h, self.h)
    
    def getBounds(self, scrollX = None):
        x0 = self.x
        y0 = self.y
        x1 = x0 + self.h
        y1 = y0 + self.h
        if scrollX == None:
            return (x0, y0, x1, y1)
        else:
            return (x0 - scrollX, y0, x1 - scrollX, y1)

    def draw(self, screen, scrollX):
        cx = self.x - scrollX - self.h // 2
        cy = self.y - self.h // 2
        w = h = self.h
        pygame.draw.rect(screen, self.color, (cx, cy, w, h))


class Level(object):
    def __init__(self, width, height, bpm):
        self.width = width
        self.height = height
        self.bpm = bpm
        #self.blocks = [Block(2000, height //2, (255, 0, 0))]
        self.blocks = []
        analyzeAudioFile()
        (self.bpm, self.beats, self.quiet, self.noisy) = extractAudioData("audio-data.txt")
        
        for beatTimeIndex in range(len(self.beats)):
            if beatTimeIndex % 4 == 0:
                beatTime = self.beats[beatTimeIndex]
                self.blocks.append(Block(1000*beatTime + screen.get_width()//2, screen.get_height()//2, (255,0,0)))

    def draw(self, screen, scrollX):
        for block in self.blocks:
            block.draw(screen, scrollX)

##########################################
# MAIN ###################################
##########################################

def randomColor():
    return tuple(np.random.random(size=3) * 256)

def boundsIntersect(boundsA, boundsB):
    (ax0, ay0, ax1, ay1) = boundsA
    (bx0, by0, bx1, by1) = boundsB

    if ax0 > ax1: ax0, ax1 = ax1, ax0
    if bx0 > bx1: bx0, bx1 = bx1, bx0
    if ay0 > ay1: ay0, ay1 = ay1, ay0
    if by0 > by1: by0, by1 = by1, by0

    return ((ax1 >= bx0) and (bx1 >= ax0) and
            (ay1 >= by0) and (by1 >= ay0))

def checkCollisions(player, blocks):
    # index = player.rect.collidelist(blocks)
    # print(index)
    # if index != -1:
    #     print("Collision")
    #     return True
    # else:
    #     return False

    for block in blocks:
        boundsA = player.getBounds()
        boundsB = block.getBounds()
        if boundsIntersect(boundsA, boundsB):
            return True
            print("Collision")
    return False

gameOver = False
me = Player(50, 50, randomColor())
# could take list of colors
background0 = Background(screen.get_width()*4, screen.get_height())
background1 = Background(screen.get_width()*4, screen.get_height())
level = Level(screen.get_width()*4, screen.get_height(), 110)
scrollX = 0
running = True
pygame.mixer.music.play()
while running:

    pygame.time.delay(27)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    # if keys[pygame.K_RIGHT]:
    #     scrollX += me.vel
    # if keys[pygame.K_LEFT]:
    #     scrollX -= me.vel
    if keys[pygame.K_SPACE]:
        me.jump()
        
    if checkCollisions(me, level.blocks):
        gameOver = True
    
    if gameOver == False:
        scrollX += me.vel
        me.updateXPos(scrollX)
        me.doPhysics()

    screen.fill((0, 0, 0))
    background0.draw(screen, scrollX*.8)
    me.draw(screen)
    background1.draw(screen, scrollX)
    level.draw(screen, scrollX)
    pygame.display.update()

pygame.quit()