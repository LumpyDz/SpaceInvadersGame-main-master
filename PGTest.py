import sys, pygame
import random as R

#Player
class PlayerBase(pygame.sprite.Sprite):
    gun_offset = -11

    def __init__(self, playerImg = '', HP = 0, X = 0, Y = 0):
        super().__init__()
        self.playerImg = pygame.image.load(playerImg)
        self.rect = self.playerImg.get_rect()
        self.score = 0
        self.HP = HP
        self.X = X
        self.Y = Y
        self.firedState = 0
        self.playerSpeed = 0
        self.lKey = False
        self.rKey = False
        self.facing = -1

    def UpdatePosition(self,X,Y):
        #Player movement and quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.playerSpeed = -0.1
                        self.lKey = True
                        print('lkey down')
                    if event.key == pygame.K_RIGHT:
                        self.playerSpeed = 0.1
                        self.rKey = True
                        print('rkey down')
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.lKey = False
                    elif event.key == pygame.K_RIGHT:
                        self.rKey = False
                    if self.lKey == False and self.rKey == False:
                        self.playerSpeed = 0
        #Adjust speed based on above input
        self.X += self.playerSpeed
        #Screen bounds for going off screen
        if self.X <= 20:
            self.X = 620
        elif self.X >= 620:
            self.X = 20
        #Update Screen
        screen.blit(self.playerImg, (self.X-32,self.Y-32))



    def gunpos(self):
        pos = self.facing * self.gun_offset + self.rect.centerx
        return pos, self.rect.top

class BasePlayerProjectile(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('bullet.png')
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = .1
        self.damage = 10

    def update(self):
        #screen.blit(self.image,(self.X,self.Y))
        self.rect.move_ip(100,self.speed)
        if self.rect.top <= 0:
            self.kill()



#Enemy
class EnemyBase(pygame.sprite.Sprite):
    def __init__(self, enemyImg='', HP = 0, score = 0, enemyX=300 ,enemyY=780):
        pygame.sprite.Sprite.__init__(self)
        self.enemyImg = pygame.image.load(enemyImg)
        self.rect = self.enemyImg.get_rect()
        self.HP = HP
        self.score = score
        self.X = enemyX
        self.Y = enemyY

    #def Move(self,X,Y):
#BLAHB

pygame.init()
#create screen
screen = pygame.display.set_mode((600,800))

#Title and Icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('SpaceInvadersLogo.png')
pygame.display.set_icon(icon)

#PlayerStuff
#start point in middle bottom of screen

#Enemy Stuff
enemyCount = 0

# def Enemy():
#     enemy1 = EnemyBase('ufo.png', 10, 10, 250,250)
#     screen.blit(enemy1.enemyImg,(enemy1.X - 32,enemy1.Y - 32))
#defualt spawn location is 300,780
player1 = PlayerBase('PlayerImg.png', 10, 300, 780)
#Game Loop
running = True

enemies = pygame.sprite.Group()
shots = pygame.sprite.Group()
all = pygame.sprite.RenderUpdates()

PlayerBase.containers = all
EnemyBase.containers = enemies, all
BasePlayerProjectile.containers = all, shots

while running:
    #screen color controls backgrounnd color and adjusts pixels when other objects move over portions of the screen that we do not want to change
    #all.update()
    screen.fill((255,200,0))
    #Move Player and screen bounds
    player1.UpdatePosition(player1.X,player1.Y)
    keystroke = pygame.key.get_pressed()

    fireing = keystroke[pygame.K_SPACE]
    if not player1.firedState and fireing:
        BasePlayerProjectile(player1.gunpos())
        print('fired')
    player1.reloading = fireing
    pygame.display.flip()
    #Enemy()
    dirty = all.draw(screen)
    pygame.display.update(dirty)
    screen.fill((255,200,0))
