import pygame
from object import Objekt

class Enemy(Objekt):
    def __init__(self, x, y, width, height, color=(255, 0, 0), pos=None, screen=None):
        # Initialize the parent class (Objekt)
        super().__init__(sprite=None, pos=[x, y], speed=[0, 0], width=width)
        
        # Create a surface for the enemy
        self.image = pygame.Surface((width, height))
        self.image.fill(color)  # Set initial color of the enemy
        
        # Set the rectangle for positioning
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Additional enemy-specific attributes
        self.direction = None
        self.pos = pos or [0, 0]
        
        # Reference to the screen for rendering
        self.screen = screen

    def render(self):
        self.screen.blit(self.image, self.rect.topleft)  # Draw the enemy using self.image

    def play_animation(self, direction):
        # Depending on the direction, change the animation
        if direction == 'left':
            self.image.fill((255, 0, 0))  # Red for left
        elif direction == 'right':
            self.image.fill((0, 255, 0))  # Green for right
        elif direction == 'up':
            self.image.fill((0, 0, 255))  # Blue for up
        elif direction == 'down':
            self.image.fill((255, 255, 0))  # Yellow for down
        else:
            self.image.fill((255, 0, 0))  # Default red

    def calculate_direction(self, strokes):
        if not strokes:
            return None

        start_point = strokes[0].pos
        end_point = strokes[-1].pos
        dx = end_point[0] - start_point[0]
        dy = end_point[1] - start_point[1]

        print(f"Start: {start_point}, End: {end_point}, dx: {dx}, dy: {dy}")  # Debugging

        if abs(dx) > abs(dy):  # Horizontal line
            if dx > 0:
                print("Direction: right")  # Debug
                return 'right'
            else:
                print("Direction: left")  # Debug
                return 'left'
            
        else:  # Vertical line
            if dy > 0:
                print("Direction: down")  # Debug
                return 'down'
            else:
                print("Direction: up")  # Debug
                return 'up'
