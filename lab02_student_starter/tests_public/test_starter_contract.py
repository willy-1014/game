"""Small public checks for starter infrastructure, not Lab solutions."""

from __future__ import annotations

import json
import math
import unittest

from star_sprout_lab import GameConfig, InputState, Phase, initial_state, step


class StarterContractTests(unittest.TestCase):
    def test_initial_state_has_stable_shape(self) -> None:
        state = initial_state(seed=7)
        self.assertEqual(state.seed, 7)
        self.assertIs(state.phase, Phase.PLAYING)
        self.assertEqual(state.tick, 0)
        self.assertEqual(state.bullets, [])
        self.assertEqual(state.enemies, [])

    def test_functional_step_does_not_mutate_input(self) -> None:
        before = initial_state(seed=8)
        after = step(before, InputState(), 0.01)
        self.assertEqual(before.tick, 0)
        self.assertEqual(before.elapsed, 0.0)
        self.assertEqual(after.tick, 1)
        self.assertAlmostEqual(after.elapsed, 0.01)

    def test_same_seed_and_inputs_are_reproducible(self) -> None:
        first = initial_state(seed=9)
        second = initial_state(seed=9)
        inputs = [InputState(), InputState(left=True), InputState(fire=True)]
        for controls in inputs:
            first = step(first, controls)
            second = step(second, controls)
        self.assertEqual(first.snapshot(), second.snapshot())

    def test_pause_transition_freezes_simulation_time(self) -> None:
        state = initial_state(seed=10)
        state = step(state, InputState(pause=True))
        self.assertIs(state.phase, Phase.PAUSED)
        frozen = state.snapshot()
        state = step(state, InputState(fire=True), 0.05)
        self.assertEqual(state.snapshot(), frozen)
        state = step(state, InputState(pause=True))
        self.assertIs(state.phase, Phase.PLAYING)

    def test_dt_is_nonnegative_and_bounded(self) -> None:
        state = initial_state(seed=11)
        unchanged = step(state, InputState(), -1.0)
        self.assertEqual(unchanged.elapsed, 0.0)
        advanced = step(state, InputState(), 999.0)
        self.assertEqual(advanced.elapsed, state.config.max_dt)

    def test_non_finite_dt_is_rejected(self) -> None:
        state = initial_state(seed=12)
        with self.assertRaises(ValueError):
            step(state, InputState(), math.inf)

    def test_terminal_state_can_restart_cleanly(self) -> None:
        config = GameConfig(round_seconds=0.05, max_dt=0.05)
        state = initial_state(seed=13, config=config)
        state = step(state, InputState(), 0.05)
        self.assertIs(state.phase, Phase.WON)
        state.score = 999
        state = step(state, InputState(restart=True))
        self.assertIs(state.phase, Phase.PLAYING)
        self.assertEqual(state.score, 0)
        self.assertEqual(state.tick, 0)

    def test_snapshot_is_json_serialisable(self) -> None:
        state = step(initial_state(seed=14), InputState())
        encoded = json.dumps(state.snapshot(), sort_keys=True)
        self.assertIn('"phase": "playing"', encoded)


if __name__ == "__main__":
    unittest.main()
