import pygame
import math
import random
import os
from enemy import Enemy
import button


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
high_score = 0
level_diff = 0
target_diff = 1000
DIFF_MULTIPLIER = 1                     #zvysi obtiažnost o 10 percent kazdy level
game_over = False
next_level = False                        #zjavenie enemaka zvysi obtiažnost levelu, dokym to nedosiahne hodnotu 1000
ENEMY_TIMER = 1000
last_enemy = pygame.time.get_ticks()
enemies_alive = 0
tower_cost = 5000
max_towers = 4
tower_positions = [
[950, 150],
[750, 150],
[550, 150],
[350, 150],
]

#nacitanie high score
if os.path.exists("score.txt"):
    with open("score.txt", "r") as file:
        high_score = int(file.read())

# definuj farby
WHITE = (255, 255, 255)
GOLD = (229, 184, 11)
BLACK = (19, 19, 18)
RED = (255,0,0)

#definuj font
font = pygame.font.SysFont("Futura", 30)
font_60 = pygame.font.SysFont("Futura", 60)
font_25 = pygame.font.SysFont("Futura", 25)



# load images
bg = pygame.image.load("img/back16002.png").convert_alpha()
bg1 = pygame.image.load("img/castle.png").convert_alpha()

# castle
castle_image_100 = pygame.image.load("img/hrad_100.png").convert_alpha()
castle_image_50 = pygame.image.load("img/hrad_50.png").convert_alpha()
castle_image_25 = pygame.image.load("img/hrad_25.png").convert_alpha()

# tower
tower_image_100 = pygame.image.load("img/hrad_100.png").convert_alpha()
tower_image_50 = pygame.image.load("img/hrad_50.png").convert_alpha()
tower_image_25 = pygame.image.load("img/hrad_25.png").convert_alpha()



# bullet
bullet_img = pygame.image.load("img/bullet.png").convert_alpha()
b_w = bullet_img.get_width()
b_h = bullet_img.get_height()
bullet_img = pygame.transform.scale(bullet_img, (int(b_w * 2), int(b_h * 2)))

# load enemies
enemy_animations = []
enemy_types = ["machine", "bandit", "spear", "monster", "barrel"]
enemy_health = [100, 50, 75, 150, 200]
enemy_pos = [300, 620, 620, 400, 220]


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



#fotky pre tlačitka
armor_img = pygame.image.load("img/hpnew.png").convert_alpha()
repair_img = pygame.image.load("img/hamnew.png").convert_alpha()
towerb_img = pygame.image.load("img/towerb.png").convert_alpha()


#funkcia na output textu na obrazovke
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

#funkcia pre zobrazovanie udajov
def show_info():
    draw_text("Money: " + str(castle.money), font, BLACK, 10, 10)
    draw_text("Score: " + str(castle.score), font, BLACK, 180, 10)
    draw_text("High Score: " + str(high_score), font, BLACK, 360, 10)
    draw_text("Level: " + str(level), font, BLACK, 650, 10)
    draw_text("Health: " + str(castle.health) + " / " + str(castle.max_health), font, BLACK, SCREEN_WIDTH - 210, 700)
    draw_text("500 Money", font_25, BLACK, 1040, 75)
    draw_text("1000 Money", font_25, BLACK, 1170, 75)
    draw_text("+250 MAX Health", font_25, BLACK, 1010, 95)
    draw_text("+500 Health", font_25, BLACK, 1160, 95)
    draw_text("5000 Money", font_25, BLACK, 1280, 75)
    draw_text("+1 Tower", font_25, BLACK, 1290, 95)
    draw_text("4 Towers Max", font_25, BLACK, 1270, 115)

# castle class
class Castle():
    def __init__(self, image100, image50, image25, x, y, scale):
        self.health = 1000
        self.max_health = self.health
        self.fired = False
        self.money = 1055845
        self.score = 0

        width = image100.get_width()
        height = image100.get_height()

        self.image100 = pygame.transform.scale(image100, (int(width - 40 * scale), int(height - 50 * scale)))
        self.image50 = pygame.transform.scale(image50, (int(width - 40 * scale), int(height - 50 * scale)))
        self.image25 = pygame.transform.scale(image25, (int(width - 40 * scale), int(height - 50 * scale)))
        self.rect = self.image100.get_rect()
        self.rect.x = x+-20
        self.rect.y = y-300

    def shoot(self):
        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.midleft[0] + 25
        y_dist = -(pos[1] - self.rect.midleft[1])
        self.angle = math.degrees(math.atan2(y_dist, x_dist))
        # print (self.angle)

        # get mouse click
        if pygame.mouse.get_pressed()[0] and self.fired == False and pos[1]>70:
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

    def repair(self):
        if self.money >= 1000 and self.health < self.max_health:
            self.health += 500
            self.money -= 1000
            if self.health > self.max_health:
                self.health = self.max_health

    def armor(self):
        if self.money >= 500:
            self.max_health += 250
            self.money -= 500

