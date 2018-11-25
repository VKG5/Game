# Pygame template - skeleton for the game

import pygame
import random
import os                                           #Will help us access system folders

WIDTH = 1024
HEIGHT = 600
FPS = 60                                            #Times/sec screen is updated

# Define colours to reuse again and again    (RGB ntotation)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


pygame.init()                                       
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("UNKNOWN WORLD")


# To define/draw text
font_name = pygame.font.match_font("Arial")
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    # True, if you want to anti alias the font
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.center = (x/2,y/2)
    surf.blit(text_surface, text_rect)


font_name = pygame.font.match_font("Bebas")
def draw_text1(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    # True, if you want to anti alias the font
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.center = (x/2,y/2)
    surf.blit(text_surface, text_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
    
def draw_shield_bar(surf, x, y, pct):
    if(pct < 0):
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 15
    fill = (pct/100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, BLUE, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_health_bar(surf, x, y, pct):
    if(pct < 0):
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 15
    fill = (pct/100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)



# SET UP ASSETS
game_folder = os.path.dirname(__file__)
i_folder = os.path.join(game_folder, "Graphics")
imagep_folder = os.path.join(i_folder, "Player")     #To access the folder with images
imagee_folder = os.path.join(i_folder, "Enemy")
imageg_folder = os.path.join(i_folder, "LEVELS")
imagea_folder = os.path.join(i_folder, "Attacks")
snd_dir = os.path.join(game_folder, "Sounds")



def show_go_screen():
    draw_text1(screen, "UNKNOWN WORLD", 96, WIDTH, HEIGHT/4)
    draw_text1(screen, "WASD or Arrow Keys to move, Space to attack", 44, WIDTH, HEIGHT/2)
    draw_text1(screen, "Press any key to begin", 36, WIDTH, HEIGHT * 3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYUP:
                waiting = False


class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Can change size of player by pygame.transform.scale(player_image, (50,30))
        self.background = pygame.image.load(os.path.join(imageg_folder, "Starting.png")).convert()
        self.background_rect = self.background.get_rect()

class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(os.path.join(imagep_folder, "Animation1.png")).convert()
        self.image.set_colorkey(WHITE)
        self.shoot_snd = pygame.mixer.Sound(os.path.join(snd_dir, "Shoot1.ogg"))
        self.shoot_snd.set_volume(0.7)
        
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 3)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.rect.bottom = HEIGHT - 30
        self.speedx = 0
        self.speedy = 0
        self.shield = 100
        self.health = 100
        self.shoot_delay = 1000
        self.last_shot = pygame.time.get_ticks()

    def update(self):            
        self.image = pygame.image.load(os.path.join(imagep_folder, "Animation1.png")).convert()
        self.image.set_colorkey(WHITE)
        self.radius = int(self.rect.width / 3)
        
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()         #Keyword for getting the input of the key

        if(keystate[pygame.K_SPACE]):
            self.shoot()
            
        if(keystate[pygame.K_a] or keystate[pygame.K_LEFT]):
            self.speedx = -5
            self.image = pygame.image.load(os.path.join(imagep_folder, "Animation2.png")).convert()
            self.image.set_colorkey(WHITE)
            self.radius = int(self.rect.width / 3)

        elif(keystate[pygame.K_d] or keystate[pygame.K_RIGHT]):
            self.speedx = 5
            self.image = pygame.image.load(os.path.join(imagep_folder, "Animation3.2.png")).convert()
            self.image.set_colorkey(WHITE)
            self.radius = int(self.rect.width / 3)

        self.rect.x += self.speedx

        if(keystate[pygame.K_w] or keystate[pygame.K_UP]):
            self.speedy = -5
            self.image = pygame.image.load(os.path.join(imagep_folder, "Animation4.png")).convert()
            self.image.set_colorkey(WHITE)
            self.radius = int(self.rect.width / 3)

        elif(keystate[pygame.K_s] or keystate[pygame.K_DOWN]):
            self.speedy = 5

        self.rect.y += self.speedy

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left <0:
            self.rect.left = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if((now - self.last_shot) > self.shoot_delay):
            self.last_shot = now
            bullet = Bullet(self.rect.center, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.shoot_snd.play()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(os.path.join(imagee_folder, "Animation1.png")).convert()
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 3)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1,8)
        self.speedx = random.randrange(-3,3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if(self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH +20):
             self.rect.x = random.randrange(WIDTH - self.rect.width)
             self.rect.y = random.randrange(-100, -40)
             self.speedy = random.randrange(1,8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image_org = pygame.image.load(os.path.join(imagea_folder, "ball0.png")).convert()
        self.image_org.set_colorkey(WHITE)
        self.image = self.image_org.copy()
        
        self.image = pygame.Surface((10,10))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.center = x
        self.speedy = -10

        self.rot = 0
        self.rot_speed = 25

        # tick() is tick of clocks, gives ticks since game started
        self.last_update = pygame.time.get_ticks()
        
    def rotate(self):
        now = pygame.time.get_ticks()
        if( now - self.last_update > 50):
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360 
            new_image = pygame.transform.rotate(self.image_org, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
    
    def update(self):
        self.rotate()
        self.image = pygame.image.load(os.path.join(imagea_folder, "ball0.png")).convert()
        self.image.set_colorkey(WHITE)
        
        self.rect.y += self.speedy
        
        #kill if it goes off screen
        if self.rect.bottom < 0:
            self.kill()                             #kill(), command to delete sprite

class power_up(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        
        self.power_images = {}
        self.power_images["Shield"] = pygame.image.load(os.path.join(imagea_folder, "power_shield.png")).convert()
        self.power_images["Health"] = pygame.image.load(os.path.join(imagea_folder, "power_health.png")).convert()
        
        self.type = random.choice(["Shield", "Health"])
        self.image = self.power_images[self.type]
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.center = center
        
    def update(self):        
        #kill if it goes off screen
        if self.rect.bottom < 0:
            self.kill()                             #kill(), command to delete sprite





sound = pygame.mixer.Sound(os.path.join(snd_dir, "Undertale Piano Concerto.ogg"))
#sound.set_volume()




# GAME LOOP
game_over = True
running = True
while(running):
    if game_over:
        show_go_screen()
        game_over = False
                                 
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        bg = Background()
        powerups = pygame.sprite.Group()
        all_sprites.add(player)

        for i in range(16):
                newmob()

        score = 0
        sound.play()
        



    # Keep loop running at the right speed
    clock.tick(FPS)

    # Process input(events)
    for event in pygame.event.get():
        #check for closing the window
        if event.type == pygame.QUIT:
            running = False
              




    # Update
    all_sprites.update()

    #check to see if bullet hit mob
    # (True, True) so that both the bullet and mob get deleted 
    hits = pygame.sprite.groupcollide(bullets, mobs, True, True)
    for hit in hits:
        score += 1
        if random.random() > 0.7:
            power = power_up(hit.rect.center)
            all_sprites.add(power)
            powerups.add(power)
        newmob()

    # Check if player hit a powerup
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == "Shield":
            player.shield += 15
            if player.shield > 100:
                player.shield = 100

        if hit.type == "Health":
            player.health += 7
            if player.health > 100:
                player.health = 100        
        
    # check to see if mob hit player
    #return list,spritecollide(check sprite, GROUP to check against, TRUE/FALSE to delete the sprite)
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= 20
        if player.shield <= 0:
            player.health -= 15
            if player.health <= 0:
                running = False
        newmob()
        




    # Draw/render
    screen.fill(BLACK)
    screen.blit(bg.background, bg.background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 72, WIDTH, HEIGHT)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_health_bar(screen, 110, 5, player.health)
    # *after* drawing everything. Flip the display
    pygame.display.flip()
    
pygame.quit()

