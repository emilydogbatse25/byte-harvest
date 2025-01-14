

import pygame
from constants import LAYERS, TILE_SIZE, APPLE_POS
from random import randint, choice
from sprite_loader import import_folder

class Terrain(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z

        # Collision boundaries
        shrink_x = self.rect.width * 0.2
        shrink_y = self.rect.height * 0.75
        self.hitbox = self.rect.copy().inflate(-shrink_x, -shrink_y)

class WaterTile(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['water']

    def update(self, dt):
        self.frame_index += 5 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

class WildFlower(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['main']
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)

class Tree(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, name, player_add):
        super().__init__(groups)

        # Tree setup
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['main']
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.5, -self.rect.height * 0.75)

        # Tree attributes
        self.name = name
        self.health = 5
        self.alive = True
        self.player_add = player_add  # Reference to player_add function for inventory management

        # Apples
        self.apple_surf = pygame.image.load('graphics/fruit/apple.png').convert_alpha()
        self.apple_pos = APPLE_POS.get(name, [])  # Get apple positions for this tree type
        self.apple_sprites = pygame.sprite.Group()
        self.create_fruit()

        # Sounds
        self.axe_sound = pygame.mixer.Sound('graphics/axe.mp3')

    def create_fruit(self):
        """Create apples on the tree at predefined positions."""
        if self.alive:
            for pos in self.apple_pos:
                apple_x = self.rect.left + pos[0]
                apple_y = self.rect.top + pos[1]
                Apple(
                    pos=(apple_x, apple_y),
                    surf=self.apple_surf,
                    groups=[self.apple_sprites],
                    player_add=self.player_add
                )

    def damage(self):
        """Damage the tree, and remove it if health is depleted."""
        self.health -= 1
        self.axe_sound.play()

        if self.health <= 0:
            self.alive = False
            self.kill()  # Remove the tree from all sprite groups
            for apple in self.apple_sprites:
                apple.kill()  # Remove all apples when the tree is destroyed


class Apple(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, player_add):
        super().__init__(groups)

        # Apple setup
        self.image = surf
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['fruit']
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.5, -self.rect.height * 0.5)

        # Reference to player's inventory management
        self.player_add = player_add

    def collect(self):
        """Handle apple collection by the player."""
        if self.player_add:
            self.player_add("apple")  # Add to player's inventory
        self.kill()  # Remove the apple sprite
        
        
class Fruit(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z, duration=200):
        super().__init__(groups)
        self.z = z

        # Basic setup
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

        # Animation
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

        # Fade effect
        mask_surf = pygame.mask.from_surface(self.image)
        new_surf = mask_surf.to_surface()
        new_surf.set_colorkey((0, 0, 0))
        self.image = new_surf

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.kill()

class Interaction(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups, name):
        super().__init__(groups)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)
        self.name = name


class SoilWaterTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil water']  # Ensure correct rendering layer