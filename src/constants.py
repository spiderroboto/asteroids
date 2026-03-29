import json

# Load editable settings
with open("settings.json", "r") as f:
    SETTINGS = json.load(f)

# -----------------------------
# SCREEN SETTINGS
# -----------------------------
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

LINE_WIDTH = 2

# -----------------------------
# PLAYER SETTINGS
# -----------------------------
PLAYER_RADIUS = 20
PLAYER_SPEED = SETTINGS["player_speed"]
PLAYER_TURN_SPEED = SETTINGS["player_turn_speed"]
PLAYER_SHOOT_COOLDOWN_SECONDS = SETTINGS["player_shoot_cooldown"]
PLAYER_SHOOT_SPEED = 500

# -----------------------------
# SHOT SETTINGS
# -----------------------------
SHOT_RADIUS = 5

# -----------------------------
# ASTEROID SETTINGS
# -----------------------------
ASTEROID_MIN_RADIUS = SETTINGS["asteroid_min_radius"]
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE_SECONDS = SETTINGS["asteroid_spawn_rate"]
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS

# -----------------------------
# GAME STATES
# -----------------------------
STATE_TITLE = 0
STATE_GAME = 1
STATE_SETTINGS = 2
STATE_GAME_OVER = 3
STATE_TUTORIAL = 4
