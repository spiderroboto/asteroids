import pygame
from circleshape import CircleShape
from constants import (
    LINE_WIDTH,
    PLAYER_RADIUS,
    PLAYER_TURN_SPEED,
    PLAYER_SPEED,
    PLAYER_SHOOT_SPEED,
    SHOT_RADIUS,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
)
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cooldown = 0.0  # seconds

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def triangle(self):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        right = pygame.Vector2(1, 0).rotate(self.rotation) * (self.radius / 1.5)

        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right

        return [a, b, c]

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()

        # rotation
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)

        # movement
        if keys[pygame.K_w]:
            self.move(-dt)
        if keys[pygame.K_s]:
            self.move(dt)

        # wrap around screen
        self.wrap()

        # cooldown timer (clamped)
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt
            if self.shoot_cooldown < 0:
                self.shoot_cooldown = 0

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        movement = rotated_vector * PLAYER_SPEED * dt
        self.position += movement

    def shoot(self):
        # block shooting if still cooling down
        if self.shoot_cooldown > 0:
            return

        # reset cooldown
        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS

        # create shot
        shot = Shot(self.position)
        shot.velocity = pygame.Vector2(0, -1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
