import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, health, animation_list, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.health = health
        self.animation_list = animation_list
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        #vyberem začiatočnú fotku
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def update(self, surface):

        self.update_animation()

        surface.blit(self.image, self.rect)

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
            self.frame_index = 0













