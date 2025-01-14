
import pygame
import datetime
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from SoilLayer import SoilLayer

class Pomodoro:
    def __init__(self, display_surface, soil_layer):
        self.display_surface = display_surface
        self.soil_layer = soil_layer
        
        # Timer states
        self.timer_active = False
        self.working = True
        self.collecting_input = True
        self.current_input = ""
        self.input_stage = 'work'  # 'work', 'break', or 'sequences'
        
        # Time tracking
        self.work_duration = 0
        self.break_duration = 0
        self.total_sequences = 0
        self.current_sequence = 1
        self.start_time = None
        self.end_time = None
        
        # Colors
        self.work_color = (255, 136, 77)  # Warm orange
        self.break_color = (102, 204, 153)  # Soft green
        self.text_color = (255, 255, 255)  # White
        
        # Font setup
        try:
            self.title_font = pygame.font.Font('graphics/PixelatedEleganceRegular-ovyAA.ttf', 64)
            self.font = pygame.font.Font('graphics/PixelatedEleganceRegular-ovyAA.ttf', 48)
            self.info_font = pygame.font.Font('graphics/PixelatedEleganceRegular-ovyAA.ttf', 32)
        except:
            print("Custom font not found, using default")
            self.title_font = pygame.font.SysFont('couriernew', 64)
            self.font = pygame.font.SysFont('couriernew', 48)
            self.info_font = pygame.font.SysFont('couriernew', 32)
            
        # Create overlay surface
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(180)  # Semi-transparent

    def setup(self):
        self.collecting_input = True
        self.input_stage = 'work'
        self.current_input = ""
        self.timer_active = True
        self.current_sequence = 1

    def handle_input(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.timer_active = False
                    return False
                elif event.key == pygame.K_RETURN and self.current_input:
                    duration = int(self.current_input)
                    if self.input_stage == 'work':
                        self.work_duration = duration
                        self.input_stage = 'break'
                    elif self.input_stage == 'break':
                        self.break_duration = duration
                        self.input_stage = 'sequences'
                    elif self.input_stage == 'sequences':
                        self.total_sequences = duration
                        self.collecting_input = False
                        self.start_timer()
                    self.current_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.current_input = self.current_input[:-1]
                elif event.unicode.isdigit():
                    self.current_input += event.unicode
        return True

    def start_timer(self):
        self.working = True
        self.start_time = datetime.datetime.now()
        self.end_time = self.start_time + datetime.timedelta(minutes=self.work_duration)

    def draw_input_screen(self):
        # Draw dark overlay
        self.display_surface.blit(self.overlay, (0, 0))
        
        # Get current window size
        current_width = self.display_surface.get_width()
        current_height = self.display_surface.get_height()

        # Title
        title = "Pomodoro Timer Setup"
        title_surf = self.title_font.render(title, True, self.text_color)
        title_rect = title_surf.get_rect(center=(current_width/2, current_height/4))

        # Prompt based on input stage
        if self.input_stage == 'work':
            prompt = "Enter work duration (minutes):"
        elif self.input_stage == 'break':
            prompt = "Enter break duration (minutes):"
        else:
            prompt = "Enter number of sequences:"

        prompt_surf = self.font.render(prompt, True, self.text_color)
        prompt_rect = prompt_surf.get_rect(center=(current_width/2, current_height/2 - 50))

        # Input text with blinking cursor
        cursor = "█" if pygame.time.get_ticks() % 1000 < 500 else " "
        input_text = self.current_input + cursor
        input_surf = self.font.render(input_text, True, self.work_color if self.input_stage == 'work' else self.break_color)
        input_rect = input_surf.get_rect(center=(current_width/2, current_height/2 + 50))

        # Draw elements
        self.display_surface.blit(title_surf, title_rect)
        self.display_surface.blit(prompt_surf, prompt_rect)
        self.display_surface.blit(input_surf, input_rect)

        # Draw instructions
        instructions = ["Press ENTER to confirm", "Press ESC to exit"]
        for i, instruction in enumerate(instructions):
            inst_surf = self.info_font.render(instruction, True, (200, 200, 200))
            inst_rect = inst_surf.get_rect(center=(current_width/2, current_height*3/4 + i*40))
            self.display_surface.blit(inst_surf, inst_rect)

    def draw_timer(self):
        current_width = self.display_surface.get_width()
        current_height = self.display_surface.get_height()
        
        if self.working:
            # Work phase - full screen
            self.display_surface.blit(self.overlay, (0, 0))
            
            # Draw "Focus Time!"
            focus_text = "Focus Time!"
            focus_surf = self.title_font.render(focus_text, True, self.work_color)
            focus_rect = focus_surf.get_rect(center=(current_width/2, current_height/4))
            self.display_surface.blit(focus_surf, focus_rect)
            
            # Draw timer with decorative box
            remaining = self.end_time - datetime.datetime.now()
            minutes = int(remaining.total_seconds() // 60)
            seconds = int(remaining.total_seconds() % 60)
            timer_text = f"{minutes:02d}:{seconds:02d}"
            
            timer_surf = self.font.render(timer_text, True, self.text_color)
            timer_rect = timer_surf.get_rect(center=(current_width/2, current_height/2))
            
            # Draw box around timer
            padding = 40
            box_rect = timer_rect.inflate(padding * 2, padding)
            pygame.draw.rect(self.display_surface, self.work_color, box_rect, 3, border_radius=10)
            
            self.display_surface.blit(timer_surf, timer_rect)
            
            # Draw sequence counter
            sequence_text = f"Sequence {self.current_sequence}/{self.total_sequences}"
            sequence_surf = self.info_font.render(sequence_text, True, self.text_color)
            sequence_rect = sequence_surf.get_rect(center=(current_width/2, current_height*3/4))
            self.display_surface.blit(sequence_surf, sequence_rect)
            
        else:
            # Break phase - overlay timer
            remaining = self.end_time - datetime.datetime.now()
            minutes = int(remaining.total_seconds() // 60)
            seconds = int(remaining.total_seconds() % 60)
            timer_text = f"Break Time: {minutes:02d}:{seconds:02d}"
            
            # Create a semi-transparent background for the break timer
            timer_surf = self.font.render(timer_text, True, self.break_color)
            timer_rect = timer_surf.get_rect()
            timer_rect.topleft = (20, 20)  # Position in top-left corner
            
            # Draw background box
            padding = 20
            box_rect = timer_rect.inflate(padding * 2, padding)
            box_rect.topleft = (10, 10)
            
            # Draw rounded rectangle background
            pygame.draw.rect(self.display_surface, (0, 0, 0, 128), box_rect, border_radius=10)
            pygame.draw.rect(self.display_surface, self.break_color, box_rect, 3, border_radius=10)
            
            self.display_surface.blit(timer_surf, timer_rect)

    def draw(self):
        if self.collecting_input:
            self.draw_input_screen()
        else:
            self.draw_timer()

    def run(self, event_list):
        if self.collecting_input:
            return self.handle_input(event_list)

        current_time = datetime.datetime.now()
        if current_time >= self.end_time:
            if self.working:
                # Switch to break
                self.working = False
                
                # !!!! maxage all plants
                self.soil_layer.maxAgeAllPlants()
                
                self.start_time = current_time
                self.end_time = current_time + datetime.timedelta(minutes=self.break_duration)
            else:
                # Switch to work
                self.current_sequence += 1
                if self.current_sequence > self.total_sequences:
                    self.timer_active = False
                    return False
                self.working = True
                self.start_time = current_time
                self.end_time = current_time + datetime.timedelta(minutes=self.work_duration)

        return True
