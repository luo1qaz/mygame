import pygame #导入pygame模块
import math
from os import path
import random

pygame.init()  #初始化pygame
width = 800
height=600

screen=pygame.display.set_mode([width,height]) #窗口宽600，高400
keep_going=True #控制游戏退出的变量
black=(0,0,0)

img_dir = path.join(path.dirname(__file__),"img")
snd_dir = path.join(path.dirname(__file__),"snd")

background=pygame.image.load(path.join(img_dir,"background.jpg"))
playerimg = pygame.image.load(path.join(img_dir,"player.png"))

bgmusic=pygame.mixer.music.load("D:\\study\\python\\Space_War-master\\snd\\game.mp3")
pygame.mixer.music.play(-1)
bulletup=pygame.mixer.Sound("D:\\study\\python\\Space_War-master\\snd\\bulletup.wav")

mybulletimg=pygame.image.load("D:\\study\\python\\Space_War-master\\img\\laser1.png")


explodebg_sound = pygame.mixer.Sound(path.join(snd_dir,"explodebg.wav")) #爆炸声音
explodesm_sound = pygame.mixer.Sound(path.join(snd_dir,"explodesm.wav")) #爆炸声音
explodedeath_sound = pygame.mixer.Sound(path.join(snd_dir,"explodedeath.wav")) #爆炸声音
shoot_sound=pygame.mixer.Sound(path.join(snd_dir,"shoot.wav")) #射击声音

explosion_anim = []
explosion_anim.append(pygame.image.load(path.join(img_dir,"regularExplosion00.png")))
explosion_anim.append(pygame.image.load(path.join(img_dir,"regularExplosion01.png")))
explosion_anim.append(pygame.image.load(path.join(img_dir,"regularExplosion02.png")))
explosion_anim.append(pygame.image.load(path.join(img_dir,"regularExplosion03.png")))
explosion_anim.append(pygame.image.load(path.join(img_dir,"regularExplosion04.png")))
explosion_anim.append(pygame.image.load(path.join(img_dir,"regularExplosion05.png")))
explosion_anim.append(pygame.image.load(path.join(img_dir,"regularExplosion06.png")))
explosion_anim.append(pygame.image.load(path.join(img_dir,"regularExplosion07.png")))
explosion_anim.append(pygame.image.load(path.join(img_dir,"regularExplosion08.png")))

explodebg =pygame.mixer.Sound("D:\\study\\python\\Space_War-master\\snd\\explodebg.wav")


bullet_sprites = pygame.sprite.Group() #子弹精灵组
all_sprites = pygame.sprite.Group()  #所有精灵组
enemy1_sprites =pygame.sprite.Group() #1号敌人精灵

#玩家精灵
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(playerimg,(70,50))
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2
        self.rect.bottom = height - 20
        self.speedx = 0
        self.speedy = 0
        self.live=3
        self.ph=50
        self.lastshoot=pygame.time.get_ticks()
        self.shootdelay = 100 #射击延时
        
    def shoot(self): #射击
        now = pygame.time.get_ticks()
        if now - self.lastshoot > self.shootdelay:
            self.lastshoot = now
            shoot_sound.play() #射击音效
            bullet=Mybullet(self.rect.centerx,self.rect.y,math.pi/2.0) #创造一个子弹
            bullet_sprites.add(bullet)
            all_sprites.add(bullet)

    def update(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_d]:
            self.speedx = 6
        if keystate[pygame.K_a]:
            self.speedx = -6
        if keystate[pygame.K_w]:
            self.speedy = -6
        if keystate[pygame.K_s]:
            self.speedy = 6
        if keystate[pygame.K_j]:
            self.shoot()
            
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        
        if self.ph < 0:
            expl = Explosion(self.rect.center)
            explodedeath_sound.play()
            all_sprites.add(expl)
            self.live -= 1
            self.ph = 100
            self.kill()
            self.rect.centerx = width / 2
            self.rect.bottom = height - 20

#子弹精灵
class Mybullet(pygame.sprite.Sprite):
    def __init__(self,x,y,radian):
        pygame.sprite.Sprite.__init__(self)
        self.image = mybulletimg
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.x = x
        self.speed = -15
        self.speedx = math.cos(radian)*self.speed
        self.speedy = math.sin(radian)*self.speed

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (self.rect.bottom < 0) or (self.rect.right < 0) or (self.rect.left > width):
            self.kill()

