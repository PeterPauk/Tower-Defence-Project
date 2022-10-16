import pygame
import math
import random
import os
from enemy import Enemy
import button
import winsound


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

# zakladne premenne
level = 1
high_score = 0
level_diff = 0
target_diff = 1000
DIFF_MULTIPLIER = 1.1                    #zvysi obtiažnost o 10 percent kazdy level
game_over = False
next_level = False                        #zjavenie enemaka zvysi obtiažnost levelu, dokym to nedosiahne hodnotu 1000
ENEMY_TIMER = 1000
last_enemy = pygame.time.get_ticks()
enemies_alive = 0
tower_cost = 2000
max_towers = 4
tower_positions = [
[950, 150],
[750, 150],
[550, 150],
[350, 150],
]
upgrade = 0
nothing = 0
bodiky = 0  #ked kliknes na fire button, dostanes bodiky. Toto mam na to, aby sa mi ukazovali dalsie buttony "power upov"" napriek nizsej upgrade hodnote

# definuj farby
WHITE = (255, 255, 255)
GOLD = (229, 184, 11)
BLACK = (19, 19, 18)
RED = (255,0,0)

#definuj font
font = pygame.font.SysFont("Futura", 30)
font_60 = pygame.font.SysFont("Futura", 60)
font_25 = pygame.font.SysFont("Futura", 25)



# načitanie fotiek
bg = pygame.image.load("img/bg_new.png").convert_alpha()
bg_eve = pygame.image.load("img/bg_eve_new.png").convert_alpha()
bg_night = pygame.image.load("img/bg_night_new.png").convert_alpha()

# castle
castle_image_300 = pygame.image.load("img/hrad_300.png").convert_alpha()
castle_image_200 = pygame.image.load("img/hrad_200.png").convert_alpha()
castle_image_100 = pygame.image.load("img/hrad_100.png").convert_alpha()
castle_image_50 = pygame.image.load("img/hrad_50.png").convert_alpha()
castle_image_25 = pygame.image.load("img/hrad_25.png").convert_alpha()

# tower
tower_image_300 = pygame.image.load("img/hrad_300.png").convert_alpha()
tower_image_200 = pygame.image.load("img/hrad_200.png").convert_alpha()
tower_image_100 = pygame.image.load("img/hrad_100.png").convert_alpha()
tower_image_50 = pygame.image.load("img/hrad_50.png").convert_alpha()
tower_image_25 = pygame.image.load("img/hrad_25.png").convert_alpha()



# bullet
bullet_img = pygame.image.load("img/bullet.png").convert_alpha()
b_w = bullet_img.get_width()
b_h = bullet_img.get_height()
bullet_img = pygame.transform.scale(bullet_img, (int(b_w * 2), int(b_h * 2)))
fire_img = pygame.image.load("img/fire.png").convert_alpha()
unknown_img = pygame.image.load("img/unknown.png").convert_alpha()
cluster_img = pygame.image.load("img/cluster.png").convert_alpha()
#cluster_img = pygame.transform.scale(cluster_img, (int(b_w * 5), int(b_h * 5)))
ice_img = pygame.image.load("img/ice.png").convert_alpha()
buck_img = pygame.image.load("img/buck.png").convert_alpha()
on_img = pygame.image.load("img/on.png").convert_alpha()

# načitanie enemakov
enemy_animations = []
enemy_types = ["machine", "bandit", "spear", "monster", "barrel"]
enemy_health = [100, 50, 75, 150, 200]
enemy_pos = [300, 620, 620, 400, 220]


