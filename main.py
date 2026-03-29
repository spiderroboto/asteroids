import sys
import pygame
import json

sys.path.insert(0, "src")
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    STATE_TITLE,
    STATE_GAME,
    STATE_SETTINGS,
    STATE_GAME_OVER,
    STATE_TUTORIAL,
)
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


# -----------------------------
# TITLE SCREEN
# -----------------------------
def title_screen(screen):
    clock = pygame.time.Clock()
    font_big = pygame.font.SysFont(None, 80)
    font_small = pygame.font.SysFont(None, 40)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return STATE_GAME
                if event.key == pygame.K_s:
                    return STATE_SETTINGS
                if event.key == pygame.K_t:
                    return STATE_TUTORIAL

        screen.fill("black")

        title = font_big.render("ASTEROIDS", True, "white")
        start = font_small.render("Press ENTER to Start", True, "white")
        settings = font_small.render("Press S for Settings", True, "white")
        tutorial = font_small.render("Press T for Tutorial", True, "white")

        screen.blit(title, (SCREEN_WIDTH / 2 - title.get_width() / 2, 200))
        screen.blit(start, (SCREEN_WIDTH / 2 - start.get_width() / 2, 350))
        screen.blit(settings, (SCREEN_WIDTH / 2 - settings.get_width() / 2, 400))
        screen.blit(tutorial, (SCREEN_WIDTH / 2 - tutorial.get_width() / 2, 450))

        pygame.display.flip()
        clock.tick(60)


# -----------------------------
# SAVE SETTINGS
# -----------------------------
def save_settings(settings):
    with open("settings.json", "w") as f:
        json.dump(settings, f, indent=4)


# -----------------------------
# SETTINGS SCREEN (EDITABLE)
# -----------------------------
def settings_screen(screen):
    clock = pygame.time.Clock()
    font_big = pygame.font.SysFont(None, 70)
    font_small = pygame.font.SysFont(None, 40)

    # Load current settings
    with open("settings.json", "r") as f:
        settings = json.load(f)

    options = [
        ("Player Speed", "player_speed"),
        ("Turn Speed", "player_turn_speed"),
        ("Shoot Cooldown", "player_shoot_cooldown"),
        ("Asteroid Size", "asteroid_min_radius"),
        ("Spawn Rate", "asteroid_spawn_rate"),
    ]

    index = 0  # which setting is selected

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    save_settings(settings)
                    return STATE_TITLE

                if event.key == pygame.K_UP:
                    index = (index - 1) % len(options)

                if event.key == pygame.K_DOWN:
                    index = (index + 1) % len(options)

                if event.key == pygame.K_LEFT:
                    key = options[index][1]
                    settings[key] = round(settings[key] - 1, 2)

                if event.key == pygame.K_RIGHT:
                    key = options[index][1]
                    settings[key] = round(settings[key] + 1, 2)

        screen.fill("black")

        title = font_big.render("SETTINGS", True, "white")
        screen.blit(title, (SCREEN_WIDTH / 2 - title.get_width() / 2, 100))

        # Draw each setting
        for i, (label, key) in enumerate(options):
            color = "yellow" if i == index else "white"
            text = font_small.render(f"{label}: {settings[key]}", True, color)
            screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2, 250 + i * 50))

        pygame.display.flip()
        clock.tick(60)


# -----------------------------
# GAME OVER SCREEN
# -----------------------------
def game_over_screen(screen):
    clock = pygame.time.Clock()
    font_big = pygame.font.SysFont(None, 80)
    font_small = pygame.font.SysFont(None, 40)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return STATE_GAME
                if event.key == pygame.K_ESCAPE:
                    return STATE_TITLE

        screen.fill("black")

        title = font_big.render("GAME OVER", True, "red")
        restart = font_small.render("Press ENTER to Restart", True, "white")
        menu = font_small.render("Press ESC for Main Menu", True, "white")

        screen.blit(title, (SCREEN_WIDTH / 2 - title.get_width() / 2, 200))
        screen.blit(restart, (SCREEN_WIDTH / 2 - restart.get_width() / 2, 350))
        screen.blit(menu, (SCREEN_WIDTH / 2 - menu.get_width() / 2, 400))

        pygame.display.flip()
        clock.tick(60)


# -----------------------------
# TUTORIAL SCREEN
# -----------------------------
def tutorial_screen(screen):
    clock = pygame.time.Clock()
    font_big = pygame.font.SysFont(None, 70)
    font_small = pygame.font.SysFont(None, 40)
    font_tiny = pygame.font.SysFont(None, 30)

    instructions = [
        "Welcome to Asteroids!",
        "",
        "Controls:",
        "WASD - Move and rotate your ship",
        "Space - Shoot",
        "",
        "Objective:",
        "Destroy all asteroids by shooting them.",
        "Large asteroids split into smaller ones.",
        "Avoid colliding with asteroids!",
        "",
        "Press ESC to return to menu",
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return STATE_TITLE

        screen.fill("black")

        title = font_big.render("TUTORIAL", True, "white")
        screen.blit(title, (SCREEN_WIDTH / 2 - title.get_width() / 2, 100))

        y = 200
        for line in instructions:
            if line == "":
                y += 20
            else:
                if "Controls:" in line or "Objective:" in line:
                    font = font_small
                    color = "yellow"
                elif "Press ESC" in line:
                    font = font_tiny
                    color = "gray"
                else:
                    font = font_tiny
                    color = "white"
                text = font.render(line, True, color)
                screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2, y))
                y += 40

        pygame.display.flip()
        clock.tick(60)


# -----------------------------
# GAMEPLAY LOOP
# -----------------------------
def run_game(screen):
    clock = pygame.time.Clock()

    # Sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Set containers
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)

    # Create objects
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    dt = 0
    running = True

    while running:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            player.shoot()

        updatable.update(dt)

        # Player vs asteroids
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                return STATE_GAME_OVER

        # Shots vs asteroids
        for asteroid in asteroids.copy():
            for shot in shots.copy():
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split()

        # Draw
        screen.fill("black")
        for obj in drawable:
            obj.draw(screen)
        pygame.display.flip()

        dt = clock.tick(60) / 1000

    return STATE_TITLE


# -----------------------------
# MAIN PROGRAM
# -----------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")

    state = STATE_TITLE

    while state is not None:
        if state == STATE_TITLE:
            state = title_screen(screen)
        elif state == STATE_SETTINGS:
            state = settings_screen(screen)
        elif state == STATE_GAME:
            state = run_game(screen)
        elif state == STATE_GAME_OVER:
            state = game_over_screen(screen)
        elif state == STATE_TUTORIAL:
            state = tutorial_screen(screen)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
