import pygame, sys

pygame.init()
pygame.font.init()

# Põhi sätted
font = pygame.font.Font('GOTHIC.ttf', 40)  # valib fondi ja selle suuruse
timer = pygame.time.Clock()
FPS = 60
pygame.display.set_caption("Mäng")

# Ekraan
ekraan_suurus = (1620, 900)  # kui suur on aken kus mäng toimub
aken = pygame.display.set_mode(ekraan_suurus)

# Mõned värvid
must = (0, 0, 0)
valge = (255, 255, 255)
punane = (255, 0, 0)

# Peategelane
mikro = pygame.image.load('main_character.png')
mikro_suurus = (200, 200)
mikro = pygame.transform.scale(mikro, mikro_suurus)
mikro_pos = [300, 300]  # Algpositsioon ekraani keskel
mikro_speed = [0, 0]  # Speed for x and y directions

# Taust
taust = pygame.image.load('ART/background.jpg')
taust = pygame.transform.scale(taust, (3240, 900))  # Pikk taust (2x ekraan)
taust_pos = [0, 0]

# Brush
brush = pygame.Surface((10, 10))  # Brush size
brush.fill(punane)  # Color of the brush
brush_positions = []  # List to store all the brush positions drawn

# Mängu tsükkel
while True:
    # Täidame ekraani mustaga
    aken.fill(must)

    # Joonistame tausta
    aken.blit(taust, taust_pos)
    aken.blit(taust, (taust_pos[0] + 1620, taust_pos[1]))  # Taust kõrvuti

    # Kui taust liigub liiga kaugele, reset
    if taust_pos[0] <= -1620:
        taust_pos[0] = 0

    # Liigutame tausta vastupidiselt tegelase liikumisele
    taust_pos[0] -= mikro_speed[0]

    # Joonistame mikrouuni
    mikro_pos[1] += mikro_speed[1]
    aken.blit(mikro, mikro_pos)

    # Joonistame pintsliga jooned
    for pos in brush_positions:
        aken.blit(brush, pos)

    # Sõlmime sõndmused
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                mikro_speed[1] = -5
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                mikro_speed[1] = 5
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                mikro_speed[0] = -5
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                mikro_speed[0] = 5
            elif event.key == pygame.K_SPACE:  # Spacebar to start drawing a line
                # Get mouse position
                mouse_pos = pygame.mouse.get_pos()
                brush_positions.append(mouse_pos)  # Start drawing at the mouse position

        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_UP, pygame.K_w, pygame.K_DOWN, pygame.K_s]:
                mikro_speed[1] = 0
            elif event.key in [pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d]:
                mikro_speed[0] = 0

    # Uuendame ekraani
    pygame.display.flip()
    timer.tick(FPS)