animation_types = ["walk", "attack", "death"]
for enemy in enemy_types:
    # načitanie animacii
    animation_list = []
    for animation in animation_types:
        # zresetuje dočasny list animacii
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
    if level < 7:
        draw_text("Money: " + str(castle.money), font, BLACK, 10, 10)
        draw_text("Score: " + str(castle.score), font, BLACK, 180, 10)
        draw_text("Level: " + str(level), font, BLACK, 650, 10)
        draw_text("Health: " + str(castle.health) + " / " + str(castle.max_health), font, BLACK, SCREEN_WIDTH - 210, 700)
        draw_text("500 Money", font_25, BLACK, 1040, 75)
        draw_text("1000 Money", font_25, BLACK, 1170, 75)
        draw_text("+250 MAX Health", font_25, BLACK, 1010, 95)
        draw_text("+500 Health", font_25, BLACK, 1160, 95)
        draw_text("2000 Money", font_25, BLACK, 1280, 75)

        draw_text("1000 Money", font_25, BLACK, 110, 95)
        draw_text("Fireballs", font_25, BLACK, 110, 75)

        draw_text("Cluster Ammo", font_25, BLACK, 290, 75)
        draw_text("2000 Money", font_25, BLACK, 290, 95)

        draw_text("Iceballs", font_25, BLACK, 495, 75)
        draw_text("3000 Money", font_25, BLACK, 495, 95)

        draw_text("Buckshot Ammo", font_25, BLACK, 670, 75)
        draw_text("4000 Money", font_25, BLACK, 670, 95)

        draw_text("+1 Tower", font_25, BLACK, 1290, 95)
        draw_text("4 Towers Max", font_25, BLACK, 1270, 115)

    else:
        draw_text("Money: " + str(castle.money), font,WHITE, 10, 10)
        draw_text("Score: " + str(castle.score), font, WHITE, 180, 10)
        draw_text("Level: " + str(level), font, WHITE, 650, 10)
        draw_text("Health: " + str(castle.health) + " / " + str(castle.max_health), font, BLACK, SCREEN_WIDTH - 210, 700)
        draw_text("500 Money", font_25, WHITE, 1040, 75)
        draw_text("1000 Money", font_25, WHITE, 1170, 75)
        draw_text("+250 MAX Health", font_25, WHITE, 1010, 95)
        draw_text("+500 Health", font_25, WHITE, 1160, 95)
        draw_text("2000 Money", font_25, WHITE, 1280, 75)
        draw_text("+1 Tower", font_25, WHITE, 1290, 95)
        draw_text("4 Towers Max", font_25, WHITE, 1270, 115)

        draw_text("1000 Money", font_25, WHITE, 110, 95)
        draw_text("Fireballs", font_25, WHITE, 110, 75)

        draw_text("Cluster Ammo", font_25, WHITE, 290, 75)
        draw_text("2000 Money", font_25, WHITE, 290, 95)

        draw_text("Iceballs", font_25, WHITE, 495, 75)
        draw_text("3000 Money", font_25, WHITE, 495, 95)

        draw_text("Buckshot Ammo", font_25, WHITE, 670, 75)
        draw_text("4000 Money", font_25, WHITE, 670, 95)



