import pygame
from constants import *
from support import import_folder
from timer_byte import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, tree_sprites, interaction_sprites, soil_layer, toggle_shop):
        super().__init__(group)

        # Animation setup
        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # General setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['main']

        # Movement
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = SPEED

        # Collision
        self.hitbox = self.rect.copy().inflate(-30, -50)  # Adjusted hitbox size
        self.collision_sprites = collision_sprites

        # Timers
        self.timers = {
            'tool use': Timer(350, self.use_tool),
            'tool switch': Timer(200),
            'seed use': Timer(350, self.use_seed),
            'seed switch': Timer(200),
        }

        # Tools
        self.tools = ['hoe', 'axe', 'water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        # Seeds
        self.seeds = ['corn', 'tomato']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]

        # Inventory
        self.item_inventory = {
            'wood': 0,
            'apple': 0,
            'corn': 0,
            'tomato': 0
        }
        self.seed_inventory = {
            'corn': 5,
            'tomato': 5
        }
        self.money = 200

        # Interaction
        self.tree_sprites = tree_sprites
        self.interaction_sprites = interaction_sprites
        self.soil_layer = soil_layer
        self.toggle_shop = toggle_shop
        self.sleep = False

        # Locking movement and actions
        self.can_move = True
        self.can_act = True

        # Sound
        try:
            self.watering = pygame.mixer.Sound('graphics/water.mp3')
            self.watering.set_volume(0.2)
        except:
            print("Water sound not found")

    def import_assets(self):
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
            'up_hoe': [], 'down_hoe': [], 'left_hoe': [], 'right_hoe': [],
            'up_axe': [], 'down_axe': [], 'left_axe': [], 'right_axe': [],
            'up_water': [], 'down_water': [], 'left_water': [], 'right_water': []
        }

        for animation in self.animations.keys():
            full_path = f'graphics/character/{animation}'
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        if not self.timers['tool use'].active and not self.sleep:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_z]:
                print(f"===== x: {self.pos.x} - y: {self.pos.y}")


            # Movement input
            if self.can_move:
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    self.direction.y = -1
                    self.status = 'up'
                elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    self.direction.y = 1
                    self.status = 'down'
                else:
                    self.direction.y = 0

                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.direction.x = 1
                    self.status = 'right'
                elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.direction.x = -1
                    self.status = 'left'
                else:
                    self.direction.x = 0

            # Tool use input
            if self.can_act and keys[pygame.K_SPACE]:
                # Allow tool use when can_act is True
                self.timers['tool use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            # Other input checks remain the same...
            if self.can_act:
                # Tool switch
                if keys[pygame.K_q] and not self.timers['tool switch'].active:
                    self.timers['tool switch'].activate()
                    self.tool_index = (self.tool_index + 1) % len(self.tools)
                    self.selected_tool = self.tools[self.tool_index]

                # Seed use input
                if keys[pygame.K_LCTRL]:
                    self.timers['seed use'].activate()
                    self.direction = pygame.math.Vector2()
                    self.frame_index = 0

                # Seed switch
                if keys[pygame.K_e] and not self.timers['seed switch'].active:
                    self.timers['seed switch'].activate()
                    self.seed_index = (self.seed_index + 1) % len(self.seeds)
                    self.selected_seed = self.seeds[self.seed_index]

                # Interaction
                if keys[pygame.K_RETURN]:
                    collided = pygame.sprite.spritecollide(self, self.interaction_sprites, False)
                    if collided:
                        if collided[0].name == 'Trader':
                            self.toggle_shop()
                        elif collided[0].name == 'Bed':
                            self.status = 'left_idle'
                            self.sleep = True

    def get_status(self):
        if self.direction.magnitude() == 0:
            if not 'idle' in self.status:
                self.status = self.status.split('_')[0] + '_idle'

        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
                        if self.direction.x > 0:  # Moving right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:  # Moving left
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx

                    if direction == 'vertical':
                        if self.direction.y > 0:  # Moving down
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:  # Moving up
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def move(self, dt):
        if not self.can_move:
            return

        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # Horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        # Vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def use_tool(self):
        if self.selected_tool == 'hoe':
            self.soil_layer.get_hit(self.target_pos)
        if self.selected_tool == 'axe':
            for tree in self.tree_sprites.sprites():
                if tree.rect.collidepoint(self.target_pos):
                    tree.damage()
        if self.selected_tool == 'water':
            self.soil_layer.water(self.target_pos)
            self.watering.play()

    def use_seed(self):
        if self.seed_inventory[self.selected_seed] > 0:
            if self.soil_layer.plant_seed(self.target_pos, self.selected_seed):
                self.seed_inventory[self.selected_seed] -= 1

    def get_target_pos(self):
        self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def set_movement_lock(self, locked):
        """Set whether the player can move or not"""
        self.can_move = not locked
        if locked:
            self.direction = pygame.math.Vector2()

    def set_action_lock(self, locked):
        """Set whether the player can perform actions or not"""
        self.can_act = not locked

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.get_target_pos()
        self.move(dt)
        self.animate(dt)