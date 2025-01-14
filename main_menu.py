# import pygame
# from constants import SCREEN_WIDTH, SCREEN_HEIGHT

# class Button:
#     def __init__(self, text, pos, size=(200, 50), font_path='graphics/PixelEleganceRegular-ovyAA.ttf'):
#         self.rect = pygame.Rect(0, 0, size[0], size[1])
#         self.rect.center = pos
#         self.text = text
#         self.is_hovered = False
        
#         # Colors
#         self.normal_color = (51, 153, 137)  # Turquoise
#         self.hover_color = (61, 183, 164)   # Lighter turquoise
#         self.text_color = (255, 255, 255)   # White
        
#         # Text setup with custom font
#         try:
#             self.font = pygame.font.Font(font_path, 24)
#         except:
#             print(f"Couldn't load custom font {font_path}, using default")
#             self.font = pygame.font.SysFont('arial', 24)
            
#         self.text_surf = self.font.render(text, True, self.text_color)
#         self.text_rect = self.text_surf.get_rect(center=self.rect.center)

#     def draw(self, surface):
#         color = self.hover_color if self.is_hovered else self.normal_color
#         pygame.draw.rect(surface, color, self.rect, border_radius=12)
#         pygame.draw.rect(surface, (255, 255, 255), self.rect, 3, border_radius=12)
#         surface.blit(self.text_surf, self.text_rect)

#     def handle_event(self, event):
#         if event.type == pygame.MOUSEMOTION:
#             self.is_hovered = self.rect.collidepoint(event.pos)
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if self.is_hovered:
#                 return True
#         return False

# class MainMenu:
#     def __init__(self):
#         self.display_surface = pygame.display.get_surface()
#         self.background = pygame.image.load('graphics/world/title_bg.jpg').convert()
#         self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
#         # Load custom font from graphics folder
#         try:
#             self.title_font = pygame.font.Font('graphics/PixelEleganceRegular-ovyAA.ttf', 72)
#             self.instructions_font = pygame.font.Font('graphics/PixelEleganceRegular-ovyAA.ttf', 20)
#             print("Successfully loaded custom font from graphics folder")
#         except Exception as e:
#             print(f"Couldn't load custom font: {e}")
#             self.title_font = pygame.font.SysFont('arial', 72)
#             self.instructions_font = pygame.font.SysFont('arial', 20)
        
#         # Title with shadow effect
#         self.title = self.title_font.render('Byte Harvest', True, (255, 255, 255))
#         self.title_shadow = self.title_font.render('Byte Harvest', True, (0, 0, 0))
#         self.title_rect = self.title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
#         self.title_shadow_rect = self.title_shadow.get_rect(center=(SCREEN_WIDTH//2 + 4, SCREEN_HEIGHT//4 + 4))
        
#         # Buttons
#         button_y = SCREEN_HEIGHT//2
#         font_path = 'graphics/PixelEleganceRegular-ovyAA.ttf'  # Updated font path
#         self.play_button = Button('Play', (SCREEN_WIDTH//2, button_y), font_path=font_path)
#         self.instructions_button = Button('Instructions', (SCREEN_WIDTH//2, button_y + 70), font_path=font_path)
#         self.exit_button = Button('Exit', (SCREEN_WIDTH//2, button_y + 140), font_path=font_path)

#         # Instructions text
#         self.instructions = [
#             "WASD or Arrow Keys - Move character",
#             "SPACE - Use tool",
#             "Q - Switch tool",
#             "E - Switch seed",
#             "LCTRL - Plant seed",
#             "RETURN - Sleep/Shop",
#             "T - Start productivity timer",
#             "ESC - Exit menu/shop"
#         ]
        
#         self.show_instructions = False

#     def draw_instructions(self):
#         # Draw semi-transparent background
#         s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
#         s.set_alpha(128)
#         s.fill((0, 0, 0))
#         self.display_surface.blit(s, (0, 0))
        
#         # Draw instructions with shadow effect
#         for i, text in enumerate(self.instructions):
#             # Draw shadow
#             shadow_surf = self.instructions_font.render(text, True, (0, 0, 0))
#             shadow_rect = shadow_surf.get_rect(center=(SCREEN_WIDTH//2 + 2, SCREEN_HEIGHT//4 + i*40 + 2))
#             self.display_surface.blit(shadow_surf, shadow_rect)
            
#             # Draw text
#             text_surf = self.instructions_font.render(text, True, (255, 255, 255))
#             text_rect = text_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4 + i*40))
#             self.display_surface.blit(text_surf, text_rect)
        
#         # Back button
#         self.exit_button.draw(self.display_surface)

#     def run(self):
#         self.display_surface.blit(self.background, (0, 0))
        
#         if self.show_instructions:
#             self.draw_instructions()
#             return None
        
#         # Draw title with shadow effect
#         self.display_surface.blit(self.title_shadow, self.title_shadow_rect)
#         self.display_surface.blit(self.title, self.title_rect)
        
#         # Draw buttons
#         self.play_button.draw(self.display_surface)
#         self.instructions_button.draw(self.display_surface)
#         self.exit_button.draw(self.display_surface)
        
#         # Handle events
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 return 'quit'
            
#             if self.play_button.handle_event(event):
#                 return 'play'
#             if self.instructions_button.handle_event(event):
#                 self.show_instructions = True
#             if self.exit_button.handle_event(event):
#                 if self.show_instructions:
#                     self.show_instructions = False
#                 else:
#                     return 'quit'
        
#         return None