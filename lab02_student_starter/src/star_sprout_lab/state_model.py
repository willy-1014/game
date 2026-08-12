"""Functional facade for deterministic notebook examples and replay tests."""

from __future__ import annotations

from copy import deepcopy

from .model import GameConfig, InputState, World


GameState = World


def initial_state(
    seed: int = 42,
    config: GameConfig | None = None,
) -> GameState:
    """Create the first state for a deterministic simulation."""

    return World.create(seed=seed, config=config)


def step(
    state: GameState,
    controls: InputState | None = None,
    dt: float | None = None,
) -> GameState:
    """Return the next state without mutating ``state``.

    The Pygame loop may call ``World.step`` for performance.  Notebook and
    reasoning exercises use this facade so before/after values remain visible.
    """

    next_state = deepcopy(state)
    next_state.step(InputState() if controls is None else controls, dt)
    return next_state
