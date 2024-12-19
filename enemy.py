import random
import pygame
from object import Objekt
from bullets import Bullet

FPS = 60

class Enemy(Objekt):
    def __init__(self, x, y, width, height, color=(255, 0, 0), pos=None, *, screen=None):
        super().__init__(sprite="man_side.png", pos=[x, y], speed=[0, 0], width=width)
        self.rect = self.sprite.get_rect()
        self.rect.topleft = (x, y)
        self.color = color
        self.screen = screen
        self.shoot_timer = 0
        self.bullets = []
        self.walk_change = 0
        self.current_action = "walk"
        self.original_speed = self._generate_random_speed()  # Random initial speed
        self.speed = self.original_speed[:]
        self.dead = False
        self.death_timer = 0

    def _generate_random_speed(self):
        """Generate a random initial speed for the enemy."""
        speed_x = random.choice([-2, -1, 1, 2])  # Random horizontal speed
        speed_y = random.choice([-2, -1, 1, 2])  # Random vertical speed
        return [speed_x, speed_y]

    def update(self, player_pos, screen_width, screen_height):
        """Update enemy logic, movement, and animations."""
        if not self.dead:  # Skip updates if the enemy is dead
            if self.current_action == "walk":
                self.rect.x += self.speed[0]
                self.rect.y += self.speed[1]

                # Reverse direction if hitting screen edges
                if self.rect.left <= 0 or self.rect.right >= screen_width:
                    self.speed[0] *= -1
                if self.rect.top <= 0 or self.rect.bottom >= screen_height:
                    self.speed[1] *= -1

                # Slight random changes to the speed to add variation
                if random.random() < 0.05:  # 5% chance to change speed
                    self.speed[0] += random.choice([-1, 1])
                    self.speed[1] += random.choice([-1, 1])

                # Clamp speeds to a maximum
                self.speed[0] = max(-3, min(self.speed[0], 3))
                self.speed[1] = max(-3, min(self.speed[1], 3))

            # Handle animations
            self.handle_animation()

            # Shooting logic
            self.shoot_timer += 1
            if self.shoot_timer >= 120:
                self.shoot(player_pos)
                self.shoot_timer = 0
        else:
            self.death_timer += 1
            if self.death_timer >= FPS * 1:  # 1 second
                return True  # Mark for removal
        return False

    def handle_animation(self):
        """Update the enemy's animation based on its action."""
        if self.dead:
            self.change_sprite("man_death.png")  # Death animation frame
        elif self.current_action == "walk" and abs(self.speed[0]) > 0:
            self.walk_change += 1
            if self.walk_change <= 10:
                self.change_sprite("man_side.png")
            elif self.walk_change <= 20:
                self.change_sprite("man_side2.png")
            if self.walk_change > 20:
                self.walk_change = 0
        elif self.current_action == "shoot":
            self.change_sprite("man_shoot.png")

    def shoot(self, player_pos):
        """Shoot a bullet toward the player's position."""
        if self.dead:
            return
        self.speed = [0, 0]
        self.current_action = "shoot"

        bullet_speed = 11
        dx = player_pos[0] - self.rect.centerx
        dy = player_pos[1] - self.rect.centery
        distance = max(1, (dx**2 + dy**2) ** 0.5)
        speed_x = (dx / distance) * bullet_speed
        speed_y = (dy / distance) * bullet_speed
        new_bullet = Bullet(self.rect.centerx, self.rect.centery, speed_x, speed_y)
        self.bullets.append(new_bullet)

        pygame.time.set_timer(pygame.USEREVENT, 300)

    def handle_shoot_event(self):
        """Resume movement after shooting animation."""
        if not self.dead:
            self.speed = self.original_speed[:]
            self.current_action = "walk"

    def render(self):
        """Draw the enemy and its bullets."""
        if self.dead:
            pygame.draw.rect(self.screen, self.color, self.rect)
        else:
            self.screen.blit(self.sprite, self.rect.topleft)
            for bullet in self.bullets:
                bullet.render(self.screen)

    def play_animation(self, direction):
        """Change the enemy's appearance based on the cutting direction."""
        if direction == 'left':
            self.color = (255, 0, 0)  # Red for left
        elif direction == 'right':
            self.color = (0, 255, 0)  # Green for right
        elif direction == 'up':
            self.color = (0, 0, 255)  # Blue for up
        elif direction == 'down':
            self.color = (255, 255, 0)  # Yellow for down
        self.dead = True  # Mark the enemy as dead

    def calculate_direction(self, strokes):
        """Calculate the direction of the line drawn by the pencil."""
        if not strokes:
            return None

        start_point = strokes[0].pos
        end_point = strokes[-1].pos
        dx = end_point[0] - start_point[0]
        dy = end_point[1] - start_point[1]

        if abs(dx) > abs(dy):  # Horizontal line
            return 'right' if dx > 0 else 'left'
        else:  # Vertical line
            return 'down' if dy > 0 else 'up'
