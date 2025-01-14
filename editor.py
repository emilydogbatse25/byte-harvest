import pygame
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, 
    PAGE_WIDTH, PAGE_HEIGHT, 
    MAX_CHARACTERS
)

class Editor:
    def __init__(self):
        # Get the display surface
        self.display_surface = pygame.display.get_surface()

        # Initialize pygame's font module
        pygame.font.init()
        self.font = pygame.font.SysFont("couriernew", 24)  # Monospaced font

        # Initial text setup
        self.text = self.font.render('', True, 'black', 'white')
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (SCREEN_WIDTH/2 - 450, SCREEN_HEIGHT/5)

        # Page offset for scrolling
        self.page_offset = 0

        # User input storage
        self.user_input = ""

    def run(self, text_side):
        # Draw background
        background = text_side
        self.display_surface.fill((114, 183, 219), background)  # Light blue background

        # Draw the page
        self.draw_page()
        
        # Handle input
        event_list = pygame.event.get(pygame.KEYDOWN)
        self.handle_events(event_list)

        # Display current text
        self.display()

    def draw_page(self):
        # Draw white page background
        pygame.draw.rect(
            self.display_surface, 
            'white', 
            pygame.Rect(
                (SCREEN_WIDTH/2)-(PAGE_WIDTH/2), 
                (SCREEN_HEIGHT/8), 
                PAGE_WIDTH, 
                PAGE_HEIGHT
            )
        )
        
        # Draw margins
        left_margin = pygame.Rect(
            (SCREEN_WIDTH/2) - 460,
            (SCREEN_HEIGHT/8),
            2,  # Width of margin line
            PAGE_HEIGHT
        )
        right_margin = pygame.Rect(
            (SCREEN_WIDTH/2) + 460,
            (SCREEN_HEIGHT/8),
            2,  # Width of margin line
            PAGE_HEIGHT
        )
        
        pygame.draw.rect(self.display_surface, 'black', left_margin)
        pygame.draw.rect(self.display_surface, 'black', right_margin)
    
    def display(self):
        # Update text surface with current input
        self.text = self.font.render(self.user_input, True, 'black', 'white')
        
        # Draw the text
        self.display_surface.blit(self.text, self.text_rect)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Handle letters and standard characters
                if event.key < 127 and event.key > 31:
                    if event.mod & pygame.KMOD_SHIFT:  # Check for shift key
                        self.user_input += pygame.key.name(event.key).upper()
                    else:
                        self.user_input += pygame.key.name(event.key)

                # Handle backspace
                elif event.key == pygame.K_BACKSPACE and len(self.user_input) > 0:
                    self.user_input = self.user_input[:-1]

                # Handle space
                elif event.key == pygame.K_SPACE:
                    self.user_input += " "

                # Handle enter/return
                elif event.key == pygame.K_RETURN:
                    self.user_input = self.user_input.ljust(MAX_CHARACTERS)

        # Keep input within maximum character limit
        if len(self.user_input) > MAX_CHARACTERS:
            self.user_input = self.user_input[:MAX_CHARACTERS]