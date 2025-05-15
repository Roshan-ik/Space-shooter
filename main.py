
import os
import time
from random import randint
import pygame

pygame.init()
width,height=1200,720
display= pygame.display.set_mode((width,height))
running = True
clock = pygame.time.Clock()
score = 0

meteor_surf = pygame.image.load(os.path.join('images','meteor.png')).convert_alpha()
explosion_frames = [pygame.image.load(os.path.join('images','frames',f'{i}.png')).convert_alpha()for i in range(11)]
#sound
laser_sound = pygame.mixer.Sound(os.path.join('sound','laser.wav'))
laser_sound.set_volume(0.5)
explosion_sound = pygame.mixer.Sound(os.path.join('sound','explosion.wav'))
explosion_sound.set_volume(0.5)
damage_sound = pygame.mixer.Sound(os.path.join('sound','damage.ogg'))
game_sound = pygame.mixer.Sound(os.path.join('sound','game_music.wav'))
game_sound.play()




#load
def starting_page():
    waiting = True
    while waiting:
        display.fill('black')
        starting_line = pygame.font.Font(None, 45)
        starting_surf = starting_line.render("""WELCOME TO MY SPACE SHOOTER GAME""", True, 'white')
        starting_rect = starting_surf.get_rect(midbottom=(width / 2, height / 2))
        display.blit(starting_surf, starting_rect)

        start_line = pygame.font.Font(None, 45)
        start_surf = start_line.render("PRESS ANY KEY TO CONTINUE", True, 'white')
        start_rect = start_surf.get_rect(midbottom=(width / 2,440))
        display.blit(start_surf, start_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting = False
starting_page()

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
            laser_sound.play()
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
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = 0
        self.laser()
class Star(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.image = pygame.image.load(os.path.join('images','star.png'))
        self.rect = self.image.get_rect(center = (randint(0,width),randint(0,height)))
class Meteor(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.original_image = meteor_surf  # Store the original image
        self.image = self.original_image
        self.rect = self.image.get_rect(center = (width/2,height/2))
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 2000
        self.mask = pygame.mask.from_surface(self.image)
        self.turn = 0
    def update(self,dt):
        self.rect.centery  += 300 * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
        self.turn += 100 * dt
        self.image = pygame.transform.rotate(self.original_image, self.turn)
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center

        self.mask = pygame.mask.from_surface(self.image)
class Laser(pygame.sprite.Sprite):
    def __init__(self,groups,pos,surf):
        super().__init__(groups)
        self.image = pygame.image.load(os.path.join('images','laser.png'))
        self.rect = self.image.get_rect(midbottom = pos)

    def update(self,dt):
        self.rect.y -= 300 * dt
        if self.rect.y <  0 :
            self.kill()
class Animation(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.frame = explosion_frames
        self.frame_index = 0
        self.image =explosion_frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)
    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frame):
            self.image = self.frame[int(self.frame_index)]
            explosion_sound.play()
        else:
            self.kill()


def collision():
    global running,score
    break1 = pygame.sprite.spritecollide(player, meteor_sprite, True)
    if break1:
        end_page()
        running = False
    for laser in laser_sprite:
        collide = pygame.sprite.spritecollide(laser, meteor_sprite, True)
        if collide:
            score += len(collide)
            laser.kill()
            Animation(laser.rect.midtop,all_sprites)
def end_page():
    display.fill('black')
    end = pygame.font.Font(None, 45)
    end_surf = end.render("GAME OVER", True, 'white')
    end_rect = end_surf.get_rect(midbottom=(width / 2, height / 2))
    display.blit(end_surf, end_rect)
    pygame.display.update()
    time.sleep(3)


def display_score():
    current_time = pygame.time.get_ticks()//1000
    font = pygame.font.Font(None, 22)
    text_surf = font.render(str(current_time), True, 'white')
    text_rect = text_surf.get_rect(midbottom = (width/2,50))
    display.blit(text_surf,text_rect)


    global score
    score_text = pygame.font.Font(None, 41)
    score_surf = score_text.render(str(f"SCORE = {score}"), True, 'white')
    score_rect = score_surf.get_rect(midbottom=(width // 2, height - 80))
    pygame.draw.rect(display, 'white', score_rect.inflate(10,20), width=3, border_radius=9)
    display.blit(score_surf, score_rect)

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
    dt=clock.tick(60)/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            meteor = Meteor([all_sprites,meteor_sprite])
            meteor.rect.center = (randint(0, width), -50)

    display.fill('black')

    all_sprites.update(dt)
    collision()
    display_score()
    all_sprites.draw(display)
    display.blit(player.image, player.rect)

    pygame.display.update()

pygame.quit()