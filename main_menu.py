import pygame
import sys

# Mõned värvid
must = (0, 0, 0)
valge = (255, 255, 255)
roheline = (0, 255, 0)
punane = (255, 0, 0)
sinine = (0, 0, 255)



def main_menu(screen):
    font = pygame.font.Font(None, 74)
    menu_options = ["Alusta Mängu", "Välju"]
    selected_index = 0

    def render_menu():
        screen.fill(valge)
        for i, option in enumerate(menu_options):
            color = sinine if i == selected_index else must
            text = font.render(option, True, color)
            text_rect = text.get_rect(center=(screen.get_width() // 2, 200 + i * 100))
            screen.blit(text, text_rect)
        pygame.display.flip()

    def handle_input():
        nonlocal selected_index
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    return selected_index
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for i, option in enumerate(menu_options):
                        text_rect = font.render(option, True, valge).get_rect(center=(screen.get_width() // 2, 200 + i * 100))
                        if text_rect.collidepoint(mouse_x, mouse_y):
                            return i
        return None

    while True:
        action = handle_input()
        if action is not None:
            if action == 0:  # Alusta Mängu
                return "start_game"
            elif action == 1:  # Välju
                pygame.quit()
                sys.exit()
        render_menu()
