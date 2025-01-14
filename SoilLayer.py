import pygame
from constants import *
from support import import_folder
from random import choice
from sprites import SoilWaterTile  # Import the new class
from SoilTile import SoilTile
from Plant import Plant

class SoilLayer:
    def __init__(self, all_sprites, collision_sprites):
        # Sprite groups
        self.all_sprites = all_sprites
        self.collision_sprites = collision_sprites
        self.soil_sprites = pygame.sprite.Group()
        self.water_sprites = pygame.sprite.Group()
        self.plant_sprites = pygame.sprite.Group()

        # Graphics
        self.soil_surfs = import_folder('graphics/soil')
        self.water_surfs = import_folder('graphics/soil_water')

        # Sound
        try:
            self.hoe_sound = pygame.mixer.Sound('graphics/hoe.wav')
            self.hoe_sound.set_volume(0.1)
        except:
            print("Hoe sound not found")

        self.create_soil_grid()
        self.create_hit_rects()

        # Weather
        self.raining = False
        self.water_all()

    def create_soil_grid(self):
        ground = pygame.image.load("graphics/world/ground.png")
        h_tiles = ground.get_width() // TILE_SIZE
        v_tiles = ground.get_height() // TILE_SIZE

        self.grid = []
        for row in range(v_tiles):
            self.grid.append([[] for col in range(h_tiles)])

    def create_hit_rects(self):
        """Create rectangles for soil collision detection."""
        self.hit_rects = []
        for row_index, row in enumerate(self.grid):
            for col_index, cell in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                self.hit_rects.append(rect)

    def get_hit(self, point):
        """Handle soil being hit with hoe."""
        for rect in self.hit_rects:
            if rect.collidepoint(point):
                self.hoe_sound.play()
                
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE

                if 'F' not in self.grid[y][x]:
                    self.grid[y][x].append('F')
                    
                    # Create soil tile
                    surf = choice(self.soil_surfs)
                    SoilTile(
                        pos=(rect.x, rect.y),
                        surf=surf,
                        groups=[self.all_sprites, self.soil_sprites]
                    )

    def water(self, target_pos):
        """Water the soil at target position."""
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):
                
                # Add water to grid
                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE
                self.grid[y][x].append('W')

                # Create soil water tile
                SoilWaterTile(  # Use the new class
                    pos=soil_sprite.rect.topleft,
                    surf=choice(self.water_surfs),
                    groups=[self.all_sprites, self.water_sprites]
                )

    def water_all(self):
        """Water all farmable soil."""
        for row_index, row in enumerate(self.grid):
            for col_index, cell in enumerate(row):
                if 'F' in cell and 'W' not in cell:
                    cell.append('W')
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE
                    SoilWaterTile(  # Use the new class
                        pos=(x, y),
                        surf=choice(self.water_surfs),
                        groups=[self.all_sprites, self.water_sprites]
                    )

    def remove_water(self):
        """Remove all water."""
        # Kill water sprites
        for sprite in self.water_sprites.sprites():
            sprite.kill()
            
        # Remove water from grid
        for row in self.grid:
            for cell in row:
                if 'W' in cell:
                    cell.remove('W')

    def check_watered(self, pos):
        """Check if position is watered."""
        x = pos[0] // TILE_SIZE
        y = pos[1] // TILE_SIZE
        cell = self.grid[y][x]
        is_watered = 'W' in cell
        return is_watered

    def plant_seed(self, target_pos, seed):
        """Plant a seed at target position."""
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):
                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE

                if 'P' not in self.grid[y][x]:
                    self.grid[y][x].append('P')
                    Plant(
                        plant_type=seed,
                        groups=[self.all_sprites, self.plant_sprites, self.collision_sprites],
                        soil=soil_sprite,
                        check_watered=self.check_watered
                    )

    def update_plants(self):
        """Update all plants."""
        for plant in self.plant_sprites.sprites():
            plant.grow()

    def maxAgeAllPlants(self):
        for plant in self.plant_sprites.sprites():
            plant.setAgetoMax()
