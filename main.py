
import os 
from random import randint
import pygame
from scipy.constants import metric_ton

pygame.init()

width,height=1200,720
display= pygame.display.set_mode((width,height))
running = True
clock = pygame.time.Clock()

#load
import images
class Player(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.image = pygame.image.load(os.path.join('images','spaceship.png')).convert_alpha()
        self.rect = self.image.get_rect(center=(width/2,height/2))
        self.direction = pygame.Vector2(0,0)
        self.speed = 200
    #cooldown
        self.cooldown_duration = 400
        self.can_shoot = True
        self.laser_shoot = 0
    def laser(self):
        current_time = pygame.time.get_ticks()
        if not self.can_shoot and current_time - self.laser_shoot >= self.cooldown_duration:
            self.can_shoot = True
    def update(self,dt):
        keys= pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_SPACE] and self.can_shoot:
            Laser((all_sprites,laser_sprite), self.rect.midtop, self.image)
            self.can_shoot = False
        self.rect.center += self.direction  * self.speed * dt
        self.laser()

class Star(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.image = pygame.image.load(os.path.join('images','star.png'))
        self.rect = self.image.get_rect(center = (randint(0,width),randint(0,height)))
class Meteor(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.image = meteor_surf
        self.rect = self.image.get_rect(center = (width/2,height/2))
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 2000
    def update(self,dt):
        self.rect.centery  += 300 * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
meteor_surf = pygame.image.load(os.path.join('images','meteor.png')).convert_alpha()
class Laser(pygame.sprite.Sprite):
    def __init__(self,groups,pos,surf):
        super().__init__(groups)
        self.image = pygame.image.load(os.path.join('images','laser.png'))
        self.rect = self.image.get_rect(midbottom = pos)

    def update(self,dt):
        self.rect.y -= 300 * dt
        if self.rect.y <  0 :
            self.kill()
all_sprites = pygame.sprite.Group()
meteor_sprite = pygame.sprite.Group()
laser_sprite = pygame.sprite.Group()
player = Player(all_sprites)
for i in range(20):
    Star(all_sprites)




meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event,1000)
#loop
while running:
    dt=clock.tick(30)/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            meteor = Meteor([all_sprites,meteor_sprite])
            meteor.rect.center = (randint(0, width), -50)
        #display
    pygame.sprite.spritecollide(player,meteor_sprite,True)
    for laser in laser_sprite:
        collide = pygame.sprite.spritecollide(laser,meteor_sprite,True)
        if collide:
            laser.kill()
    display.fill('black')
    all_sprites.update(dt)
    all_sprites.draw(display)
    display.blit(player.image, player.rect)
    pygame.display.update()

pygame.quit()