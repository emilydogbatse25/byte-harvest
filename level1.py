import pygame
from constants import *
from player import Player
from overlay import Overlay
from sprites import Terrain, WaterTile, WildFlower, Tree, Interaction, Particle
from pytmx.util_pygame import load_pygame
from sprite_loader import import_folder
from transition1 import Transition
from SoilLayer import SoilLayer
from menu1 import Menu
from cameraGroup import CameraGroup
from animal import Animal
from random import randint
from pomodoroTimer import Pomodoro


class Level:
    def __init__(self, farm_screen):
        # Display surface
        self.farm_screen = farm_screen

        # Sprite groups
        self.all_sprites = CameraGroup(self.farm_screen)
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()
        self.animal_sprites = pygame.sprite.Group()

        # Soil setup
        self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)

        # Timer setup
        self.timer_active = False
        self.pomodoro = Pomodoro(self.farm_screen, self.soil_layer)
        self.last_working_state = True

        # Setup level components
        self.setup()
        self.setup_animals()

        # Set a better starting position in an open area
        self.default_position = pygame.math.Vector2(1640, 1825)
        #self.default_position = pygame.math.Vector2(1640, 1640)

        # UI elements
        self.overlay = Overlay(self.player)
        self.transition = Transition(self.reset, self.player)

        # Menu
        self.menu = Menu(self.player, self.toggle_shop, self.farm_screen)
        self.menu_active = False

        # Setup audio
        self.setup_audio()

        # Ensure player starts locked
        self.player.set_movement_lock(True)
        self.player.set_action_lock(True)

        # Store initial position
        self.initial_position = pygame.math.Vector2(self.player.pos.x, self.player.pos.y)

    def setup_audio(self):
        try:
            pygame.mixer.music.load('audio/score.mp3')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.3)
        except:
            print("Music file not found")

    def reset_player_position(self):
        """Reset player to default position"""
        self.player.pos.x = self.default_position.x
        self.player.pos.y = self.default_position.y
        self.player.hitbox.center = self.player.pos
        self.player.rect.center = self.player.hitbox.center

    def setup(self):
        tmx_data = load_pygame('data/map.tmx')

        # Setup house layers
        self.setup_house(tmx_data)

        # Setup map layers and boundaries
        self.setup_map_elements(tmx_data)
        self.add_map_boundaries(tmx_data)
        self.setup_player_and_interactions(tmx_data)
  
    def setup_house(self, tmx_data):
        # Define door area
        """
        DOOR_POSITIONS = [
            (15, 10), (16, 10),  # Door entrance
            (15, 11), (16, 11)   # Inside house near door
            41
        ]
        """
        DOOR_POSITIONS = [
            (15 * TILE_SIZE, 10* TILE_SIZE), (16* TILE_SIZE, 10* TILE_SIZE),  # Door entrance
            (15* TILE_SIZE, 11* TILE_SIZE), (16* TILE_SIZE, 11* TILE_SIZE)   # Inside house near door
        ]

        # House floor and bottom furniture (no collision)
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                if surf:
                    Terrain(
                        pos=(x * TILE_SIZE, y * TILE_SIZE),
                        surf=surf,
                        groups=[self.all_sprites],
                        z=LAYERS['house bottom']
                    )

        # House walls with door handling
        for x, y, surf in tmx_data.get_layer_by_name('HouseWalls').tiles():
            if surf:
                if (x, y) not in DOOR_POSITIONS:
                    # Regular wall with collision
                    Terrain(
                        pos=(x * TILE_SIZE, y * TILE_SIZE),
                        surf=surf,
                        groups=[self.all_sprites, self.collision_sprites],
                        #z=LAYERS['house bottom']
                    )
                else:
                    # Door area without collision
                    Terrain(
                        pos=(x * TILE_SIZE, y * TILE_SIZE),
                        surf=surf,
                        groups=[self.all_sprites],
                        z=LAYERS['house bottom']
                    )

        # House top furniture (above player)
        for x, y, surf in tmx_data.get_layer_by_name('HouseFurnitureTop').tiles():
            if surf:
                Terrain(
                    pos=(x * TILE_SIZE, y * TILE_SIZE),
                    surf=surf,
                    groups=[self.all_sprites],
                    z=LAYERS['house top']
                )
  
    def setup_map_elements(self, tmx_data):
        # Fence
        for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
            if surf:
                Terrain(
                    pos=(x * TILE_SIZE, y * TILE_SIZE),
                    surf=surf,
                    groups=[self.all_sprites, self.collision_sprites]
                )

        # Water
        water_frames = import_folder('graphics/water')
        for x, y, _ in tmx_data.get_layer_by_name('Water').tiles():
            WaterTile(
                pos=(x * TILE_SIZE, y * TILE_SIZE),
                frames=water_frames,
                groups=[self.all_sprites]
            )

        # Trees
        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree(
                pos=(obj.x, obj.y),
                surf=obj.image,
                groups=[self.all_sprites, self.collision_sprites, self.tree_sprites],
                name=obj.name,
                player_add=self.player_add
            )

        # Decoration
        for obj in tmx_data.get_layer_by_name('Decoration'):
            WildFlower(
                pos=(obj.x, obj.y),
                surf=obj.image,
                groups=[self.all_sprites, self.collision_sprites]
            )

        # Ground
        ground = pygame.image.load('graphics/world/ground.png').convert_alpha()
        Terrain(
            pos=(0, 0),
            surf=ground,
            groups=[self.all_sprites],
            z=LAYERS['ground']
        )

    def setup_animals(self):
        # Position the chicken in the open area near the player
        Animal(
            animal_type='chicken',
            start_pos=(550, 500),
            groups=[self.all_sprites, self.animal_sprites],
            collision_sprites=self.collision_sprites
        )

    def add_map_boundaries(self, tmx_data):
        map_width = tmx_data.width * TILE_SIZE
        map_height = tmx_data.height * TILE_SIZE
        wall_thickness = 32

        walls = [
            (0, 0, wall_thickness, map_height),              # Left
            (map_width - wall_thickness, 0, wall_thickness, map_height),  # Right
            (0, 0, map_width, wall_thickness),              # Top
            (0, map_height - wall_thickness, map_width, wall_thickness)   # Bottom
        ]

        for x, y, width, height in walls:
            wall_surf = pygame.Surface((width, height), pygame.SRCALPHA)
            collision_sprite = Terrain(
                pos=(x, y),
                surf=wall_surf,
                groups=[self.collision_sprites]
            )
            collision_sprite.rect = pygame.Rect(x, y, width / 2, height / 2)
            collision_sprite.hitbox = collision_sprite.rect

    def setup_player_and_interactions(self, tmx_data):
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
                self.player = Player(
                    pos=(obj.x, obj.y),
                    group=self.all_sprites,
                    collision_sprites=self.collision_sprites,
                    tree_sprites=self.tree_sprites,
                    interaction_sprites=self.interaction_sprites,
                    soil_layer=self.soil_layer,
                    toggle_shop=self.toggle_shop
                )
            elif obj.name == 'Trader':
                Interaction(
                    pos=(obj.x, obj.y),
                    size=(obj.width, obj.height),
                    groups=[self.interaction_sprites],
                    name=obj.name
                )
            elif obj.name == 'Bed':
                Interaction(
                    pos=(obj.x, obj.y),
                    size=(obj.width, obj.height),
                    groups=[self.interaction_sprites],
                    name=obj.name
                )

    def player_add(self, item):
        self.player.item_inventory[item] += 1

    def toggle_shop(self):
        self.menu_active = not self.menu_active

    def reset(self):
        self.soil_layer.update_plants()

        for tree in self.tree_sprites.sprites():
            for apple in tree.apple_sprites.sprites():
                apple.kill()
            tree.create_fruit()

    def tree_collision(self):
        """Handle tree collision and damage"""
        keys = pygame.key.get_pressed()
        for tree in self.tree_sprites.sprites():
            if tree.rect.colliderect(self.player.hitbox) and self.player.selected_tool == 'axe' and keys[pygame.K_SPACE]:
                tree.damage()

    def run(self, dt, event_list):
        self.handle_input(event_list)

        # If timer isn't active, player shouldn't be able to move or act
        if not self.timer_active:
            self.player.set_movement_lock(True)
            self.player.set_action_lock(True)

        if self.timer_active:
            should_continue = self.pomodoro.run(event_list)
            if not should_continue:
                self.timer_active = False
                self.player.set_movement_lock(True)
                self.player.set_action_lock(True)
            else:
                if self.pomodoro.working:
                    self.player.set_movement_lock(True)
                    self.player.set_action_lock(True)
                    self.farm_screen.fill('black')
                    self.pomodoro.draw()
                    self.last_working_state = True
                    return
                else:
                    # Only reset position when transitioning from work to break
                    if self.last_working_state:
                        self.reset_player_position()
                        self.last_working_state = False
                    self.player.set_movement_lock(False)
                    self.player.set_action_lock(False)

        self.farm_screen.fill('black')

        if self.menu_active:
            self.menu.update()
        else:
            self.all_sprites.custom_draw(self.player)
            self.all_sprites.update(dt)
            self.plant_collision()
            if self.timer_active and not self.pomodoro.working:
                self.tree_collision()

        self.overlay.display()

        if self.timer_active and not self.pomodoro.working:
            self.pomodoro.draw()

        if self.player.sleep or self.transition.active:
            self.transition.play(dt)

    def handle_input(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t and not self.timer_active:
                    print("Starting timer...")
                    self.timer_active = True
                    self.pomodoro.setup()
                    self.player.set_movement_lock(True)
                    self.player.set_action_lock(True)
                elif event.key == pygame.K_ESCAPE and self.timer_active:
                    self.timer_active = False
                    # Only reset position if we were in a break
                    if not self.pomodoro.working:
                        self.reset_player_position()
                    self.player.set_movement_lock(True)
                    self.player.set_action_lock(True)

                if event.key == pygame.K_m:
                    self.toggle_shop()

    def plant_collision(self):
        if hasattr(self.soil_layer, 'plant_sprites'):
            for plant in self.soil_layer.plant_sprites.sprites():
                if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
                    self.player_add(plant.plant_type)
                    plant.kill()
                    Particle(
                        pos=plant.rect.topleft,
                        surf=plant.image,
                        groups=[self.all_sprites],
                        z=LAYERS['main']
                    )
                    grid_x = plant.rect.centerx // TILE_SIZE
                    grid_y = plant.rect.centery // TILE_SIZE
                    if 'P' in self.soil_layer.grid[grid_y][grid_x]:
                        self.soil_layer.grid[grid_y][grid_x].remove('P')