roundbulletimg = pygame.image.load(path.join(img_dir,"roundbullet.png"))
#敌人子弹
class Roundbullet(pygame.sprite.Sprite):
    def __init__(self,x,y,degree):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(roundbulletimg,(30,30))
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 7
        self.speedx = self.speed*math.sin(math.radians(degree))
        self.speedy = self.speed * math.cos(math.radians(degree))

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if (self.rect.top > height) or (self.rect.right < 0) or (self.rect.left > width):
            self.kill()

enemy1img = pygame.image.load(path.join(img_dir,"enemy1.png"))
roundbullet_sprites =pygame.sprite.Group()
#敌人精灵
class Enemy1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_org = pygame.transform.scale(enemy1img,(90,70))
        self.image_org.set_colorkey(black)
        self.image = self.image_org.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,width-self.rect.width)
        self.rect.y = -random.randrange(300,1300)
        self.radius = int(self.rect.width * 0.85 / 2)
        self.speedy = 3
        self.rotate_time = pygame.time.get_ticks()
        self.angle = 0
        self.shoot_time = pygame.time.get_ticks()
        self.shoot_delay = 1000
        self.ph = 70
        self.fullph = 70
        self.drawph = False

    def rotate(self,angle):
        now = pygame.time.get_ticks()
        if now - self.rotate_time > 50:
            self.rotate_time = pygame.time.get_ticks()
            newimage = pygame.transform.rotate(self.image_org,angle)
            oldcenter = self.rect.center
            self.image = newimage
            self.rect = self.image.get_rect()
            self.rect.center = oldcenter

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.shoot_time > self.shoot_delay and self.rect.y > 0:
            self.shoot_time = pygame.time.get_ticks()
            b = Roundbullet(self.rect.centerx, self.rect.centery, self.angle)
            roundbullet_sprites.add(b)
            all_sprites.add(b)

    def enemy_health(self,ph, fullph, x, y):
        container = pygame.Rect(x, y, 150, 20)
        blood = pygame.Rect(x + 1, y + 1, 150 * ph / fullph - 2, 20 - 2)
        pygame.draw.rect(screen, white, container, 1)
        pygame.draw.rect(screen, purple, blood)

    def update(self):
        try:
            self.angle = math.degrees(math.atan((player.rect.x-self.rect.x)/(player.rect.y-self.rect.y)))
        except:
            self.angle = 0
        if player.rect.y < self.rect.y:
            self.angle = 180 + self.angle
        self.rotate(self.angle)
        self.shoot()
        self.rect.y += self.speedy
        if self.rect.y > height:
            self.drawph = False
            self.kill()
            b = Enemy1()
            b.rect.y=0
            enemy1_sprites.add(b)
            all_sprites.add(b)
        if self.ph <= 0:
            self.drawph = False
            expl = Explosion(self.rect.center)
            explodedeath_sound.play()
            all_sprites.add(expl)
            self.kill()
            b = Enemy1()
            b.rect.y=0
            enemy1_sprites.add(b)
            all_sprites.add(b)

# 爆炸精灵
class Explosion(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.update_rate = 90

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.update_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

player = Player()
all_sprites.add(player)
clock = pygame.time.Clock()
fps = 30

enemy1=Enemy1()
enemy1.rect.y = -100
enemy1_sprites.add(enemy1)
all_sprites.add(enemy1)

while keep_going:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            keep_going=False

    clock.tick(fps)
    all_sprites.update()

    #我的子弹击中敌人
    hits = pygame.sprite.groupcollide(bullet_sprites,enemy1_sprites,True,False) 
    for hit in hits:
        expl = Explosion(hit.rect.center)
        explodesm_sound.play()
        all_sprites.add(expl)
        enemy1.drawph = True
        enemy1.ph -= 10

    # 敌机子弹击中我 
    hits = pygame.sprite.spritecollide(player,roundbullet_sprites,True)
    for hit in hits:
        expl = Explosion(hit.rect.center)
        explodesm_sound.play()
        all_sprites.add(expl)
        player.ph -= 10

    screen.blit(background, (0, 0))

    all_sprites.draw(screen)

    pygame.display.update()

    
pygame.quit()
