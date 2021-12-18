import sys, random
import pygame, pygame_gui

#Constants
GAMESTATE = 'MAIN_MENU'
SCREENRECT = pygame.Rect(0,0,600,800)
FIRE = 5
#define our sprite groups and add them into super constructors to initiate
all = pygame.sprite.RenderUpdates()
shots = pygame.sprite.Group()
enemies = pygame.sprite.Group()
Menu = pygame.sprite.Group()
enemyshots = pygame.sprite.Group()
playerG = pygame.sprite.Group()

pygame.init()
clock = pygame.time.Clock()
#custom user event with timer
SpawnNow = pygame.event.Event(pygame.USEREVENT + 1)
pygame.time.set_timer(SpawnNow,3000,5)
#Enemy Shot timer
Shoot = pygame.event.Event(pygame.USEREVENT + 2)
pygame.time.set_timer(Shoot, 500)

#GUI Manager
manager = pygame_gui.UIManager((SCREENRECT.size))
#GUi element
spawn_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (100, 50)),text='Spawn Enemey',manager=manager)
screen = pygame.display.set_mode(SCREENRECT.size)
#Init classes
class Player(pygame.sprite.Sprite):
    #Base player class that handles movement and a method for getting the objects pos(gunpos)
    speed = 5
    images = ''
    health_capacity = 100
    current_health = health_capacity

    def __init__(self):
        super().__init__(all,playerG)
        self.image = self.images
        self.rect = self.image.get_rect(midbottom=(300,780))
        self.reloading = 0
        self.HealthBar = pygame_gui.elements.ui_screen_space_health_bar.UIScreenSpaceHealthBar(relative_rect=pygame.Rect((10,780),(100,20)),
                                                                                                    manager=manager,sprite_to_monitor=Player)
    def Move(self, direction):
        self.rect.x += (direction * self.speed)
        if self.rect.left < 0:
            self.rect.right=(600)
        elif self.rect.right > 600:
            self.rect.left=(0)

    def gunpos(self):
        pos = self.rect.midtop
        return pos

class Shot(pygame.sprite.Sprite):

    images = ''

    def __init__(self,pos):
        super().__init__(all,shots)
        self.image = self.images
        self.rect = self.image.get_rect(midbottom = pos)

    def update(self):
        self.rect.move_ip(0,-10)
        if self.rect.y <= 0:
            self.kill()

class EnemyShot(pygame.sprite.Sprite):

    images = ''

    def __init__(self,pos):
        super().__init__(all,enemyshots)
        self.image = self.images
        self.rect = self.image.get_rect(midbottom = pos)

    def update(self):
        self.rect.move_ip(0,10)
        if self.rect.y >= 800:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    images = ''
    startdirection = 1
    damage = 10

    def __init__(self):
        super().__init__(all,enemies)
        self.image = self.images
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(100,500)
        self.rect.y = 100
        self.direction = self.startdirection
        self.HP = 2
        self.Fire = 5


    def gunpos(self):
        pos = self.rect.midbottom
        return pos

    def update(self):
        if self.direction > 0:
            self.rect.move_ip(1 * self.direction,0)
            if self.rect.right > 600:
                self.direction = -1
        elif self.direction < 0:
            self.rect.move_ip(1 * self.direction,0)
            if self.rect.left < 0:
                self.direction = 1
        self.rect = self.rect.clamp(SCREENRECT)
        if len(playerG.sprites()) == 0:
            self.kill()
        if self.HP <= 1:
            self.image = pygame.image.load('Images\EnemyImages\\ufo2.png')

class MAINMENU(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(Menu)
        self.PlayButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 50), (100, 50)),text='Play',manager=manager)
        self.InfoButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 0), (100, 50)),text='Info',manager=manager)
        self.gamestate = "Main Menu"
        self.PlayAgain = None
        self.Quit = None
        self.MenuPanel = None

    def RetryScreen(self):
        self.MenuPanel = pygame_gui.elements.ui_panel.UIPanel(relative_rect=pygame.Rect((100,100),(400,400)), starting_layer_height=0,manager=manager)
        pygame_gui.elements.ui_label.UILabel(relative_rect=pygame.Rect((90,0),(200,50)),text='You Died! Play Again?',manager=manager,container = self.MenuPanel)
        self.PlayAgain = pygame_gui.elements.ui_button.UIButton(relative_rect=pygame.Rect((150,150),(100,50)), text='Play Again?', manager=manager, container=self.MenuPanel)
        self.Quit = pygame_gui.elements.ui_button.UIButton(relative_rect=pygame.Rect((150,200),(100,50)), text='Quit', manager=manager, container=self.MenuPanel)

