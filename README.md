# Asteroids Game

A classic Asteroids game implemented in Python using Pygame.

## Features

- Player ship that can rotate and move
- Asteroids that spawn and move around the screen
- Shooting mechanics to destroy asteroids
- Asteroids split into smaller pieces when shot
- Screen wrapping for all objects
- Settings screen to adjust game parameters
- Logging of game state and events
- Game over screen with restart option

## Controls

- **WASD**: Move and rotate the ship
- **Space**: Shoot
- **Enter**: Start game / Restart
- **S**: Open settings
- **T**: Open tutorial
- **Escape**: Return to title / Main menu

In settings:
- **Up/Down**: Navigate options
- **Left/Right**: Adjust values
- **Escape**: Save and return to title

## Installation

1. Ensure Python 3.13+ is installed.
2. Install dependencies: `pip install -r requirements.txt` or use uv: `uv sync`
3. Run the game: `python main.py`

## Project Structure

- `src/`: Source code
  - `main.py`: Main game loop and screens
  - `player.py`: Player ship class
  - `asteroid.py`: Asteroid class
  - `shot.py`: Shot class
  - `circleshape.py`: Base class for circular objects
  - `asteroidfield.py`: Manages asteroid spawning
  - `constants.py`: Game constants and settings loading
  - `logger.py`: Logging functionality
- `settings.json`: Editable game settings
- `game_state.jsonl`: Logged game state (ignored in git)
- `game_events.jsonl`: Logged events (ignored in git)

## Development

The game uses Pygame for graphics and input handling. Objects wrap around the screen edges. Asteroids spawn at random edges and move in random directions.