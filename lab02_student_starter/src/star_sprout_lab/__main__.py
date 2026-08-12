"""Headless command-line smoke runner for the student starter."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence

from .model import InputState
from .state_model import initial_state, step


def simulate(seed: int, frames: int, dt: float | None) -> dict[str, object]:
    state = initial_state(seed=seed)
    controls = InputState()
    for _ in range(frames):
        state = step(state, controls, dt)
    return state.snapshot()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the StarSprout starter without opening a window."
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Accepted now and retained for the later Pygame entrypoint.",
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--frames", type=int, default=120)
    parser.add_argument(
        "--dt",
        type=float,
        default=None,
        help="Seconds per step; defaults to GameConfig.fixed_dt.",
    )
    parser.add_argument(
        "--assert-deterministic",
        action="store_true",
        help="Run the same simulation twice and compare snapshots.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.frames < 0:
        raise SystemExit("--frames must be zero or greater")

    first = simulate(args.seed, args.frames, args.dt)
    result: dict[str, object] = {"snapshot": first}

    if args.assert_deterministic:
        second = simulate(args.seed, args.frames, args.dt)
        reproducible = first == second
        result["deterministic"] = reproducible
        if not reproducible:
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            return 1

    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
