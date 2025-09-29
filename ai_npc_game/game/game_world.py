import pygame
from game import config
from game.camera import Camera
from game.entity import Entity
from game.food import Food
from game.obstacle import Obstacle

class GameWorld:
    def __init__(self, initial_entities):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("AI NPC Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.camera = Camera()
        
        food1 = Food(500, 500)
        obstacle1 = Obstacle(1500, 1500)
        self.world_objects = [food1, obstacle1]
        for entity in initial_entities:
            self.world_objects.append(entity)


    def run(self):
        while self.running:   # Main Game loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.camera.listen_for_mouse_input(event)
            self.camera.listen_for_key_input()
            for obj in self.world_objects:
                if isinstance(obj, Entity):
                    obj.update(self.world_objects)
                else:
                    obj.update()
            self.world_objects = [obj for obj in self.world_objects if not getattr(obj, 'consumed', False)]
            self.screen.fill(config.WHITE)

            # Setup and render the world border
            world_rect_pos = self.camera.apply((0, 0))
            scaled_world_width = config.WORLD_WIDTH * self.camera.zoom
            scaled_world_height = config.WORLD_HEIGHT * self.camera.zoom
            border_rect = pygame.Rect(
                world_rect_pos[0],
                world_rect_pos[1],
                scaled_world_width,
                scaled_world_height
            )
            pygame.draw.rect(
                self.screen,
                config.BLACK,
                border_rect,
                width=3
            )

            # Render all world object relative to the camera
            for obj in self.world_objects:
                obj.draw(self.screen, self.camera)

            pygame.display.flip()  # refresh the screen
            self.clock.tick(60)    # tick at 60 fps
        pygame.quit()
