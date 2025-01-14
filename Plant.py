
import pygame
from constants import *
import random
from support import import_folder

class Plant(pygame.sprite.Sprite):
    def __init__(self, plant_type, groups, soil, check_watered):
        super().__init__(groups)
        
        # Setup
        self.plant_type = plant_type
        self.frames = import_folder(f'graphics/fruit/{plant_type}')
        self.soil = soil
        self.check_watered = check_watered
        
        # Growth
        self.age = 0
        self.max_age = len(self.frames) - 1
        self.grow_speed = GROW_SPEED[plant_type]
        
        # Sprite setup
        self.image = self.frames[self.age]
        self.y_offset = -16
        self.rect = self.image.get_rect(midbottom = soil.rect.midbottom + pygame.math.Vector2(0,self.y_offset))
        self.z = LAYERS['ground plant']

        # Attributes
        self.harvestable = False
        
        # Randomize growth speed (50% chance of different speed)
        random.seed(123)  # For testing - remove in production
        r = random.randint(1, 10)
        if r % 2 == 0:
            self.grow_speed = GROW_SPEED[self.plant_type]
        else:
            self.grow_speed = r/10

    def grow(self):
        if self.check_watered(self.rect.center):
            self.age += self.grow_speed

            # If plant reaches max age
            if self.age >= self.max_age:
                self.age = self.max_age
                self.harvestable = True

            # Update sprite
            self.image = self.frames[int(self.age)]
            self.rect = self.image.get_rect(midbottom = self.soil.rect.midbottom + pygame.math.Vector2(0,self.y_offset))

    def setAgetoMax(self):
        if self.check_watered(self.rect.center):
            self.age = self.max_age

            # If plant reaches max age
            if self.age >= self.max_age:
                self.age = self.max_age
                self.harvestable = True

            # Update sprite
            self.image = self.frames[int(self.age)]
            self.rect = self.image.get_rect(midbottom = self.soil.rect.midbottom + pygame.math.Vector2(0,self.y_offset))