class Background():
    def __init__(self):
        self.bgimage = pygame.image.load('Images\\BackgroundImages\Space Background.png')
        self.rectBGimg = self.bgimage.get_rect()
        self.bgY1 = 0
        self.bgX1 = 0
        self.bgY2 = self.rectBGimg.height
        self.bgX2 = 0
        self.moving_speed = 1

    def update(self):
        self.bgY1 -= self.moving_speed
        self.bgY2 -= self.moving_speed
        if self.bgY1 <= -self.rectBGimg.height:
            self.bgY1 = self.rectBGimg.height
        if self.bgY2 <= -self.rectBGimg.height:
            self.bgY2 = self.rectBGimg.height

    def render(self):
        screen.blit(self.bgimage, (self.bgX1, self.bgY1))
        screen.blit(self.bgimage, (self.bgX2, self.bgY2))


def main():
    #setup main screen
    screen = pygame.display.set_mode(SCREENRECT.size)
    surface = pygame.Surface(screen.get_size())
    #initialize the screen extras
    pygame.display.set_caption('Space Invaders Test 2')
    pygame.display.set_icon(pygame.image.load('SpaceInvadersLogo.png'))

    #setup and display the background
    back_ground = Background()
    pygame.display.flip()

    #Load and prepare images
    Player.images = pygame.image.load('Images\PlayerImages\PlayerImg.png')
    Shot.images = pygame.image.load('Images\ProjectileImages\\bullet.png')
    EnemyShot.images = pygame.image.load('Images\ProjectileImages\\bomb.png')
    Enemy.images = pygame.image.load('Images\EnemyImages\\ufo.png')


    menu = MAINMENU()
    #Create starting Sprites
    while menu.gamestate == 'Main Menu':
        time_delta = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == menu.PlayButton:
                        menu.gamestate = 'Play'
                        menu.PlayButton.kill()
                        menu.InfoButton.kill()

        back_ground.update()
        back_ground.render()
        manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()

    paused = False
    player = Player()
    while menu.gamestate == 'Play':
        time_delta = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            # if event.type == pygame.USEREVENT + 1:
            #     Enemy.Spawn(Enemy())
            #     print('Spawned')
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == spawn_button:
                        enemy = Enemy()
                    if event.ui_element == menu.PlayAgain:
                        menu.MenuPanel.kill()
                        Player.current_health = Player.health_capacity
                        main()
                    if event.ui_element == menu.Quit:
                        return

            if event.type == pygame.USEREVENT + 2:
                #sprite_list = enemies.sprites()
                for enemy in enemies.sprites():
                    enemy.Fire = random.randint(0,10)
                    if enemy.Fire == FIRE:
                        EnemyShot(enemy.gunpos())


            #Pause
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
        if paused == True:
            continue

        else:
            #process GUI events in event loop
            manager.process_events(event)
            manager.update(time_delta)

            all.clear(screen,surface)
            all.update()

            keystate = pygame.key.get_pressed()
            direction = keystate[pygame.K_RIGHT] - keystate[pygame.K_LEFT]
            player.Move(direction)
            fireing = keystate[pygame.K_SPACE]
            if not player.reloading and fireing:
                shot = Shot(player.gunpos())
            player.reloading = fireing

            #Collision detection
            for enemy in pygame.sprite.groupcollide(enemies,shots,0,1).keys():
                #shot.kill()
                enemy.HP -= 1
                print(enemy.HP)
                if enemy.HP <= 0:
                    enemy.kill()

            for player in pygame.sprite.groupcollide(playerG, enemyshots,0,1).keys():
                Player.current_health -= Enemy.damage
                print(player.current_health)
                if Player.current_health <= 0:
                    player.kill()
                    #menu.gamestate = 'Retry'
                    menu.RetryScreen()

            #draw elements to screen
            back_ground.update()
            back_ground.render()
            manager.draw_ui(screen)
            dirty = all.draw(screen)
            pygame.display.update(dirty)
            #update entire screen again just in case
            pygame.display.update()


if __name__ == '__main__':
    main()
    pygame.quit()
