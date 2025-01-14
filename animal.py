import pygame
from random import randint
from constants import LAYERS, TILE_SIZE

class Animal(pygame.sprite.Sprite):
    def __init__(self, animal_type, start_pos, groups, collision_sprites):
        super().__init__(groups)
        self.collision_sprites = collision_sprites
        self.animal_type = animal_type

        # Load animal image
        try:
            self.image = pygame.image.load(f'graphics/assets/{animal_type}.png').convert_alpha()
            # Optionally scale the image if necessary
            self.image = pygame.transform.scale(self.image, (64, 64))  # Scale to 64x64 pixels
        except FileNotFoundError:
            print(f"No image found for {animal_type} at 'graphics/assets/{animal_type}.png', using placeholder")
            self.image = pygame.Surface((64, 64))
            self.image.fill('yellow')

        self.rect = self.image.get_rect(topleft=start_pos)
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # Set the rendering layer (z-value)
        self.z = LAYERS['main']  # Ensure animals are drawn above ground elements

        # Movement attributes
        self.direction = pygame.math.Vector2()
        self.speed = 20  # Adjust speed as needed
        self.timer = 0
        self.move_time = 2000  # Move every 2 seconds

    def update(self, dt):
        self.timer += dt * 1000  # Convert dt to milliseconds
        if self.timer >= self.move_time:
            self.timer = 0
            # Random movement direction
            self.direction.x = randint(-1, 1)
            self.direction.y = randint(-1, 1)

        # Move animal
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

        # Handle collisions
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                self.pos -= self.direction * self.speed * dt
                self.rect.topleft = (int(self.pos.x), int(self.pos.y))
                break  # Exit the loop after collision is handled