# castle class
class Castle():
    def __init__(self, image300, image200, image100, image50, image25, x, y, scale):
        self.health = 1000
        self.max_health = self.health
        self.fired = False
        self.money = 0
        self.score = 0


        width = image100.get_width()
        height = image100.get_height()

        self.image300 = pygame.transform.scale(image300, (int(width - 40 * scale), int(height - 50 * scale)))
        self.image200 = pygame.transform.scale(image200, (int(width - 40 * scale), int(height - 50 * scale)))
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
        #print (self.angle)

        # klikanie myšky - strielanie
        if pygame.mouse.get_pressed()[0] and self.fired == False and pos[1]>120:
            self.fired = True
            if upgrade < 1:
                bullet = Bullet(bullet_img, self.rect.midleft[0] + 25, self.rect.midleft[1], self.angle)
                bullet_group.add(bullet)
                #winsound.PlaySound("sounds/shoot.wav", winsound.SND_ASYNC)
            if upgrade == 1:
                fire = Fire(fire_img, self.rect.midleft[0] + 25, self.rect.midleft[1], self.angle, 10)
                fire_group.add(fire)
                #winsound.PlaySound("sounds/shoot.wav", winsound.SND_ASYNC)
            if upgrade == 2:
                bullet = Bullet(bullet_img, self.rect.midleft[0] + 25, self.rect.midleft[1], self.angle)
                bullet_group.add(bullet)
                bullet1 = Bullet(bullet_img, self.rect.midleft[0] + 25, self.rect.midleft[1], self.angle + 25)
                bullet_group.add(bullet1)
                bullet2 = Bullet(bullet_img, self.rect.midleft[0] + 25, self.rect.midleft[1], self.angle -25)
                bullet_group.add(bullet2)
            if upgrade == 3:
                ice = Ice(ice_img, self.rect.midleft[0] + 25, self.rect.midleft[1], self.angle, 10)
                ice_group.add(ice)
               # winsound.PlaySound("sounds/shoot.wav", winsound.SND_ASYNC)
            if upgrade == 4:
                bullet = Bullet(bullet_img, self.rect.midleft[0] + 25, self.rect.midleft[1], self.angle)
                bullet_group.add(bullet)
                bullet1 = Bullet(bullet_img, self.rect.midleft[0] + 25, self.rect.midleft[1], self.angle + 15)
                bullet_group.add(bullet1)
                bullet2 = Bullet(bullet_img, self.rect.midleft[0] + 25, self.rect.midleft[1], self.angle - 15)
                bullet_group.add(bullet2)
                bullet3 = Bullet(bullet_img, self.rect.midleft[0] + 25, self.rect.midleft[1], self.angle + 30)
                bullet_group.add(bullet3)
                bullet4 = Bullet(bullet_img, self.rect.midleft[0] + 25, self.rect.midleft[1], self.angle - 30)
                bullet_group.add(bullet4)
                bullet5 = Bullet(bullet_img, self.rect.midleft[0] + 25, self.rect.midleft[1], self.angle + 45)
                bullet_group.add(bullet5)
                bullet6 = Bullet(bullet_img, self.rect.midleft[0] + 25, self.rect.midleft[1], self.angle - 45)
                bullet_group.add(bullet6)


        # reset click
        if pygame.mouse.get_pressed()[0] == False:
            self.fired = False

    def draw(self):
        # použije sa rozny obrazok podla poctu hp
        if self.health <= 250:
            self.image = self.image25
        elif self.health <= 500:
            self.image = self.image50
        elif self.health <= 1000 and self.health < 2000:
            self.image = self.image100
        elif self.health >= 2000 and self.health < 3000:
            self.image = self.image200
        elif self.health >= 3000:
            self.image = self.image300

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
    def __init__(self, image300, image200, image100, image50, image25, x, y, scale):
        pygame.sprite.Sprite.__init__(self)

        self.target_found = False
        self.angle = 0
        self.last_shot = pygame.time.get_ticks()


        width = image100.get_width()
        height = image100.get_height()

        self.image300 = pygame.transform.scale(image300, (int(width - 40 * scale), int(height - 50 * scale)))
        self.image200 = pygame.transform.scale(image200, (int(width - 40 * scale), int(height - 50 * scale)))
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
                if upgrade == 0:
                    bullet = Bullet(bullet_img, self.rect.midleft[0] + 25, self.rect.midleft[1], self.angle)
                    bullet_group.add(bullet)
                if upgrade == 1:
                    fire = Fire(fire_img, self.rect.midleft[0] + 25, self.rect.midleft[1], self.angle, 10)
                    fire_group.add(fire)
                if upgrade == 2:
                    bullet = Bullet(bullet_img, self.rect.midleft[0] + 25, self.rect.midleft[1], self.angle)
                    bullet_group.add(bullet)
                    bullet1 = Bullet(bullet_img, self.rect.midleft[0] + 25, self.rect.midleft[1], self.angle + 25)
                    bullet_group.add(bullet1)
                    bullet2 = Bullet(bullet_img, self.rect.midleft[0] + 25, self.rect.midleft[1], self.angle - 25)
                    bullet_group.add(bullet2)
                if upgrade ==3:
                    ice = Ice(ice_img, self.rect.midleft[0] + 25, self.rect.midleft[1], self.angle, 10)
                    ice_group.add(ice)
                if upgrade == 4:
                    bullet = Bullet(bullet_img, self.rect.midleft[0] + 25, self.rect.midleft[1], self.angle)
                    bullet_group.add(bullet)
                    bullet1 = Bullet(bullet_img, self.rect.midleft[0] + 25, self.rect.midleft[1], self.angle + 15)
                    bullet_group.add(bullet1)
                    bullet2 = Bullet(bullet_img, self.rect.midleft[0] + 25, self.rect.midleft[1], self.angle - 15)
                    bullet_group.add(bullet2)
                    bullet3 = Bullet(bullet_img, self.rect.midleft[0] + 25, self.rect.midleft[1], self.angle + 30)
                    bullet_group.add(bullet3)
                    bullet4 = Bullet(bullet_img, self.rect.midleft[0] + 25, self.rect.midleft[1], self.angle - 30)
                    bullet_group.add(bullet4)
                    bullet5 = Bullet(bullet_img, self.rect.midleft[0] + 25, self.rect.midleft[1], self.angle + 45)
                    bullet_group.add(bullet5)
                    bullet6 = Bullet(bullet_img, self.rect.midleft[0] + 25, self.rect.midleft[1], self.angle - 45)
                    bullet_group.add(bullet6)


        if castle.health <= 250:
            self.image = self.image25
        elif castle.health <= 500:
            self.image = self.image50
        elif castle.health <= 1000 and castle.health < 2000:
            self.image = self.image100
        elif castle.health >= 2000 and castle.health < 3000:
            self.image = self.image200
        elif castle.health >= 3000:
            self.image = self.image300

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
        # horizontalna a vertikalna rychlost
        self.dx = math.cos(self.angle) * self.speed
        self.dy = -(math.sin(self.angle) * self.speed)

    def update(self):
        # skontroluje, či je bullet mimo obrazovky
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

        # pohyb
        self.rect.x += self.dx
        self.rect.y += self.dy

class Fire(Bullet):
    def __init__(self, image, x, y, angle, knockback):
        super().__init__(image, x, y, angle)
        self.knockback = knockback

class Ice(Bullet):
    def __init__(self, image, x, y, angle, knockback):
        super().__init__(image, x, y, angle)
        self.knockback = knockback

