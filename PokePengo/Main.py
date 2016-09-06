################################################################################
##                          PokePengo                                         ##
##                                                                            ##
##              Programmed by Ryun Valdez                                     ##
##                                                                            ##
################################################################################

#Initiate
from Player import player
import Enemy
import Pokeball
import Specialball
import Wall
import Level
import Tile
import pygame

pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()

#Set Window & Title & Clock
window_width = 480
window_height = 640
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('PokePengo')
clock = pygame.time.Clock()

#Game Variables
lives = 3
score = 0
level = 1

#Initialize Music
Music_1 = pygame.mixer.Sound('Audio/Soundtrack_TrainerMusic.wav')
Music_1.set_volume(0.5)
Music_1.play(-1)

throw = pygame.mixer.Sound('Audio/Ball_throw.wav')  #load sound
catch = pygame.mixer.Sound('Audio/Item.wav')  #load sound
player_collide = pygame.mixer.Sound('Audio/Player_collision.wav')  #load sound
ball_collide = pygame.mixer.Sound('Audio/Ball_collision.wav')  #load sound
player_death = pygame.mixer.Sound('Audio/pikachu_sound.wav')  #load sound
ball_shake = pygame.mixer.Sound('Audio/Ball_shake.wav')  #load sound
ball_shake.set_volume(1.0)
ball_open = pygame.mixer.Sound('Audio/Ball_open.wav')  #load sound
ball_open.set_volume(0.3)

#Initialize Objects
player = player()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Gameloop~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

lPress = False
rPress = False
uPress = False
dPress = False

