import pygame
import os

class Bullet:
    def __init__(self, x, y, speed_x, speed_y, sprite_path="Sprites/kuul.png", size=10):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed_x = speed_x
        self.speed_y = speed_y

        # Load the sprite
        if os.path.exists(sprite_path):
            self.sprite = pygame.image.load(sprite_path)
            self.sprite = pygame.transform.scale(self.sprite, (size, size))  # Scale to bullet size
        else:
            print(f"Warning: {sprite_path} not found. Using default color.")
            self.sprite = None  # Fallback if image is not found

        self.color = (255, 0, 0)  # Default color if no sprite

    def move(self):
        """Move the bullet based on its speed."""
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def render(self, screen):
        """Draw the bullet using the sprite or as a rectangle."""
        if self.sprite:
            screen.blit(self.sprite, self.rect.topleft)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

    def off_screen(self, width, height):
        """Check if the bullet goes off screen."""
        return self.rect.x < 0 or self.rect.x > width or self.rect.y < 0 or self.rect.y > height
