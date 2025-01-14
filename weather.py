import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, LAYERS
from support import import_folder
from sprites import Terrain
from random import randint, choice


class Sky:
    def __init__(self, farm_screen):
        self.display_surface = farm_screen
        self.full_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.start_color = [255, 255, 255]  # Start with a bright sky
        self.end_color = (38, 101, 189)  # Night sky color
        self.day = True  # Start with day mode

    def display(self, dt):
        """Gradually change the sky color for a day-night transition."""
        for index, value in enumerate(self.end_color):
            if self.day and self.start_color[index] > value:
                # Transition from day to night
                self.start_color[index] -= 2 * dt
            elif not self.day and self.start_color[index] < 255:
                # Transition from night to day
                self.start_color[index] += 2 * dt

        # Fill the screen with the transitioning color
        self.full_surf.fill(self.start_color)
        self.display_surface.blit(self.full_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)


class Drop(Terrain):
    def __init__(self, surf, pos, moving, groups, z):
        super().__init__(pos, surf, groups, z)
        self.lifetime = randint(400, 500)  # Lifetime in milliseconds
        self.start_time = pygame.time.get_ticks()

        self.moving = moving
        if self.moving:
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.direction = pygame.math.Vector2(-1, 4)  # Slight horizontal drift, downward fall
            self.speed = randint(100, 150)  # Speed for snowflakes

    def update(self, dt):
        """Update the position and lifetime of the drop."""
        if self.moving:
            # Move the drop based on direction and speed
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        # Remove the drop when its lifetime expires
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()


class Snow:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.snowflakes = import_folder("graphics/snow/flakes/")  # Load snowflake graphics
        self.ground_w, self.ground_h = SCREEN_WIDTH, SCREEN_HEIGHT  # Full screen dimensions

    def create_flake(self):
        """Generate a snowflake at a random position."""
        Drop(
            surf=choice(self.snowflakes),  # Random snowflake image
            pos=(randint(0, self.ground_w), randint(0, self.ground_h)),  # Random position
            moving=True,
            groups=self.all_sprites,
            z=LAYERS["main"],
        )

    def update(self):
        """Continuously create snowflakes to simulate snowfall."""
        for _ in range(5):  # Adjust number of snowflakes per frame for density
            self.create_flake()