running = True
while running:

    if lives <= 0:
        Music_1.stop()
        pygame.draw.rect(window,(0,0,0),(0,0, 480, 640))
        
        menufont = pygame.font.SysFont("monospace", 30)
        gameover_text = menufont.render("Game Over!", 1, (255,255,255))
        window.blit(gameover_text, (150, 300))

        pygame.Surface.convert_alpha(window)
        pygame.display.update()

        running = False
        pygame.time.wait(5000)

    if len(Enemy.enemy.s)==0:
        level+=1
        Music_1.stop()
        pygame.draw.rect(window,(0,0,0),(0,0, 480, 640))
        
        menufont = pygame.font.SysFont("monospace", 30)
        levelup_text = menufont.render("Level "+ str(level), 1, (255,255,255))
        window.blit(levelup_text, (160
                                   , 300))

        pygame.Surface.convert_alpha(window)
        pygame.display.update()

        pygame.time.wait(2000)

        for pokeball in Pokeball.pokeball.s:
            pokeball.kill()
        for specialball in Specialball.specialball.s:
            specialball.kill()
            
        Tile.set_level()
        player.x = 224
        player.y = 320
        Music_1.play(-1)
    for event in pygame.event.get():
        #X Button works
        if event.type == pygame.QUIT:
            running = False
        #Keypress events
        #Space press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if player.radar.object in Pokeball.pokeball.s:
                    if player.radar.object not in Pokeball.pokeball.breaking:
                        if player.radar2.solid==True:
                                ball_shake.play()
                                player.radar.object.breakTime = pygame.time.get_ticks()
                                Pokeball.pokeball.breaking.add(player.radar.object)
                                player.opening = True
                        else:
                            if player.face_dir=='left':
                                player.radar.object.roll_dir = 'left'
                            elif player.face_dir=='right':
                                player.radar.object.roll_dir = 'right'
                            elif player.face_dir=='up':
                                player.radar.object.roll_dir = 'up'    
                            else:
                                player.radar.object.roll_dir = 'down'
                            Pokeball.pokeball.rolling.add(player.radar.object)
                            Tile.tile.grid[player.radar.object.x2grid(player.radar.object.x)][player.radar.object.y2grid(player.radar.object.y)].empty()
                            throw.play()
                    else:
                        None
                elif player.radar.object in Specialball.specialball.s:
                    if player.radar2.solid==True:
                        None
                    else:
                        if player.face_dir=='left':
                            player.radar.object.roll_dir = 'left'
                        elif player.face_dir=='right':
                            player.radar.object.roll_dir = 'right'
                        elif player.face_dir=='up':
                            player.radar.object.roll_dir = 'up'    
                        else:
                            player.radar.object.roll_dir = 'down'
                        Specialball.specialball.rolling.add(player.radar.object)
                        Tile.tile.grid[player.radar.object.x2grid(player.radar.object.x)][player.radar.object.y2grid(player.radar.object.y)].empty()
                        throw.play()
                else:
                    None
                
        #Directional Keys
        if event.type == pygame.KEYDOWN and player.move_dir == '':
            if event.key != pygame.K_SPACE:
                if player.radar.object in Pokeball.pokeball.s:
                    if player.opening == True:
                        if player.radar.object.offset != 16:
                            player.radar.object.remove(Pokeball.pokeball.breaking)
            if event.key == pygame.K_LEFT:
                player.move_dir = 'left'
                player.face_dir = 'left'
                lPress = True
            elif event.key == pygame.K_RIGHT:
                player.move_dir = 'right'
                player.face_dir = 'right'
                rPress = True
            elif event.key == pygame.K_UP:
                player.move_dir = 'up'
                player.face_dir = 'up'
                uPress = True
            elif event.key == pygame.K_DOWN:
                player.move_dir = 'down'
                player.face_dir = 'down'
                dPress = True
        #Queue up next direction(smoother controls)
        if event.type == pygame.KEYDOWN and player.move_dir != '':
            if event.key != pygame.K_SPACE:
                if player.radar.object in Pokeball.pokeball.s:
                    if player.opening == True:
                        if player.radar.object.offset != 16:
                            player.radar.object.remove(Pokeball.pokeball.breaking)
            if event.key == pygame.K_LEFT:
                player.move_Q = 'left'
                lPress = True
            elif event.key == pygame.K_RIGHT:
                player.move_Q = 'right'
                rPress = True
            elif event.key == pygame.K_UP:
                player.move_Q = 'up'
                uPress = True
            elif event.key == pygame.K_DOWN:
                player.move_Q = 'down'
                dPress = True
        #Keylift events, keep track of what buttons are pressed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                if player.radar.object in Pokeball.pokeball.s:
                    if player.opening == True:
                        if player.radar.object.offset != 16:
                            player.radar.object.remove(Pokeball.pokeball.breaking)
                player.opening = False
            if event.key == pygame.K_LEFT:
                lPress = False
            elif event.key == pygame.K_RIGHT:
                rPress = False
            elif event.key == pygame.K_UP:
                uPress = False
            elif event.key == pygame.K_DOWN:
                dPress = False 
                
    #Check if all directional keys are lifted
    if lPress==False and rPress==False and uPress==False and dPress==False:
        player.stopping = True
        
    #Change Direction at next coordinate
    if player.x%32==0 and player.y%32==0:
        if player.stopping == False:
            player.move_dir = player.move_Q
            player.face_dir = player.move_Q    
    #Stop at next coordinate if no keys are pressed
        else:
            player.move_dir = ''
            player.stopping = False
        
    #Move
    #Player
    player.move()
    #Enemy
    for enemy in Enemy.enemy.s:
        if enemy not in Enemy.enemy.opening:
            enemy.chase(player)
        enemy.move()
    #Pokeballs
    for pokeball in Pokeball.pokeball.rolling:
        pokeball.roll()
    for specialball in Specialball.specialball.rolling:
        specialball.roll()
    for pokeball in Pokeball.pokeball.breaking:
        success = False
        success=pokeball.destroy(success)
        if success == True:
            ball_open.play()
            success = False
    
    #Collision Detection
    #Pokeball vs. stuff
    for pokeball in Pokeball.pokeball.rolling:
        if pokeball.radar.solid==True:
            if pokeball.rect.colliderect(pokeball.radar.object.rect):
                if pokeball.roll_dir == 'left':
                    pokeball.x = pokeball.radar.object.x+32
                if pokeball.roll_dir == 'right':
                    pokeball.x = pokeball.radar.object.x-32
                if pokeball.roll_dir == 'up':
                    pokeball.y = pokeball.radar.object.y+32
                if pokeball.roll_dir == 'down':
                    pokeball.y = pokeball.radar.object.y-32
                pokeball.roll_dir = ''
                pokeball.remove(Pokeball.pokeball.rolling)
                pokeball.i = 0
                Tile.tile.grid[pokeball.x2grid(pokeball.x)][pokeball.y2grid(pokeball.y)].fill(pokeball)
                ball_collide.play()
            #Save changes made to location
            pokeball.rect.topleft = (pokeball.x,pokeball.y)
            
        for enemy in Enemy.enemy.s:
            if pokeball.rect.colliderect(enemy.rect):
                enemy.kill()
                score += 400
                catch.play()

    #Specialball vs. stuff
    for specialball in Specialball.specialball.rolling:
        if specialball.radar.solid==True:
            if specialball.rect.colliderect(specialball.radar.object.rect):
                if specialball.roll_dir == 'left':
                    specialball.x = specialball.radar.object.x+32
                if specialball.roll_dir == 'right':
                    specialball.x = specialball.radar.object.x-32
                if specialball.roll_dir == 'up':
                    specialball.y = specialball.radar.object.y+32
                if specialball.roll_dir == 'down':
                    specialball.y = specialball.radar.object.y-32
                specialball.roll_dir = ''
                specialball.remove(Specialball.specialball.rolling)
                specialball.i = 0
                Tile.tile.grid[specialball.x2grid(specialball.x)][specialball.y2grid(specialball.y)].fill(specialball)
                ball_collide.play()
            #Save changes made to location
            specialball.rect.topleft = (specialball.x,specialball.y)
            
        for enemy in Enemy.enemy.s:
            if specialball.rect.colliderect(enemy.rect):
                enemy.kill()
                score += 400
                catch.play()

    #Player vs. pokeball
        
    #Player vs. Wall
        
    #Player vs. Enemy
    for enemy in Enemy.enemy.s:
        if enemy.radar.object == player:
            if player.rect.colliderect(enemy.rect):
                for enemy in Enemy.enemy.s:
                    enemy.respawn()
                player.x = 224
                player.y = 320
                lives -= 1
                player_death.play()
                pygame.time.wait(1000)

    #Background
    Background_viridian = pygame.image.load('Graphics/Viridian_in_progress2.png')
    window.blit(Background_viridian,(0,0))
    #Score Board
    pygame.draw.rect(window,(0,0,0),(0,610, 480, 30)) #Background

    Player_lives = pygame.image.load('Graphics/Lives.png')
    i=0
    while i < lives:
        window.blit(Player_lives,(i*20+80,620))
        i+=1
    
    # render text
    myfont = pygame.font.SysFont("monospace", 15)
    lives_text = myfont.render("Lives: ", 1, (255,255,255))
    points_text = myfont.render("Points: "+str(score), 1, (255,255,255))
    level_text = myfont.render("Level: "+str(level), 1, (255,255,255))
    window.blit(level_text, (160, 615))
    window.blit(lives_text, (20, 615))
    window.blit(points_text, (300, 615))
            
    #Update
    player.update(window)
    for pokeball in Pokeball.pokeball.s:
        pokeball.update(window)
    for specialball in Specialball.specialball.s:
        specialball.update(window)
    for enemy in Enemy.enemy.s:
        enemy.update(window)
    pygame.Surface.convert_alpha(window)
    pygame.display.update()
   
    #Timer   
    clock.tick(30)

pygame.quit()
quit()
