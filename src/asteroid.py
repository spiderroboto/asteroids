import pygame
import random
from logger import log_event
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS


class Asteroid(CircleShape):
    def __init__(self, x, y, radius, velocity=None):
        super().__init__(x, y, radius)
        self.velocity = velocity or pygame.Vector2(
            random.uniform(-100, 100), random.uniform(-100, 100)
        )

    def update(self, dt):
        self.position += self.velocity * dt
        self.wrap()

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            "gray",
            (int(self.position.x), int(self.position.y)),
            int(self.radius),
        )

    def split(self):
        # Destroy this asteroid
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return  # Small asteroid, no splitting

        # Log the split event
        log_event("asteroid_split")

        # Random split angle
        angle = random.uniform(20, 50)  # degrees

        # First split velocity
        vel1 = self.velocity.rotate(angle) * 1.2
        # Second split velocity
        vel2 = self.velocity.rotate(-angle) * 1.2

        # New radius for the smaller asteroids
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        # Spawn new asteroids
        Asteroid(self.position.x, self.position.y, new_radius, vel1)
        Asteroid(self.position.x, self.position.y, new_radius, vel2)
