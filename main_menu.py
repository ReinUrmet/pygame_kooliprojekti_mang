import pygame
import sys

def main_menu(screen):
    """Main menu function."""
    # Colors and font
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    HIGHLIGHT = (255, 100, 100)
    font = pygame.font.Font(None, 74)

    # Menu options
    menu_options = ["Start Game", "Quit"]
    selected_index = 0

    def render_menu():
        """Render menu options."""
        screen.fill(BLACK)
        for i, option in enumerate(menu_options):
            color = HIGHLIGHT if i == selected_index else WHITE
            text = font.render(option, True, color)
            text_rect = text.get_rect(center=(screen.get_width() // 2, 200 + i * 100))
            screen.blit(text, text_rect)
        pygame.display.flip()

    def handle_input():
        """Handle input for the menu."""
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
        return None

    # Main menu loop
    while True:
        action = handle_input()
        if action is not None:
            if action == 0:  # Start Game
                return "start_game"
            elif action == 1:  # Quit
                pygame.quit()
                sys.exit()
        render_menu()
