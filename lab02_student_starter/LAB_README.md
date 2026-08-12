# Lab 02 - Deterministic State Model

> Course block: D1-B2, 13:00-16:00  
> Implementation timebox: 135 minutes  
> AI level: **L0 Human-only**  
> Student pack: `lab02_student_starter.zip` (self-contained, intentionally incomplete)

## Scenario

An interactive game updates many times per second. If its rules depend directly on the keyboard, display, or uncontrolled time, failures become difficult to reproduce. In this Lab, you will turn one frame of input into an explicit state transition so that the same seed, input sequence, and `dt` always produce the same snapshot.

## Learning outcomes

You will be able to:

1. Represent game state with dataclasses and collections.
2. Distinguish a pure facade from an in-place update and explain when each is useful.
3. Update position using delta time while handling opposite directions and normalized diagonal movement.
4. Verify repeatability with a fixed seed and input sequence.
5. Test the domain model without opening Pygame.

## Stable public interface

```python
from star_sprout_lab import GameConfig, InputState, World, initial_state, step
```

- `initial_state(seed=42, config=None) -> World`
- `step(state, controls=None, dt=None) -> World`: returns a new `World` without mutating `state`.
- `World.create(seed=42, config=None) -> World`
- `World.step(controls, dt=None) -> None`: equivalent in-place update entry point.
- `World.snapshot() -> dict[str, object]`: returns a JSON-serializable observation.

## Required deliverables

```text
evidence/lab02_state_table.md
evidence/lab02_replay.txt
tests/test_lab02_student.py
src/star_sprout_lab/model.py       # Modify only the Lab 02 TODO
```

## Procedure

### 1. Establish the baseline (15 minutes)

From the extracted student pack, first select and verify an accepted Python 3.11–3.13 interpreter. Only then create and activate `.venv`:

```bash
python --version
python -c "import sys; raise SystemExit(0 if (3, 11) <= sys.version_info[:2] < (3, 14) else 1)"
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# PowerShell:   .venv\Scripts\Activate.ps1
python -m pip install -e '.[test]'
python -m unittest discover -s tests_public -p 'test_starter_contract.py' -v
python -m unittest discover -s tests_public -v
python -m star_sprout_lab --headless --seed 42 --frames 120 --assert-deterministic
```

The infrastructure-only command must pass 8 tests. The full discovery command must report `Ran 15 tests` and the expected red baseline `FAILED (failures=4)` until you complete Lab 02. Commit only after confirming this exact expected-red baseline; do not edit `tests_public/`.

If package installation is unavailable, the standard-library-only Day 1 fallback remains runnable without an editable install:

```bash
# macOS/Linux
PYTHONPATH=src python -m unittest discover -s tests_public -v
PYTHONPATH=src python -m star_sprout_lab --headless --seed 42 --frames 120 --assert-deterministic

# PowerShell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests_public -v
python -m star_sprout_lab --headless --seed 42 --frames 120 --assert-deterministic
```

### 2. Predict the state transition (20 minutes)

Assume `GameConfig(player_speed=100.0, max_dt=0.05)` and an initial player position of `(480, 504)`. Before running code, predict `tick`, `elapsed`, `x`, and `y` after each step:

1. `right=True, dt=0.05`
2. `right=True, up=True, dt=0.05`
3. `left=True, right=True, dt=0.05`
4. neutral input, `dt=0.20`

Normalize diagonal movement. Opposite directions cancel on that axis, and `dt` cannot exceed `max_dt`. Record the prediction, actual result, and any difference in `evidence/lab02_state_table.md`.

### 3. Implement the player transition (50 minutes)

Complete only `TODO(Lab 02)`:

- Horizontal intent is `right - left`; vertical intent is `down - up`.
- Normalize any non-zero vector with its Euclidean length.
- `precision=True` uses 50% of normal speed.
- Displacement is normalized direction x speed x bounded `dt`.
- Keep the player's center inside these inclusive bounds:
  - `radius <= x <= width - radius`
  - `hud_height + radius <= y <= height - radius`
- Use `min` and `max` for now. The reusable `clamp()` function is reserved for Lab 04.
- `dt <= 0` does not advance tick, time, or position; `dt > max_dt` advances by only `max_dt`.
- `NaN`, `+inf`, and `-inf` raise `ValueError`.

The model must not import `pygame`, read a keyboard, call a clock, or draw anything.

### 4. Add tests and replay evidence (35 minutes)

Add at least two focused tests to `tests/test_lab02_student.py`. Recommended targets include pure-state isolation, diagonal normalization, playfield bounds, and replay equality.

Run the same fixed `InputState` sequence twice. Save both snapshots and the equality result as text in `evidence/lab02_replay.txt`.

### 5. Explain and commit (15 minutes)

```bash
python -m unittest discover -s tests_public -v
python -m unittest discover -s tests -v
python -m star_sprout_lab --headless --seed 42 --frames 120 --assert-deterministic
git diff --check
```

Suggested commit: `lab02: implement deterministic player state`

## Acceptance criteria

- Pure `step()` returns a different object and does not mutate its input.
- The in-place and pure-facade forms have equivalent observable snapshots.
- Movement, precision, diagonal normalization, and playfield boundaries match the contract.
- Zero, negative, oversized, and non-finite `dt` values match the contract.
- Replaying the same seed, inputs, and `dt` values produces identical results.
- At least two student-written logic tests pass, and the pure model does not require Pygame.
- You can explain why deterministic behaviour does not mean every seed produces the same result.

Review [rubric.md](rubric.md), [submission_checklist.md](submission_checklist.md), and the [public test contract](public_test_contract.md) before submitting.
