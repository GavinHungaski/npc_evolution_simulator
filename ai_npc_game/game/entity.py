import pygame
import math
from game import config, food, obstacle

class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.energy = 100
        self.color = config.BLUE
        self.size = 10
        self.velocity = [0, 0]
        self.brain = None
        self.nearest_food_dist = 0
        self.nearest_obstacle_dist = 0
        self.nearest_left_boundary = 0
        self.nearest_right_boundary = 0
        self.nearest_top_boundary = 0
        self.nearest_bottom_boundary = 0

    def update(self, world_objects):
        self.nearest_food_dist = float('inf')
        self.nearest_obstacle_dist = float('inf')
        
        for obj in world_objects:
            if obj is self:
                continue
            distance = math.dist((self.x, self.y), (obj.x, obj.y))
            if isinstance(obj, food.Food):
                if distance < self.size + obj.size:
                    self.energy += 20
                    obj.consumed = True
                if distance < self.nearest_food_dist:
                    self.nearest_food_dist = distance
            elif isinstance(obj, obstacle.Obstacle):
                if distance < self.size + obj.size:
                    self.energy -= 10
                if distance < self.nearest_obstacle_dist:
                    self.nearest_obstacle_dist = distance
            elif isinstance(obj, Entity):
                pass
        
        # Calculate distances to boundaries
        self.nearest_left_boundary = self.x
        self.nearest_right_boundary = config.WORLD_WIDTH - self.x
        self.nearest_top_boundary = self.y
        self.nearest_bottom_boundary = config.WORLD_HEIGHT - self.y

        # Check for boundary collisions
        if self.nearest_left_boundary <= self.size or self.nearest_right_boundary <= self.size:
            self.energy -= 10
            self.velocity[0] *= -1 # Simple bounce on collision
        if self.nearest_top_boundary <= self.size or self.nearest_bottom_boundary <= self.size:
            self.energy -= 10
            self.velocity[1] *= -1

        # Check if the entity has a brain
        if self.brain:
            # Get sensor data as inputs for the neural network
            inputs = [
                self.nearest_food_dist,
                self.nearest_obstacle_dist,
                self.energy,
                self.nearest_left_boundary,
                self.nearest_right_boundary,
                self.nearest_top_boundary,
                self.nearest_bottom_boundary
            ]
            
            # Get the neural network's outputs
            outputs = self.brain.predict(inputs)
            
            # Use the outputs to set the velocity
            speed = 2 # You can adjust this value
            self.velocity[0] = outputs[0] * speed
            self.velocity[1] = outputs[1] * speed

        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.clamp_pos()
        self.energy -= 0.1


    def clamp_pos(self):
        if self.x < 0:
            self.x = 0
        elif self.x > config.WORLD_WIDTH:
            self.x = config.WORLD_WIDTH

        if self.y < 0:
            self.y = 0
        elif self.y > config.WORLD_HEIGHT:
            self.y = config.WORLD_HEIGHT

    def draw(self, screen, camera):
        screen_pos = camera.apply((self.x, self.y))
        scaled_size = self.size * camera.zoom
        pygame.draw.circle(screen, self.color, screen_pos, scaled_size)