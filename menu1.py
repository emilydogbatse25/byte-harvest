import pygame
from constants import *
from timer_byte import Timer

class Menu:
    def __init__(self, player, toggle_menu, farm_screen):
        # Basic setup
        self.player = player
        self.toggle_menu = toggle_menu
        self.farm_screen = farm_screen
        self.font = pygame.font.SysFont('couriernew', 26)
        
        # Menu spacing
        self.padding = 30
        
        # Menu options from player inventory and shop items
        self.menu_options = []
        self.menu_options += list(self.player.item_inventory.keys())
        self.num_sellable = len(self.menu_options)  # Track number of sellable items
        self.menu_options += PURCHASE_PRICES.keys()
        
        # Complete setup
        self.setup()
        
        # Selection management
        self.selector_index = 0
        self.timer = Timer(200)  # Timer for input delay

    def setup(self):
        # Calculate menu dimensions
        self.menu_height = (50 * len(self.menu_options)) + (self.padding * (len(self.menu_options) + 1))
        self.menu_top = FARM_HEIGHT * 0.75
        self.menu_top -= self.menu_height // 2

        # Create text surfaces and rectangles for menu options
        self.option_texts = []
        self.option_rects = []
        
        for i, option in enumerate(self.menu_options):
            # Format option string
            option_string = f" {option}".ljust(27)
            
            # Add price
            if i < self.num_sellable:
                amount = SALE_PRICES[option]
            else:
                amount = PURCHASE_PRICES[option]
            option_string += str(amount).ljust(3)

            # Create text surface
            text = self.font.render(option_string, True, 'black', 'white')
            text_rect = text.get_rect()
            text_rect.center = (SCREEN_WIDTH/2, self.menu_top + (i * (self.padding + 20)))

            self.option_texts.append(text)
            self.option_rects.append(text_rect)

    def display_money(self):
        text = f"Money: {self.player.money}"
        money_surf = self.font.render(text, True, 'black', 'white')
        money_rect = money_surf.get_rect(center=(SCREEN_WIDTH // 2, FARM_HEIGHT - 50))
        self.farm_screen.blit(money_surf, money_rect)

    def display_inventory(self):
        # Background for inventory
        left = SCREEN_WIDTH // 5
        inventory_bg = pygame.Rect(left - 70, FARM_HEIGHT // 7, 250, 300)
        pygame.draw.rect(self.farm_screen, 'white', inventory_bg)
        pygame.draw.rect(self.farm_screen, 'blue', inventory_bg, 2)

        # Items header
        header_text = self.font.render('Items: ', True, 'black', 'white')
        header_rect = header_text.get_rect(left=left - 50, top=FARM_HEIGHT // 6)
        self.farm_screen.blit(header_text, header_rect)

        # Display items
        for i, (item, count) in enumerate(self.player.item_inventory.items()):
            text = f"{item}: {count}"
            item_surf = self.font.render(text, True, 'black', 'white')
            item_rect = item_surf.get_rect(left=left, top=FARM_HEIGHT // 4 + (30 * i))
            self.farm_screen.blit(item_surf, item_rect)

        # Seeds header
        seed_header = self.font.render('Seeds: ', True, 'black', 'white')
        seed_header_rect = seed_header.get_rect(left=left - 50, top=FARM_HEIGHT // 2 + 20)
        self.farm_screen.blit(seed_header, seed_header_rect)

        # Display seeds
        for i, (seed, count) in enumerate(self.player.seed_inventory.items(), 1):
            text = f"{seed}: {count}"
            seed_surf = self.font.render(text, True, 'black', 'white')
            seed_rect = seed_surf.get_rect(left=left, top=FARM_HEIGHT // 2 + 20 + (30 * i))
            self.farm_screen.blit(seed_surf, seed_rect)

    def show_entry(self):
        for i, (text, rect) in enumerate(zip(self.option_texts, self.option_rects)):
            # Display menu option
            self.farm_screen.blit(text, rect)
            
            # Highlight selected option
            if self.selector_index == i:
                border_rect = pygame.Rect(0, 0, 480, 35)
                border_rect.center = (SCREEN_WIDTH/2, self.menu_top + (i * (self.padding + 20)))
                pygame.draw.rect(self.farm_screen, 'black', border_rect, 3)

                # Show BUY/SELL text
                action_font = pygame.font.SysFont('couriernew', 22)
                action_text = "SELL" if i < self.num_sellable else "BUY"
                action_surf = action_font.render(action_text, True, 'black')
                action_rect = action_surf.get_rect(center=border_rect.center)
                self.farm_screen.blit(action_surf, action_rect)

    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()

        if not self.timer.active:
            if keys[pygame.K_UP]:
                self.selector_index = (self.selector_index - 1) % len(self.menu_options)
                self.timer.activate()
            elif keys[pygame.K_DOWN]:
                self.selector_index = (self.selector_index + 1) % len(self.menu_options)
                self.timer.activate()
            elif keys[pygame.K_RETURN]:
                self.timer.activate()
                
                # Get selected item
                item = self.menu_options[self.selector_index]
                
                # Handle selling
                if self.selector_index < self.num_sellable:
                    if self.player.item_inventory[item] >= 1:
                        self.player.item_inventory[item] -= 1
                        self.player.money += SALE_PRICES[item]
                # Handle buying
                else:
                    if self.player.money >= PURCHASE_PRICES[item]:
                        self.player.seed_inventory[item] += 1
                        self.player.money -= PURCHASE_PRICES[item]

    def update(self):
        # Draw menu background
        menu_bg = pygame.Rect(0, 0, 3*SCREEN_WIDTH // 4, FARM_HEIGHT - 50)
        menu_bg.center = (SCREEN_WIDTH // 2, FARM_HEIGHT // 2)
        pygame.draw.rect(self.farm_screen, 'white', menu_bg)
        pygame.draw.rect(self.farm_screen, 'black', menu_bg, 2)

        self.input()
        self.display_money()
        self.display_inventory()
        self.show_entry()