import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, health, animation_list, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.health = health
        self.animation_list = animation_list
        self.frame_index = 0
        self.action = 0 #0 - walk, 1 - action, 2 = death
        self.update_time = pygame.time.get_ticks()

        #vyberem začiatočnú fotku
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0, 0, 120, 120)
        self.rect.center = (x, y)

    def update(self, surface, target, bullet_group):

        if self.alive:

            #kontrola kolizie s nabojom
            if pygame.sprite.spritecollide(self, bullet_group, True): #naboj zmizne po kontakte s enemakom
                #zniž health enemaka
                self.health -= 25


            #kontrola, či je enemak pri hrade - bude sa hybat dokym nenastane kolizia s hradom
            if self.rect.right > target.rect.left:
                self.update_action(1)


            #pohyb enemaka
            if self.action == 0:
                #zmena pozicie rect.
                self.rect.x += self.speed+1

            #check if healht je menej ako 0
            if self.health <= 0:
                target.money += 100
                target.score += 100
                self.update_action(2)  #smrt
                self.alive = False


        self.update_animation()

        # zobrazenie fotky enemaka na obrazovke
        #pygame.draw.rect(surface, (255,255,255), self.rect, 1)
        surface.blit(self.image, (self.rect.x, self.rect.y))  # zobrazenie sprite-tu v rect. - čiže v hitboxe

    def update_animation(self):

        #define animation cooldown
        ANIMATION_COOLDOWN = 200

        #update fotky podla akcie
        self.image = self.animation_list[self.action][self.frame_index]
        #check if time has passed since last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #reset animacie
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 2:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        #skontroluje či sučasna akcia je ina ako predošla akcia
        if new_action != self.action:
            self.action = new_action
            #update animation settings
            self.frame_index = 0
            self.update_date = pygame.time.get_ticks()