class Crosshair():
    def __init__(self, scale):
        image = pygame.image.load("img/cross_2.png").convert_alpha()
        width = image.get_width()
        height = image.get_height()

        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()

        # schovanie kurzora
        pygame.mouse.set_visible(False)

    def draw(self):
        mx, my = pygame.mouse.get_pos()
        self.rect.center = (mx, my)
        screen.blit(self.image, self.rect)


# create castle
castle = Castle(castle_image_300, castle_image_200, castle_image_100, castle_image_50, castle_image_25, SCREEN_WIDTH - 190, SCREEN_HEIGHT - 300, 2.1)

# create cross
crosshair = Crosshair(0.750)

#vytvorenie tlacidiel
repair_button = button.Button(1180, 10, repair_img)
armor_button = button.Button(1050, 10, armor_img)
tower_button = button.Button(1290, 10, towerb_img)
fire_button = button.Button(40, 45, fire_img)
unknown_button = button.Button(220, 45, unknown_img)
unknown1_button = button.Button(400, 45, unknown_img)
cluster_button = button.Button(220, 45, cluster_img)
ice_button = button.Button(425, 35, ice_img)
buck_button = button.Button(600, 35, buck_img)

on_button = button.Button(52, 130, on_img)
on_button1 = button.Button(247, 130, on_img)
on_button2 = button.Button(440, 130, on_img)
on_button3= button.Button(615, 130, on_img)

# vytvorenie groups
tower_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
fire_group = pygame.sprite.Group()
ice_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# game loop
run = True
while run:

    clock.tick(FPS)

    if game_over == False:
        if level <= 3:
            screen.blit(bg, (0, 0))
        elif level <7:
            screen.blit(bg_eve, (0, 0))
        elif level>=7:
            screen.blit(bg_night, (0,0))


        # draw castle
        castle.draw()
        castle.shoot()

        #draw towers
        tower_group.draw(screen)
        tower_group.update(enemy_group)

        # draw bullet
        bullet_group.update()
        bullet_group.draw(screen)

        fire_group.update()
        fire_group.draw(screen)

        ice_group.update()
        ice_group.draw(screen)

        # draw enemaci
        enemy_group.update(screen, castle, bullet_group, fire_group, ice_group)


        # tlacitka
        if repair_button.draw(screen):
            castle.repair()


        if armor_button.draw(screen):
            castle.armor()

        if tower_button.draw(screen):
            if castle.money >= tower_cost and len(tower_group) < max_towers:
                tower = Tower(
                    tower_image_300,
                    tower_image_200,
                    tower_image_100,
                    tower_image_50,
                    tower_image_25,
                    tower_positions[len(tower_group)][0],
                    tower_positions[len(tower_group)][1],
                    2.5
                    )
                tower_group.add(tower)

                castle.money -= tower_cost

        if fire_button.draw(screen):
            if castle.money >= 1000:
                castle.money -= 1000
                upgrade = 1

        #prva faza power - upov


        if cluster_button.draw(screen):
            if castle.money >= 2000:
                upgrade = 2
                castle.money -= 2000


        #druha faza


        if ice_button.draw(screen):
            if castle.money >= 3000:
                upgrade = 3
                castle.money -= 3000

        if buck_button.draw(screen):
            if castle.money >= 4000:
                upgrade = 4
                castle.money -= 4000

        if upgrade == 1:
            if on_button.draw(screen):
                nothing += 10

        if upgrade == 2:
            if on_button1.draw(screen):
                nothing += 10

        if upgrade == 3:
            if on_button2.draw(screen):
                nothing += 10

        if upgrade == 4:
            if on_button3.draw(screen):
                nothing += 10



        # draw cross
        crosshair.draw()

        #detaily
        show_info()

        # toto bude kontrolovat, či sa dosiahol max počet enemakov

        if level_diff < target_diff:
            if pygame.time.get_ticks() - last_enemy > ENEMY_TIMER:
                # časovač
                e = random.randint(0, len(enemy_types)-1)

                enemy = Enemy(enemy_health[e], enemy_animations[e], -150, enemy_pos[e], 1)

                enemy_group.add(enemy)
                # zresetuje časovač
                last_enemy = pygame.time.get_ticks()
                # zvysenie levelu
                level_diff += enemy_health[e]


        if level_diff >= target_diff:
            #skontoluje kolko enemakov stale žije
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



            if pygame.time.get_ticks() - level_reset_time > 2000:
                next_level = False
                level += 1
                last_enemy = pygame.time.get_ticks()
                target_diff *= DIFF_MULTIPLIER
                level_diff = 0
                castle.money += 1000
                FPS += 15
                enemy_group.empty()

        kluc = pygame.key.get_pressed()
        if kluc[pygame.K_c]:
            castle.money += 1000

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
            upgrade = 0
            FPS = 60
            pygame.mouse.set_visible(False)



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update displej
    pygame.display.update()

pygame.quit()