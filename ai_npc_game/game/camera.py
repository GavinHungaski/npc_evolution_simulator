import pygame
from game import config

class Camera:
    def __init__(self, width = 0, height = 0, speed = 5):
        self.x = width
        self.y = height
        self.move_speed = speed
        self.is_dragging = False
        self.last_mouse_pos = (0, 0)
        self.zoom = 1.0  # initial zoom
        self.zoom_speed = 0.1

    def listen_for_key_input(self):
        keys = pygame.key.get_pressed()
        speed = self.move_speed / self.zoom
        if keys[pygame.K_LEFT]:
            self.x -= speed
        if keys[pygame.K_RIGHT]:
            self.x += speed
        if keys[pygame.K_UP]:
            self.y -= speed
        if keys[pygame.K_DOWN]:
            self.y += speed
        self.clamp_camera_position()

    def listen_for_mouse_input(self, event):
        old_zoom = self.zoom
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:   # LMB
                self.is_dragging = True
                self.last_mouse_pos = event.pos
            elif event.button == 4:  # scroll up (zoom in)
                self.zoom += self.zoom_speed
            elif event.button == 5:  # scroll down (zoom out)
                self.zoom -= self.zoom_speed
                if self.zoom < 0.1:     # limit zoom
                    self.zoom = 0.1
        if self.zoom != old_zoom:
            self.zoom_to_center(old_zoom)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.is_dragging = False
        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            current_mouse_pos = event.pos
            dx = current_mouse_pos[0] - self.last_mouse_pos[0]
            dy = current_mouse_pos[1] - self.last_mouse_pos[1]
            self.x -= dx / self.zoom
            self.y -= dy / self.zoom
            self.last_mouse_pos = current_mouse_pos
        self.clamp_camera_position()

    def zoom_to_center(self, old_zoom):
        center_x = self.x + config.SCREEN_WIDTH / (2 * old_zoom)
        center_y = self.y + config.SCREEN_HEIGHT / (2 * old_zoom)
        self.x = center_x - config.SCREEN_WIDTH / (2 * self.zoom)
        self.y = center_y - config.SCREEN_HEIGHT / (2 * self.zoom)

    def clamp_camera_position(self):
        camera_left = self.x
        camera_top = self.y
        camera_right = self.x + config.SCREEN_WIDTH / self.zoom
        camera_bottom = self.y + config.SCREEN_HEIGHT / self.zoom
        if camera_left < 0:
            self.x = 0
        elif camera_right > config.WORLD_WIDTH:
            self.x = config.WORLD_WIDTH - config.SCREEN_WIDTH / self.zoom
            if self.x < 0:
                self.x = 0
        if camera_top < 0:
            self.y = 0
        elif camera_bottom > config.WORLD_HEIGHT:
            self.y = config.WORLD_HEIGHT - config.SCREEN_HEIGHT / self.zoom
            if self.y < 0:
                self.y = 0

    def apply(self, world_pos):
        scaled_x = (world_pos[0] - self.x) * self.zoom
        scaled_y = (world_pos[1] - self.y) * self.zoom
        return (scaled_x, scaled_y)