import os
import pygame


def import_folder(path):
    """Import all images from a folder into surfaces."""
    surface_list = []

    try:
        for _, __, img_files in os.walk(path):
            for image in sorted(img_files):
                full_path = os.path.join(path, image)
                if image.endswith(('.png', '.jpg', '.jpeg')):
                    try:
                        image_surf = pygame.image.load(full_path).convert_alpha()
                        surface_list.append(image_surf)
                    except pygame.error:
                        print(f'Failed to load image: {full_path}')
    except Exception as e:
        print(f'Error accessing path {path}: {str(e)}')

    # Create placeholder if no images loaded
    if not surface_list:
        placeholder = pygame.Surface((32, 32))
        placeholder.fill((255, 0, 255))  # Magenta for visibility
        surface_list.append(placeholder)
        print(f"No images found in {path}, using placeholder")

    return surface_list

def import_folder_dict(path):
    """Import images from folder into a dictionary using filenames as keys."""
    surface_dict = {}

    try:
        for _, __, img_files in os.walk(path):
            for image in img_files:
                full_path = os.path.join(path, image)
                if image.endswith(('.png', '.jpg', '.jpeg')):
                    try:
                        # Get filename without extension as key
                        key = os.path.splitext(image)[0]
                        surface_dict[key] = pygame.image.load(full_path).convert_alpha()
                    except pygame.error:
                        print(f'Failed to load image: {full_path}')
    except Exception as e:
        print(f'Error accessing path {path}: {str(e)}')

    return surface_dict

def load_pygame_image(name):
    """Load a single image with error handling."""
    try:
        return pygame.image.load(name).convert_alpha()
    except pygame.error:
        print(f'Failed to load image: {name}')
        # Create placeholder
        surf = pygame.Surface((32, 32))
        surf.fill((255, 0, 255))  # Magenta for visibility
        return surf