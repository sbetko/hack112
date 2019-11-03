import random, math, copy
import numpy as np
import pygame
import sys
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
        self.vel = 20
        self.y = screen.get_height()/2
        self.x = screen.get_width()/2
        self.jumping = False
        self.dy = 0

    def jump(self):
        if self.jumping == False:
            self.jumping = True
            self.dy = -30

    def doPhysics(self):
        if self.jumping == True:
            self.y += self.dy
            self.dy += 3
        if self.y >= screen.get_height()/2:
            self.jumping = False
            self.y = screen.get_height()/2

    def draw(self, screen):
        cx = self.x- self.width/2
        cy = self.y - self.height/2
        pygame.draw.rect(screen, self.color, (cx, cy, self.width, self.height))

class Dot(object):
    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y
        self.r = r
        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

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
            dot.x = dot.x - scrollX
            dot.draw(screen)

##########################################
# MAIN ###################################
##########################################

def randomColor():
    return tuple(np.random.random(size=3) * 256)

me = Player(50, 50, randomColor())
# could take list of colors
background0 = Background(screen.get_width()*4, screen.get_height())
background1 = Background(screen.get_width()*4, screen.get_height())

running = True
pygame.mixer.music.play()
while running:

    pygame.time.delay(27)
    scrollX = 0

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
    
    scrollX += me.vel
    me.doPhysics()
    

    screen.fill((0, 0, 0))
    background0.draw(screen, scrollX*.8)
    me.draw(screen)
    background1.draw(screen, scrollX)
    pygame.display.update()

pygame.quit()