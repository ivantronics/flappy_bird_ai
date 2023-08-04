import pygame


def image_scaler(image_path):
    # Easy scale change
    return pygame.transform.scale2x(pygame.image.load(image_path))
