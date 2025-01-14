import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from level1 import Level

class Game:
    def __init__(self):
        pygame.init()
        # Set up resizable window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Byte Harvest")
        self.clock = pygame.time.Clock()

        # Create farm surface (this stays at fixed size)
        self.farm_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.level = Level(self.farm_screen)

        # Store original dimensions
        self.original_width = SCREEN_WIDTH
        self.original_height = SCREEN_HEIGHT

    def handle_resize(self, event):
        new_width = max(event.w, SCREEN_WIDTH // 2)  # Don't allow too small
        new_height = max(event.h, SCREEN_HEIGHT // 2)
        self.screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)

    def run(self):
        running = True
        while running:
            # Event handling
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.handle_resize(event)

            # Calculate delta time
            dt = self.clock.tick(60) / 1000  # 60 FPS

            # Update level
            self.level.run(dt, event_list)

            # Scale farm_screen to fit current window size while maintaining aspect ratio
            current_size = self.screen.get_size()
            scale_factor = min(current_size[0] / SCREEN_WIDTH, 
                               current_size[1] / SCREEN_HEIGHT)
            
            scaled_width = int(SCREEN_WIDTH * scale_factor)
            scaled_height = int(SCREEN_HEIGHT * scale_factor)
            
            # Center the scaled surface
            x_offset = (current_size[0] - scaled_width) // 2
            y_offset = (current_size[1] - scaled_height) // 2
            
            # Scale and draw farm screen
            scaled_surface = pygame.transform.smoothscale(self.farm_screen, 
                                                          (scaled_width, scaled_height))
            self.screen.fill('black')  # Fill with black to cover empty space
            self.screen.blit(scaled_surface, (x_offset, y_offset))
            
            pygame.display.flip()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
