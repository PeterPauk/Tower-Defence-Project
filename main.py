import pygame

#zapnutie hry
pygame.init()

#okno hry
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

#zapnutie okna hry
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))
pygame.display.set_caption("Castle")

clock = pygame.time.Clock()
FPS = 60

#load image pozadie
bg = pygame.image.load("New Piskel (1).png").convert_alpha()


#game loop
run = True
while run:

    clock.tick(FPS)

    screen.blit(bg, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()