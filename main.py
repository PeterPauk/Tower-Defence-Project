import pygame
import math
import random
from enemy import Enemy


# zapnutie hry
pygame.init()

# okno hry
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800

# zapnutie okna hry
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defence GAME OF THE YEAR 2022 EDITION")

clock = pygame.time.Clock()
FPS = 60

# define premenne
level = 1
level_diff = 0
target_diff = 1000          #zjavenie enemaka zvysi obtiažnost levelu, dokym to nedosiahne hodnotu 1000
ENEMY_TIMER = 1000
last_enemy = pygame.time.get_ticks()
enemies_alive = 0

# load images
bg = pygame.image.load("img/back16002.png").convert_alpha()
# castle
castle_image_100 = pygame.image.load("img/castle100.png").convert_alpha()
castle_image_50 = pygame.image.load("img/castle50.png").convert_alpha()
castle_image_25 = pygame.image.load("img/castle25.png").convert_alpha()
# bullet
bullet_img = pygame.image.load("img/bullet.png").convert_alpha()
b_w = bullet_img.get_width()
b_h = bullet_img.get_height()
bullet_img = pygame.transform.scale(bullet_img, (int(b_w * 2), int(b_h * 2)))

# load enemies
enemy_animations = []
enemy_types = ["red", "blue"]
enemy_health = [75, 100]


animation_types = ["walk", "attack", "death"]
for enemy in enemy_types:
    # load animation
    animation_list = []
    for animation in animation_types:
        # reset temporary list of images
        temp_list = []
        num_of_frames = 7
        for i in range(num_of_frames):
            img = pygame.image.load(f"img/enemies/{enemy}/{animation}/{i}.png").convert_alpha()
            e_w = img.get_width()
            e_h = img.get_height()
            img = pygame.transform.scale(img, (int(e_w ), int(e_h )))
            temp_list.append(img)
        animation_list.append(temp_list)
    enemy_animations.append(animation_list)

# definuj farby
WHITE = (255, 255, 255)


# castle class
class Castle():
    def __init__(self, image100, image50, image25, x, y, scale):
        self.health = 1000
        self.max_health = self.health
        self.fired = False
        self.money = 0
        self.score = 0

        width = image100.get_width()
        height = image100.get_height()

        self.image100 = pygame.transform.scale(image100, (int(width - 50 * scale), int(height - 50 * scale)))
        self.image50 = pygame.transform.scale(image50, (int(width - 50 * scale), int(height - 50 * scale)))
        self.image25 = pygame.transform.scale(image25, (int(width - 50 * scale), int(height - 50 * scale)))
        self.rect = self.image100.get_rect()
        self.rect.x = x
        self.rect.y = y

    def shoot(self):
        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.midleft[0] + 25
        y_dist = -(pos[1] - self.rect.midleft[1])
        self.angle = math.degrees(math.atan2(y_dist, x_dist))
        # print (self.angle)

        # get mouse click
        if pygame.mouse.get_pressed()[0] and self.fired == False:
            self.fired = True
            bullet = Bullet(bullet_img, self.rect.midleft[0] + 25, self.rect.midleft[1], self.angle)
            bullet_group.add(bullet)
        # reset click
        if pygame.mouse.get_pressed()[0] == False:
            self.fired = False

    def draw(self):
        # použije sa rozny obrazok podla poctu hp
        if self.health <= 250:
            self.image = self.image25
        elif self.health <= 500:
            self.image = self.image50
        else:
            self.image = self.image100

        screen.blit(self.image, self.rect)


# bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = math.radians(angle)  # zmen uhol na radiany
        self.speed = 10
        # calculate h and v speed
        self.dx = math.cos(self.angle) * self.speed
        self.dy = -(math.sin(self.angle) * self.speed)

    def update(self):
        # check if bullet je mimo obrazovky
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

        # move bullet
        self.rect.x += self.dx
        self.rect.y += self.dy


class Crosshair():
    def __init__(self, scale):
        image = pygame.image.load("img/cross.png").convert_alpha()
        width = image.get_width()
        height = image.get_height()

        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()

        # hide mouse
        pygame.mouse.set_visible(False)

    def draw(self):
        mx, my = pygame.mouse.get_pos()
        self.rect.center = (mx, my)
        screen.blit(self.image, self.rect)


# create castle
castle = Castle(castle_image_100, castle_image_50, castle_image_25, SCREEN_WIDTH - 190, SCREEN_HEIGHT - 300, 2.1)

# create cross
crosshair = Crosshair(0.750)

# create groups
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# game loop
run = True
while run:

    clock.tick(FPS)

    screen.blit(bg, (0, 0))

    # draw castle
    castle.draw()
    castle.shoot()



    # draw bullet
    bullet_group.update()
    bullet_group.draw(screen)

    # draw enemies
    enemy_group.update(screen, castle, bullet_group)

    # draw cross
    crosshair.draw()

    # create enemies
    # check if max num if enemies has reached

    if level_diff < target_diff:
        if pygame.time.get_ticks() - last_enemy > ENEMY_TIMER:
            # časovač
            e = random.randint(0, len(enemy_types)-1)
            enemy = Enemy(enemy_health[e], enemy_animations[e], -100, 650, 1)
            enemy_group.add(enemy)
            # reset enemy timer
            last_enemy = pygame.time.get_ticks()
            # zvysenie levelu
            level_diff += enemy_health[e]
            print(level_diff)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update displej
    pygame.display.update()

pygame.quit()