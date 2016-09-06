################################################################################
##                          PokePengo                                         ##
##                          Player Class                                      ##
##                                                                            ##
##              Programmed by Ryun Valdez                                     ##
##                                                                            ##
################################################################################

#Initiate
import pygame
import Tile

#PlayerClass
class player(pygame.sprite.Sprite):
    def __init__(self,x=7,y=8):
        self.speed = 2
        #Image variables
        self.i=1
        self.j=0
        #Awareness
        self.location=Tile.tile.grid[x][y]
        self.radar=Tile.tile.grid[x][y+1]
        self.radar2=Tile.tile.grid[x][y+2]
        #Directions
        self.move_dir = ''
        self.move_Q = ''
        self.face_dir = 'down'
        self.stopping = False
        self.opening = False
        #Initialize image
        self.playerSheet = pygame.image.load('Graphics/player_sheet.png')
        self.playerSheet.set_clip(pygame.Rect(0,0, 32,32))
        self.playerImg = self.playerSheet.subsurface(self.playerSheet.get_clip())
        self.rect = self.playerImg.get_rect()
        pygame.sprite.Sprite.__init__(self)
        #Place rect object at image location
        self.rect.topleft = (x*32,y*32+64)
        self.x = self.rect.x
        self.y = self.rect.y
        #Set timing
        self.last = pygame.time.get_ticks()
        self.cooldown = 250
        
    def x2grid(self,x):
        xgrid = int(x/32)
        return xgrid

    def y2grid(self,y):
        ygrid = int((y-64)/32)
        return ygrid
    def scanTiles(self):
        #Empty old location
        self.location.empty()
        #Update new location
        self.location = Tile.tile.grid[self.x2grid(self.x)][self.y2grid(self.y)]
        #Fill new location
        self.location.fill(self)
        #Left
        if self.face_dir=='left':
            self.radar=Tile.tile.grid[self.x2grid(self.x)-1][self.y2grid(self.y)]
            if (self.x2grid(self.x)-2)<0:
                self.radar2=None
            else:
                self.radar2=Tile.tile.grid[self.x2grid(self.x)-2][self.y2grid(self.y)]
        #Right
        elif self.face_dir=='right':
            self.radar=Tile.tile.grid[self.x2grid(self.x)+1][self.y2grid(self.y)]
            if (self.x2grid(self.x)+2)>14:
                self.radar2=None
            else:
                self.radar2=Tile.tile.grid[self.x2grid(self.x)+2][self.y2grid(self.y)]
        #Up
        elif self.face_dir=='up':
            self.radar=Tile.tile.grid[self.x2grid(self.x)][self.y2grid(self.y)-1]
            if (self.y2grid(self.y)-2)<0:
                self.radar2=None
            else:
                self.radar2=Tile.tile.grid[self.x2grid(self.x)][self.y2grid(self.y)-2]
        #Down
        elif self.face_dir=='down':
            self.radar=Tile.tile.grid[self.x2grid(self.x)][self.y2grid(self.y)+1]
            if (self.y2grid(self.y)+2)>16:
                self.radar2=None
            else:
                self.radar2=Tile.tile.grid[self.x2grid(self.x)][self.y2grid(self.y)+2]
                
    def move(self):
        #Scan Player Vision
        if self.x%32==0 and self.y%32==0:
            self.scanTiles()
        if self.move_dir == 'left':
            self.j = 1
            if self.radar.solid==True:
                None
            else:
                self.x -= self.speed
            now = pygame.time.get_ticks()
            if now - self.last >= self.cooldown-200:
                self.last = now
                self.i+=1
                if self.i > 2:
                    self.i=0
        elif self.move_dir == 'right':
            self.j = 2
            if self.radar.solid==True:
                None
            else:
                self.x += self.speed
            now = pygame.time.get_ticks()
            if now - self.last >= self.cooldown-200:
                self.last = now
                self.i+=1
                if self.i > 2:
                    self.i=0
        elif self.move_dir == 'up':
            self.j = 3
            if self.radar.solid==True:
                None
            else:
                self.y -= self.speed
            now = pygame.time.get_ticks()
            if now - self.last >= self.cooldown-100:
                self.last = now
                self.i+=1
                if self.i > 2:
                    self.i=1
        elif self.move_dir == 'down':
            self.j = 0
            if self.radar.solid==True:
                None
            else:
                self.y += self.speed
            now = pygame.time.get_ticks()
            if now - self.last >= self.cooldown-100:
                self.last = now
                self.i+=1
                if self.i > 2:
                    self.i=1
        else:
            self.i = 0
        #Object Location Update
        self.rect.topleft = (self.x,self.y)

    def update(self, surface):
        #Current Frame Update    
        self.playerSheet.set_clip(pygame.Rect(self.i*32,self.j*32, 32,32))
        self.playerImg = self.playerSheet.subsurface(self.playerSheet.get_clip())
        #Image Location Update
        surface.blit(self.playerImg,(self.x,self.y))





