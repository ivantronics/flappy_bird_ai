import os
from image_scaler import image_scaler

BASE_IMG = image_scaler(os.path.join("images", "base.png"))


class Ground:
    GROUND_SPEED = 7
    GROUND_WIDTH = BASE_IMG.get_width()
    GROUND_IMAGE = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.GROUND_WIDTH

    def move(self):
        self.x1 -= self.GROUND_SPEED
        self.x2 -= self.GROUND_SPEED

        if self.x1 + self.GROUND_WIDTH < 0:
            self.x1 = self.x2 + self.GROUND_WIDTH

        if self.x2 + self.GROUND_WIDTH < 0:
            self.x2 = self.x1 + self.GROUND_WIDTH

    def draw(self, window):
        window.blit(self.GROUND_IMAGE, (self.x1, self.y))
        window.blit(self.GROUND_IMAGE, (self.x2, self.y))
