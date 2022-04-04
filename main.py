import pygame
import math
from enemy import Enemy

#zapnutie hry
pygame.init()

#okno hry
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800

#zapnutie okna hry
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defence GAME OF THE YEAR 2022 EDITION")

clock = pygame.time.Clock()
FPS = 60

#load images
bg = pygame.image.load("img/back16002.png").convert_alpha()
#castle
castle_image_100 = pygame.image.load("img/castle.png").convert_alpha()

#bullet
bullet_img = pygame.image.load("img/bullet.png").convert_alpha()
b_w = bullet_img.get_width()
b_h = bullet_img.get_height()
bullet_img = pygame.transform.scale(bullet_img, (int(b_w * 2), int(b_h * 2)))

#load enemies
enemy_animations = []
enemy_types = ["red"]
enemy_health = [75]

animation_types = ["walk"]
for enemy in enemy_types:
    #load animation
    animation_list = []
    for animation in animation_types:
        #reset temporary list of images
        temp_list = []
        num_of_frames = 3
        for i in range(num_of_frames):
            img = pygame.image.load(f"img/enemies/{enemy}/{animation}/{i}.png").convert_alpha()
            e_w = img.get_width()
            e_h = img.get_height()
            img = pygame.transform.scale(img, (int(e_w * 2), int(e_h * 2)))
            temp_list.append(img)
        animation_list.append(temp_list)
    enemy_animations.append(animation_list)







#definuj farby
WHITE = (255,255,255)

#castle class
class Castle():
    def __init__(self, image100, x, y, scale):
        self.health = 1000
        self.max_health = self.health
        self.fired = False

        width = image100.get_width()
        height = image100.get_height()

        self.image100 = pygame.transform.scale(image100, (int(width * scale), int(height * scale)))
        self.rect = self.image100.get_rect()
        self.rect.x = x
        self.rect.y = y

    def shoot(self):
        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.midleft[0]+25
        y_dist = -(pos[1] - self.rect.midleft[1])
        self.angle = math.degrees(math.atan2(y_dist, x_dist))
        print (self.angle)

        #get mouse click
        if pygame.mouse.get_pressed()[0] and self.fired == False:
            self.fired = True
            bullet = Bullet(bullet_img, self.rect.midleft[0]+25,self.rect.midleft[1], self.angle)
            bullet_group.add(bullet)
        #reset click
        if pygame.mouse.get_pressed()[0] == False:
            self.fired = False



    def draw(self):
        self.image = self.image100

        screen.blit(self.image, self.rect)

#bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = math.radians(angle) #zmen uhol na radiany
        self.speed = 10
        #calculate h and v speed
        self.dx = math.cos(self.angle) * self.speed
        self.dy = -(math.sin(self.angle) * self.speed)

    def update(self):
        #check if bullet je mimo obrazovky
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()


        #move bullet
        self.rect.x += self.dx
        self.rect.y += self.dy

#create castle
castle = Castle(castle_image_100, SCREEN_WIDTH - 190, SCREEN_HEIGHT - 300, 2.1)

#create groups
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()


#create enemies
enemy_1 = Enemy(enemy_health[0], enemy_animations[0], 200, 650, 1)
enemy_group.add(enemy_1)

#game loop
run = True
while run:

    clock.tick(FPS)

    screen.blit(bg, (0,0))

    #draw castle
    castle.draw()
    castle.shoot()

    #draw bullet
    bullet_group.update()
    bullet_group.draw(screen)

    #draw enemies
    enemy_group.update(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update displej
    pygame.display.update()

pygame.quit()