#tower class
class Tower(pygame.sprite.Sprite):
    def __init__(self, image100, image50, image25, x, y, scale):
        pygame.sprite.Sprite.__init__(self)

        self.target_found = False
        self.angle = 0
        self.last_shot = pygame.time.get_ticks()

        width = image100.get_width()
        height = image100.get_height()

        self.image100 = pygame.transform.scale(image100, (int(width - 40 * scale), int(height - 50 * scale)))
        self.image50 = pygame.transform.scale(image50, (int(width - 40 * scale), int(height - 50 * scale)))
        self.image25 = pygame.transform.scale(image25, (int(width - 40 * scale), int(height - 50 * scale)))
        self.image = self.image100
        self.rect = self.image100.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, enemy_group):
        self.target_found = False
        target_x = 0
        target_y = 0
        for e in enemy_group:
            if e.alive:
                target_x, target_y = e.rect.midbottom
                self.target_found = True
                break

        if self.target_found:
            x_dist = target_x- self.rect.midleft[0] + 25
            y_dist = -(target_y- self.rect.midleft[1])
            self.angle = math.degrees(math.atan2(y_dist, x_dist))

            shot_cooldown = 800
            #strielanie strel
            if pygame.time.get_ticks() - self.last_shot > shot_cooldown:
                self.last_shot = pygame.time.get_ticks()
                bullet = Bullet(bullet_img, self.rect.midleft[0] + 25, self.rect.midleft[1], self.angle)
                bullet_group.add(bullet)

        if castle.health <= 250:
            self.image = self.image25
        elif castle.health <= 500:
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
        image = pygame.image.load("img/cross_2.png").convert_alpha()
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

#vytvorenie tlacidiel
repair_button = button.Button(1180, 10, repair_img)
armor_button = button.Button(1050, 10, armor_img)
tower_button = button.Button(1290, 10, towerb_img)

# create groups
tower_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# game loop
run = True
while run:

    clock.tick(FPS)

    if game_over == False:
        screen.blit(bg, (0, 0))

        # draw castle
        castle.draw()
        castle.shoot()

        #draw towers
        tower_group.draw(screen)
        tower_group.update(enemy_group)

        # draw bullet
        bullet_group.update()
        bullet_group.draw(screen)



        # draw enemies
        enemy_group.update(screen, castle, bullet_group)


        # tlacitka
        if repair_button.draw(screen):
            castle.repair()


        if armor_button.draw(screen):
            castle.armor()

        if tower_button.draw(screen):
            if castle.money >= tower_cost and len(tower_group) < max_towers:
                tower = Tower(
                    tower_image_100,
                    tower_image_50,
                    tower_image_25,
                    tower_positions[len(tower_group)][0],
                    tower_positions[len(tower_group)][1],
                    2.5
                    )
                tower_group.add(tower)

                castle.money -= tower_cost


        # draw cross
        crosshair.draw()

        #detaily
        show_info()

        # create enemies
        # check if max num if enemies has reached

        if level_diff < target_diff:
            if pygame.time.get_ticks() - last_enemy > ENEMY_TIMER:
                # časovač
                e = random.randint(0, len(enemy_types)-1)

                enemy = Enemy(enemy_health[e], enemy_animations[e], -150, enemy_pos[e], 1)

                enemy_group.add(enemy)
                # reset enemy timer
                last_enemy = pygame.time.get_ticks()
                # zvysenie levelu
                level_diff += enemy_health[e]


        if level_diff >= target_diff:
            #check how many alive
            enemies_alive = 0
            for e in enemy_group:
                if e.alive == True:
                    enemies_alive += 1

            if enemies_alive == 0 and next_level == False:
                next_level = True
                level_reset_time = pygame.time.get_ticks()

        #next level
        if next_level == True:
            draw_text("LEVEL COMPLETE!", font_60, WHITE, 500, 350)
            #aktualizovanie high score
            if castle.score > high_score:
                high_score = castle.score
                with open("score.txt", "w") as file:
                    file.write(str(high_score))


            if pygame.time.get_ticks() - level_reset_time > 2000:
                next_level = False
                level += 1
                last_enemy = pygame.time.get_ticks()
                target_diff *= DIFF_MULTIPLIER
                level_diff = 0
                FPS += 15
                enemy_group.empty()

        #check game over
        if castle.health <= 0:
            game_over = True

    else:
        draw_text("GAME OVER!", font_60, RED, 500, 350)
        draw_text("Press A to play again!", font_60, RED, 460, 420)
        pygame.mouse.set_visible(True)
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            game_over = False
            level = 1
            target_diff = 1000
            level_diff = 0
            last_enemy = pygame.time.get_ticks()
            enemy_group.empty()
            tower_group.empty()
            castle.score = 0
            castle.health = 1000
            castle.max_health = castle.health
            castle.money = 0
            pygame.mouse.set_visible(False)



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update displej
    pygame.display.update()

pygame.quit()