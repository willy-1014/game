"""Pure domain model for the StarSprout Shooter student starter.

This module must stay importable without Pygame.  The starter deliberately
implements only the simulation clock and lifecycle states.  Lab work adds
movement, shooting, spawning, collision, and cleanup behind the same API.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import math
import random
from typing import Final


class Phase(str, Enum):
    """Top-level game lifecycle."""

    PLAYING = "playing"
    PAUSED = "paused"
    WON = "won"
    GAME_OVER = "game_over"


@dataclass(frozen=True, slots=True)
class GameConfig:
    """Tunable rules kept outside presentation code."""

    width: int = 960
    height: int = 540
    hud_height: int = 60
    fixed_dt: float = 1.0 / 60.0
    max_dt: float = 0.05
    round_seconds: float = 60.0
    player_speed: float = 300.0
    player_radius: float = 16.0
    bullet_speed: float = 640.0
    fire_cooldown: float = 0.15
    spawn_interval: float = 0.80
    max_bullets: int = 72
    max_enemies: int = 42

    def __post_init__(self) -> None:
        numeric_positive = {
            "width": self.width,
            "height": self.height,
            "fixed_dt": self.fixed_dt,
            "max_dt": self.max_dt,
            "round_seconds": self.round_seconds,
            "player_radius": self.player_radius,
        }
        for name, value in numeric_positive.items():
            if value <= 0:
                raise ValueError(f"{name} must be positive")
        if not 0 <= self.hud_height < self.height:
            raise ValueError("hud_height must be inside the window")
        if self.max_bullets < 0 or self.max_enemies < 0:
            raise ValueError("entity limits cannot be negative")


DEFAULT_CONFIG: Final = GameConfig()


@dataclass(frozen=True, slots=True)
class InputState:
    """Device-independent controls for exactly one simulation step."""

    left: bool = False
    right: bool = False
    up: bool = False
    down: bool = False
    fire: bool = False
    precision: bool = False
    pause: bool = False
    restart: bool = False


@dataclass(slots=True)
class Player:
    x: float
    y: float
    speed: float
    radius: float
    lives: int = 3
    max_lives: int = 3
    cooldown_left: float = 0.0
    invulnerable_left: float = 0.0


@dataclass(slots=True)
class Bullet:
    bullet_id: int
    x: float
    y: float
    vy: float
    radius: float = 5.0


@dataclass(slots=True)
class Enemy:
    enemy_id: int
    kind: str
    x: float
    y: float
    vx: float
    vy: float
    radius: float
    hp: int
    score_value: int


@dataclass(frozen=True, slots=True)
class GameEvent:
    kind: str
    entity_id: int | None = None
    value: int = 0


def clamp(value: float, lower: float, upper: float) -> float:
    """Return ``value`` constrained to the inclusive interval.

    TODO(Lab 04): define invalid-interval behaviour and implement the boundary
    cases before connecting this helper to player movement.
    """

    raise NotImplementedError("TODO(Lab 04): implement clamp")


def circles_overlap(
    ax: float,
    ay: float,
    a_radius: float,
    bx: float,
    by: float,
    b_radius: float,
) -> bool:
    """Return whether two circles touch or overlap.

    TODO(Lab 04): implement from the written geometric invariant.  Decide in
    the Lab specification whether touching at exactly one point is a hit.
    """

    raise NotImplementedError("TODO(Lab 04): implement circles_overlap")


@dataclass(slots=True)
class World:
    """All authoritative game state; never stores a Pygame object."""

    config: GameConfig
    seed: int
    phase: Phase
    tick: int
    elapsed: float
    score: int
    player: Player
    bullets: list[Bullet]
    enemies: list[Enemy]
    events: list[GameEvent]
    spawn_timer: float
    next_bullet_id: int
    next_enemy_id: int
    _rng: random.Random = field(repr=False, compare=False)

    @classmethod
    def create(
        cls,
        seed: int = 42,
        config: GameConfig | None = None,
    ) -> "World":
        rules = DEFAULT_CONFIG if config is None else config
        integer_seed = int(seed)
        return cls(
            config=rules,
            seed=integer_seed,
            phase=Phase.PLAYING,
            tick=0,
            elapsed=0.0,
            score=0,
            player=Player(
                x=rules.width / 2.0,
                y=rules.height - rules.player_radius - 20.0,
                speed=rules.player_speed,
                radius=rules.player_radius,
            ),
            bullets=[],
            enemies=[],
            events=[],
            spawn_timer=rules.spawn_interval,
            next_bullet_id=1,
            next_enemy_id=1,
            _rng=random.Random(integer_seed),
        )

    @property
    def remaining(self) -> float:
        return max(0.0, self.config.round_seconds - self.elapsed)

    def reset(self, seed: int | None = None) -> None:
        """Restore every gameplay field while preserving the config."""

        replacement = World.create(
            self.seed if seed is None else int(seed),
            self.config,
        )
        for name in (
            "seed",
            "phase",
            "tick",
            "elapsed",
            "score",
            "player",
            "bullets",
            "enemies",
            "events",
            "spawn_timer",
            "next_bullet_id",
            "next_enemy_id",
            "_rng",
        ):
            setattr(self, name, getattr(replacement, name))

    def toggle_pause(self) -> Phase:
        if self.phase is Phase.PLAYING:
            self.phase = Phase.PAUSED
        elif self.phase is Phase.PAUSED:
            self.phase = Phase.PLAYING
        return self.phase

    def step(self, controls: InputState, dt: float | None = None) -> None:
        """Advance one bounded step in place.

        The baseline handles only lifecycle and time.  Labs 02–04 extend this
        method through small helpers; presentation code must not be added here.
        """

        self.events.clear()

        if controls.restart and self.phase in (Phase.WON, Phase.GAME_OVER):
            self.reset()
            self.events.append(GameEvent("restart"))
            return

        if controls.pause and self.phase in (Phase.PLAYING, Phase.PAUSED):
            phase = self.toggle_pause()
            self.events.append(
                GameEvent("pause" if phase is Phase.PAUSED else "resume")
            )
            return

        if self.phase is not Phase.PLAYING:
            return

        bounded_dt = self._bounded_dt(self.config.fixed_dt if dt is None else dt)
        if bounded_dt == 0.0:
            return

        self.tick += 1
        self.elapsed = min(self.config.round_seconds, self.elapsed + bounded_dt)

        # TODO(Lab 02): update and clamp player movement using InputState.
        dx = (1.0 if controls.right else 0.0) - (1.0 if controls.left else 0.0)
        dy = (1.0 if controls.down else 0.0) - (1.0 if controls.up else 0.0)

        length = math.hypot(dx, dy)
        if length > 0.0:
            dx /= length
            dy /= length

            # Precision movement halves the effective speed
            speed = self.player.speed * 0.5 if controls.precision else self.player.speed

            self.player.x += dx * speed * bounded_dt
            self.player.y += dy * speed * bounded_dt

            # Clamp player inside the playfield bounds (taking HUD height and radius into account)
            self.player.x = max(
                self.player.radius,
                min(self.player.x, self.config.width - self.player.radius),
            )
            self.player.y = max(
                self.config.hud_height + self.player.radius,
                min(self.player.y, self.config.height - self.player.radius),
            )
        # TODO(Lab 03): update firing, spawning, movement, and object cleanup.
        # TODO(Lab 04): resolve bullet/enemy and enemy/player collisions once.

        if self.elapsed >= self.config.round_seconds:
            self.phase = Phase.WON
            self.events.append(GameEvent("victory", value=self.score))

        self.assert_invariants()

    def _bounded_dt(self, dt: float) -> float:
        value = float(dt)
        if not math.isfinite(value):
            raise ValueError("dt must be finite")
        return max(0.0, min(value, self.config.max_dt))

    def assert_invariants(self) -> None:
        """Fail fast when model state cannot represent a valid game."""

        if not 0.0 <= self.elapsed <= self.config.round_seconds:
            raise AssertionError("elapsed is outside the round")
        if not 0 <= self.player.lives <= self.player.max_lives:
            raise AssertionError("player lives are invalid")
        bullet_ids = [bullet.bullet_id for bullet in self.bullets]
        enemy_ids = [enemy.enemy_id for enemy in self.enemies]
        if len(bullet_ids) != len(set(bullet_ids)):
            raise AssertionError("bullet IDs must be unique")
        if len(enemy_ids) != len(set(enemy_ids)):
            raise AssertionError("enemy IDs must be unique")

    def snapshot(self) -> dict[str, object]:
        """Return a compact JSON-safe summary for tests and CI evidence."""

        return {
            "seed": self.seed,
            "phase": self.phase.value,
            "tick": self.tick,
            "elapsed": round(self.elapsed, 6),
            "remaining": round(self.remaining, 6),
            "score": self.score,
            "lives": self.player.lives,
            "player": [round(self.player.x, 3), round(self.player.y, 3)],
            "bullets": len(self.bullets),
            "enemies": len(self.enemies),
        }
