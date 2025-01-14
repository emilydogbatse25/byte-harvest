

import pygame

class Timer:
    def __init__(self, duration, func=None):
        self.duration = duration
        self.func = func    # Function to call when timer completes
        self.start_time = 0
        self.active = False

    def activate(self):
        """Start the timer."""
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        """Stop the timer."""
        self.active = False
        self.start_time = 0

    def update(self):
        """Update the timer and call function if duration reached."""
        current_time = pygame.time.get_ticks()
        
        if self.active and current_time - self.start_time >= self.duration:
            if self.func:
                self.func()
            self.deactivate()