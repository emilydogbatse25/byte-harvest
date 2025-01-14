
import pygame
from pygame import Vector2
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, LAYERS

class CameraGroup(pygame.sprite.Group):
    def __init__(self, target_surface):
        super().__init__()
        self.display_surface = target_surface
        self.offset = Vector2()

    def custom_draw(self, player):
        """Draw sprites with camera offset, ordered by layer."""
        
        # Get the center offset
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        # Draw all sprites by layer
        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if hasattr(sprite, 'z') and sprite.z == layer:
                    # Get the offset rectangle for positioning
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    
                    # Draw the sprite
                    self.display_surface.blit(sprite.image, offset_rect)