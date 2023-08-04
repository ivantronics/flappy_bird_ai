import pygame
import os
import random
from image_scaler import image_scaler

# Assigning graphics
PIPE_IMG = image_scaler(os.path.join("images", "pipe.png"))


class Pipe:
    PIPE_GAP = 200  # Vertical gap between two pipes
    PIPE_HORIZONTAL_SPEED = 5  # How fast the bird is flying, i.e. how fast pipes are coming at the bird
    PIPE_TOP_IMAGE = pygame.transform.flip(PIPE_IMG,
                                           False,
                                           True)  # Flipping pipe image to create up-side down pipe

    PIPE_BOTTOM_IMAGE = PIPE_IMG
    PIPE_WIDTH = PIPE_IMG.get_width()

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG
        self.passed = False  # For collision detection
        self.set_height()  # Create random height of the gap between top and bottom pipes

    def set_height(self):
        # Setting up each set of pipes randomly
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP_IMAGE.get_height()
        self.bottom = self.height + self.PIPE_GAP

    def move(self):
        self.x -= self.PIPE_HORIZONTAL_SPEED

    def draw(self, window):
        window.blit(self.PIPE_TOP_IMAGE, (self.x, self.top))
        window.blit(self.PIPE_BOTTOM_IMAGE, (self.x, self.bottom))

    def collision(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP_IMAGE)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM_IMAGE)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        top_point = bird_mask.overlap(top_mask, top_offset)
        bottom_point = bird_mask.overlap(bottom_mask, bottom_offset)
        #ground_point = bird.y + bird.image.get_height() > WIN_HEIGHT - 112 * 2  # 112px is ground height, multiplied beacuse we scaled the image

        if top_point or bottom_point: #or ground_point:
            return True

        return False
