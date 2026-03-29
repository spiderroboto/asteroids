import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT


class Shot(CircleShape):
    containers = ()

    def __init__(self, pos: pygame.Vector2):
        super().__init__(pos.x, pos.y, SHOT_RADIUS)
        self.velocity = pygame.Vector2(0, -1)

    def update(self, dt):
        self.position += self.velocity * dt

        # Remove if off-screen
        if (
            self.position.x < 0
            or self.position.x > SCREEN_WIDTH
            or self.position.y < 0
            or self.position.y > SCREEN_HEIGHT
        ):
            self.kill()

    def draw(self, screen):
        pygame.draw.circle(
            screen, "white", (int(self.position.x), int(self.position.y)), self.radius
        )
