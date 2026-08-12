# Lab 02 Public Test Contract

Executable tests are distributed in the starter's `tests_public/` folder. This document is the stable behaviour contract, not a solution.

## Import contract

```python
from star_sprout_lab import GameConfig, InputState, World, initial_state, step
```

## Published behaviour

1. `initial_state(seed=7)` starts in `playing` with zero tick, elapsed time, score, and entity counts.
2. Initial snapshots match for the same config and seed.
3. `step(before, InputState(right=True), 0.05)` returns a new `World`; `before.snapshot()` remains unchanged.
4. The pure facade and `World.step()` produce the same snapshot for the same input.
5. Single-axis travel distance is `player.speed * bounded_dt`.
6. Diagonal input is normalized, so two active axes do not increase total speed.
7. `left=True, right=True` produces no horizontal motion; the vertical pair behaves the same way.
8. `precision=True` produces 50% of normal displacement.
9. The player's center remains in the playfield and outside the HUD.
10. `dt <= 0` does not change tick, elapsed time, or position; values above `max_dt` are clamped.
11. `NaN` or infinite `dt` raises `ValueError`.
12. `json.dumps(state.snapshot())` succeeds.

Tests may use different valid configs, seeds, direction sequences, and boundary positions. Do not hard-code the default dimensions or seed 42.

## Public-test layout

```text
tests_public/
`-- test_public_lab02.py      # Distributed by the course; do not modify
```

This contract is packaged at the repository root as `public_test_contract.md`. The executable test is included in the student pack and must not be modified. Add independent checks in `tests/test_lab02_student.py`; do not use an unconditional placeholder test.
