"""Public API for the intentionally incomplete StarSprout student starter."""

from .model import (
    DEFAULT_CONFIG,
    Bullet,
    Enemy,
    GameConfig,
    GameEvent,
    InputState,
    Phase,
    Player,
    World,
    circles_overlap,
    clamp,
)
from .state_model import GameState, initial_state, step

__all__ = [
    "DEFAULT_CONFIG",
    "Bullet",
    "Enemy",
    "GameConfig",
    "GameEvent",
    "GameState",
    "InputState",
    "Phase",
    "Player",
    "World",
    "circles_overlap",
    "clamp",
    "initial_state",
    "step",
]

__version__ = "0.1.0"
