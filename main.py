import pygame, sys

pygame.init()
pygame.font.init()
font = pygame.font.Font('GOTHIC.ttf', 40) #valib fondi ja selle suuruse
timer = pygame.time.Clock()
FPS = 60
pygame.display.set_caption("Mäng")

ekraan_suurus = (1620,900) # kui suur on aken kus mäng toimub
aken = pygame.display.set_mode(ekraan_suurus)

mikro = pygame.image.load('main_character.png')
mikro_suurus = (500,500)
mikro = pygame.transform.scale(mikro,mikro_suurus)
mikro_pos= (0,0)
must = (0,0,0)
while True:
    aken.fill(must)
    aken.blit(mikro, mikro_pos)
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()