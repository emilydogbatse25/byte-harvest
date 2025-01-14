
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Transition:
    def __init__(self, reset_function, player):
        # Display surface
        self.display_surface = pygame.display.get_surface()
        
        # Reset function and player reference
        self.reset_function = reset_function
        self.player = player
        
        # Transition parameters
        self.duration = 2000  # Total duration for fade-out and fade-in phases (in milliseconds)
        self.timer = 0  # Tracks elapsed time during the transition
        self.active = False  # Indicates whether the transition is active
        self.transition_phase = 'fade_out'  # Can be 'fade_out' or 'fade_in'
        
        # Overlay surface for the fade effect
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.overlay.fill('black')  # The overlay color (black for now)

    def play(self, dt):
        """
        Plays the transition effect. Handles fade-out and fade-in phases.
        :param dt: Delta time for smooth transition scaling.
        """
        if not self.active:
            return
        
        # Update the timer
        self.timer += dt
        
        # Calculate progress (0 to 1)
        progress = self.timer / self.duration
        progress = min(progress, 1)  # Cap progress at 1

        if self.transition_phase == 'fade_out':
            # Fade out: Increase opacity from 0 to 255
            alpha = int(progress * 255)
            self.overlay.set_alpha(alpha)
            self.display_surface.blit(self.overlay, (0, 0))

            if progress >= 1:  # If fade-out is complete
                self.reset_function()  # Call the reset function
                self.timer = 0  # Reset the timer for the next phase
                self.transition_phase = 'fade_in'
        
        elif self.transition_phase == 'fade_in':
            # Fade in: Decrease opacity from 255 to 0
            alpha = int((1 - progress) * 255)
            self.overlay.set_alpha(alpha)
            self.display_surface.blit(self.overlay, (0, 0))

            if progress >= 1:  # If fade-in is complete
                self.active = False  # End the transition
                self.player.sleep = False  # Ensure the player is no longer "sleeping"
                self.transition_phase = 'fade_out'  # Reset for the next transition
                self.timer = 0  # Reset the timer for future transitions

    def start(self):
        """
        Activates the transition sequence, starting with fade-out.
        """
        self.active = True
        self.timer = 0
        self.transition_phase = 'fade_out'
        self.player.sleep = True  # Mark the player as sleeping during the transition
