import pygame
import os

def load_spritesheet(path, frame_width, frame_height):
    """
    Load a spritesheet and split it into individual frames.
    """
    try:
        # Load the full spritesheet
        sheet = pygame.image.load(path).convert_alpha()
        sheet_width = sheet.get_width()
        sheet_height = sheet.get_height()

        # Calculate number of frames
        cols = sheet_width // frame_width

        # Create empty list for frames
        frames = []

        # Cut up the spritesheet into individual frames
        for col in range(cols):
            # Create surface for the frame
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)

            # Copy the frame from the sheet
            frame.blit(sheet, (0, 0),
                      (col * frame_width, 0, frame_width, frame_height))

            frames.append(frame)

        return frames

    except (pygame.error, FileNotFoundError) as e:
        print(f"Failed to load spritesheet: {path}")
        print(f"Error: {str(e)}")

        # Create placeholder frames
        frames = []
        for _ in range(4):  # Assume 4 frames for placeholder
            surf = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            surf.fill((255, 192, 203))  # Pink color for visibility
            pygame.draw.rect(surf, (0, 0, 0), surf.get_rect(), 1)  # Black border
            frames.append(surf)
        return frames

def import_folder(path):
    """
    Import all image files from a folder as surfaces.
    """
    surface_list = []

    try:
        for _, __, img_files in os.walk(path):
            # Sort files to ensure consistent ordering
            img_files.sort()  # Ensure consistent order
            for image in img_files:
                if image.endswith(('.png', '.jpg', '.jpeg')):
                    full_path = os.path.join(path, image)
                    try:
                        image_surf = pygame.image.load(full_path).convert_alpha()
                        surface_list.append(image_surf)
                    except pygame.error as e:
                        print(f"Failed to load image: {full_path}")
                        print(f"Error: {str(e)}")
        if not surface_list:
            print(f"No valid images found in {path}")
    except Exception as e:
        print(f"Error accessing path {path}: {str(e)}")

    # If no images were loaded, create a placeholder surface
    if not surface_list:
        placeholder = pygame.Surface((32, 32), pygame.SRCALPHA)
        placeholder.fill((255, 0, 255))  # Magenta for visibility
        pygame.draw.rect(placeholder, (0, 0, 0), placeholder.get_rect(), 1)
        surface_list.append(placeholder)

    return surface_list

def scale_images(surfaces, scale_factor):
    """
    Scale a list of surfaces by a given factor.
    """
    scaled_surfaces = []

    for surface in surfaces:
        width = int(surface.get_width() * scale_factor)
        height = int(surface.get_height() * scale_factor)
        scaled_surface = pygame.transform.scale(surface, (width, height))
        scaled_surfaces.append(scaled_surface)

    return scaled_surfaces

def flip_images(surfaces, flip_x=True, flip_y=False):
    """
    Flip a list of surfaces horizontally and/or vertically.
    """
    return [pygame.transform.flip(surface, flip_x, flip_y) for surface in surfaces]
