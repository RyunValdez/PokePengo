################################################################################
##                          PokePengo                                         ##
##                          Enemy Class                                       ##
##                                                                            ##
##              Programmed by Ryun Valdez                                     ##
##                                                                            ##
################################################################################

import pygame
import random
import Tile
import Pokeball

class enemy(pygame.sprite.Sprite):

    s = pygame.sprite.Group()
    opening = pygame.sprite.Group()
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, enemy.s)
        self.speed = 2
        #Variables
        self.i=0
        self.j=3
        self.x = x*32
        self.y = y*32+64
        self.spawn = (self.x,self.y)
        self.choice = random.choice([0,1,2,3,4,5,6,7,8,9])
        #Awareness
        self.location=Tile.tile.grid[x][y]
        self.radar=Tile.tile.grid[x][y+1]
        #Move Direction
        self.move_dir = 'down'
        self.directions = ['left','right','up','down']
        #Initialize image
        self.enemySheet = pygame.image.load('Graphics/pikachu_sheet.png')
        self.enemySheet.set_clip(pygame.Rect(0,0, 32,32))
        self.enemyImg = self.enemySheet.subsurface(self.enemySheet.get_clip())
        self.rect = pygame.Rect(0,0, 1,1)
        #Place rect object in a location that makes collisions look more realistic
        #(janky)
        self.rect.topleft = (self.x+17,self.y+20)
        #Set timing
        self.last = pygame.time.get_ticks()
        self.cooldown = 800

    def chase(self, player):
        if self.x%32==0 and self.y%32==0:
            if self.choice >= 8:
                self.move_dir = self.directions[int(random.random()*3)+1]
            else:
                x_dif = player.x-self.x
                y_dif = player.y-self.y
                if abs(x_dif)>abs(y_dif):
                    if x_dif<=0:
                        self.move_dir = 'left'
                    else:
                        self.move_dir = 'right'
                elif abs(x_dif)<abs(y_dif):
                    if y_dif<=0:
                        self.move_dir = 'up'
                    else:
                        self.move_dir = 'down'
                else:
                    self.move_dir = self.directions[int(random.random()*3)+1]

        
    def respawn(self):
        self.x = self.spawn[0]
        self.y = self.spawn[1]
        self.rect.topleft = (self.x+17,self.y+20)
    
    def x2grid(self,x):
        xgrid = int(x/32)
        return xgrid

    def y2grid(self,y):
        ygrid = int((y-64)/32)
        return ygrid
    def scanTiles(self):
        #Not working, cyclical reference don't really need now anyway...
        #they check to see if they got player, and pokeball v enemy works on all rolling pokeballs
##        #Empty old location
##        self.location.empty()
##        #Update new location
##        self.location = Tile.tile.grid[self.x2grid(self.x)][self.y2grid(self.y)]
##        #Fill new location
##        self.location.fill(self)
        #Left
        if self.move_dir=='left':
            self.radar=Tile.tile.grid[self.x2grid(self.x)-1][self.y2grid(self.y)]
        #Right
        elif self.move_dir=='right':
            self.radar=Tile.tile.grid[self.x2grid(self.x)+1][self.y2grid(self.y)]
        #Up
        elif self.move_dir=='up':
            self.radar=Tile.tile.grid[self.x2grid(self.x)][self.y2grid(self.y)-1]
        #Down
        elif self.move_dir=='down':
            self.radar=Tile.tile.grid[self.x2grid(self.x)][self.y2grid(self.y)+1]

    def openPokeball(self, pokeball):
        pokeball.breakTime = pygame.time.get_ticks()
        Pokeball.pokeball.breaking.add(pokeball)
        enemy.opening.add(self)
            
    def move(self):
        looks = 0
        directions = self.directions
        random.shuffle(directions)
        #Scan Enemy Vision
        if self.x%32==0 and self.y%32==0:
            if self not in enemy.opening:
                self.scanTiles()
                self.choice = random.choice([0,1,2,3,4,5,6,7,8,9])
        for looks in range(0,3):
            if self.radar.solid==True:
                if self.radar.object in Pokeball.pokeball.s and self.choice>=5:
                    if self.radar.object not in Pokeball.pokeball.breaking:
                        if self not in enemy.opening:
                            self.openPokeball(self.radar.object)
                            if self.move_dir == 'left':
                                self.i = 1
                                self.j = 0
                            elif self.move_dir == 'right':
                                self.i = 1
                                self.j = 2
                            elif self.move_dir == 'up':
                                self.i = 0
                                self.j = 0
                            elif self.move_dir == 'down':
                                self.i = 0
                                self.j = 2
                    else: #pokeball is breaking
                        if self in enemy.opening:
                            None
                        else:
                            self.move_dir = directions[looks]
                            self.scanTiles()
                            looks+=1
                            #this shouldn't ever happen, unless it is surrounded
                            if looks == 3 and self.radar.solid==True:
                                return 
                    return
                else: #not a pokeball
                    self.move_dir = directions[looks]
                    self.scanTiles()
                    looks+=1
                    #this shouldn't ever happen, unless it is surrounded
                    if looks == 3 and self.radar.solid==True:
                        return 
            else: #not solid
                break
        if self in enemy.opening:
            enemy.opening.remove(self)   
        if self.move_dir == 'left':
            self.i = 1
            self.j = 0
            self.x -= self.speed
            now = pygame.time.get_ticks()
            if now - self.last >= self.cooldown:
                self.last = now
                self.j+=1
                if self.j == 2:
                    self.j=0
        elif self.move_dir == 'right':
            self.i = 1
            self.j = 2
            self.x += self.speed
            now = pygame.time.get_ticks()
            if now - self.last >= self.cooldown:
                self.last = now
                self.j+=1
                if self.j == 4:
                    self.j=2
        elif self.move_dir == 'up':
            self.i = 0
            self.j = 0
            self.y -= self.speed
            now = pygame.time.get_ticks()
            if now - self.last >= self.cooldown:
                self.last = now
                self.j+=1
                if self.j == 2:
                    self.j=0
        elif self.move_dir == 'down':
            self.i = 0
            self.j = 2
            self.y += self.speed
            now = pygame.time.get_ticks()
            if now - self.last >= self.cooldown:
                self.last = now
                self.j+=1
                if self.j == 4:
                    self.j=2
        #Object Location Update
        self.rect.topleft = (self.x+17,self.y+20)          
    
    def update(self, surface):
        #Current Frame Update    
        self.enemySheet.set_clip(pygame.Rect(self.i*32,self.j*32, 32,32))
        self.enemyImg = self.enemySheet.subsurface(self.enemySheet.get_clip())
        #Image Location Update
        surface.blit(self.enemyImg,(self.x,self.y))
