import pygame
from game import config


class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = config.GREEN
        self.size = 10
        self.consumed = False


    def update(self):
        pass


    def draw(self, screen, camera):
        screen_pos = camera.apply((self.x, self.y))
        scaled_size = self.size * camera.zoom
        pygame.draw.circle(screen, self.color, screen_pos, scaled_size)