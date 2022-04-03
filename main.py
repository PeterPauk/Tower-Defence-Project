import pygame

#zapnutie hry
pygame.init()

#okno hry
SCREEN_WIDTH = 832
SCREEN_HEIGHT = 800

#zapnutie okna hry
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))
pygame.display.set_caption("Castle")

clock = pygame.time.Clock()
FPS = 60

#load images
bg = pygame.image.load("background.png").convert_alpha()
#castle
castle_image_100 = pygame.image.load("castle.png").convert_alpha()

#castle class
class Castle():
    def __init__(self, image100, x, y, scale):
        self.health = 1000
        self.max_health = self.health

        width = image100.get_width()
        height = image100.get_height()

        self.image100 = pygame.transform.scale(image100, (int(width * scale), int(height * scale)))
        self.rect = self.image100.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        self.image = self.image100

        screen.blit(self.image, self.rect)




#create castle
castle = Castle(castle_image_100, SCREEN_WIDTH - 190, SCREEN_HEIGHT - 300, 2.1)



#game loop
run = True
while run:

    clock.tick(FPS)

    screen.blit(bg, (0,0))

    #draw castle
    castle.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update displej
    pygame.display.update()

pygame.quit()