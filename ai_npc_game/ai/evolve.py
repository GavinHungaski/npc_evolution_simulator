import random
from game.game_world import GameWorld
from game import config
from game.entity import Entity
from ai.neural_network import NeuralNetwork

POPULATION_SIZE = 50
GENERATIONS = 100
MUTATION_RATE = 0.05

def evolve():
    # Step 1: Create the initial population
    population = []
    for _ in range(POPULATION_SIZE):
        brain = NeuralNetwork(
            input_nodes=7,
            hidden_nodes=4,
            output_nodes=2
        )
        entity = Entity(
            x = random.randint(0, config.WORLD_WIDTH),
            y = random.randint(0, config.WORLD_HEIGHT)
        )
        entity.brain = brain
        population.append(entity)

    for gen in range(GENERATIONS):
        print(f"--- Generation {gen} ---")
        
        # Step 2: Run the simulation for each generation
        world = GameWorld(initial_entities = population)
        world.run()

        # Step 3: Evaluate fitness
        population.sort(key=lambda ent: ent.energy, reverse=True)
        next_generation = []
        for _ in range(POPULATION_SIZE):
            parent1 = population[0]
            parent2 = population[1]

            child_brain = parent1.brain.crossover(parent2.brain)
            child_brain.mutate(MUTATION_RATE)

            new_entity = Entity(
                x = random.randint(0, config.WORLD_WIDTH),
                y = random.randint(0, config.WORLD_HEIGHT)
            )
            new_entity.brain = child_brain
            next_generation.append(new_entity)
        
        population = next_generation