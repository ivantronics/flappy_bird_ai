import pygame
import os
from itertools import cycle
from image_scaler import image_scaler

# Assigning graphics
BIRD_IMG = [
    image_scaler(os.path.join("images", "bird1.png")),
    image_scaler(os.path.join("images", "bird2.png")),
    image_scaler(os.path.join("images", "bird3.png")),
    image_scaler(os.path.join("images", "bird2.png")),  # bird2.png is needed for smooth animation transition
]


class Bird:
    ANIMATION_IMAGE = BIRD_IMG
    MAX_ROTATION = 25
    ROTATION_VELOCITY = 10
    ANIMATION_TIME = 5
    ANIMATION_CYCLE = cycle((range(1, 20)))

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.image_count = 0
        self.image = self.ANIMATION_IMAGE[0]

    def jump(self):
        self.velocity = -5.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        # Counting how fast and in what direction bird is going
        displacement = self.velocity * self.tick_count + 1 * self.tick_count ** 2 // 1.3

        if displacement >= 16:
            displacement = 16  # Speed limit

        if displacement < 0:
            displacement -= 4  # Slowing down upwards momentum

        self.y = self.y + displacement  # New coordinates after movement

        if displacement < 0:  # Rotation logic for going up/down
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt = max(self.tilt - self.ROTATION_VELOCITY, -90)

    def draw(self, window):
        self.image_count = next(self.ANIMATION_CYCLE)
        self.image = self.ANIMATION_IMAGE[(
                self.image_count // self.ANIMATION_TIME % 4)]

        if self.tilt <= -80:
            self.image = self.ANIMATION_IMAGE[1]
            self.image_count = self.ANIMATION_TIME * 2

        # Rotating the bird image around it's center (not top left corner)
        # and putting it on the screen
        rotated_image = pygame.transform.rotate(self.image, self.tilt)
        new_rectangle = rotated_image.get_rect(
            center=self.image.get_rect(topleft=(self.x, self.y)).center)
        window.blit(rotated_image, new_rectangle.topleft)

    def get_mask(self):
        # Collision detection tool
        return pygame.mask.from_surface(self.image)
