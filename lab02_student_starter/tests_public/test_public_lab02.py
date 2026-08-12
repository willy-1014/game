"""Representative public checks for the published Lab 02 contract."""

import math
import unittest

from star_sprout_lab import GameConfig, InputState, World, initial_state, step


class PublicLab02Tests(unittest.TestCase):
    def test_single_axis_movement_uses_speed_and_bounded_dt(self) -> None:
        config = GameConfig(player_speed=100.0, max_dt=0.05)
        before = initial_state(seed=7, config=config)
        after = step(before, InputState(right=True), 0.05)
        self.assertAlmostEqual(after.player.x - before.player.x, 5.0)

    def test_pure_and_in_place_entry_points_agree(self) -> None:
        controls = InputState(left=True, up=True, precision=True)
        before = initial_state(seed=8)
        pure_after = step(before, controls, 0.02)
        in_place = World.create(seed=8)
        in_place.step(controls, 0.02)
        self.assertEqual(pure_after.snapshot(), in_place.snapshot())
        self.assertEqual(before.tick, 0)

    def test_diagonal_speed_is_normalized(self) -> None:
        config = GameConfig(player_speed=100.0)
        axis_before = initial_state(seed=9, config=config)
        diagonal_before = initial_state(seed=9, config=config)
        axis = step(axis_before, InputState(right=True), 0.01)
        diagonal = step(diagonal_before, InputState(right=True, up=True), 0.01)
        axis_distance = math.hypot(axis.player.x - axis_before.player.x, axis.player.y - axis_before.player.y)
        diagonal_distance = math.hypot(diagonal.player.x - diagonal_before.player.x, diagonal.player.y - diagonal_before.player.y)
        self.assertAlmostEqual(axis_distance, 1.0)
        self.assertAlmostEqual(axis_distance, diagonal_distance)

    def test_opposite_directions_cancel(self) -> None:
        before = initial_state(seed=10)
        after = step(before, InputState(left=True, right=True, up=True, down=True), 0.05)
        self.assertEqual((after.player.x, after.player.y), (before.player.x, before.player.y))

    def test_precision_is_half_speed(self) -> None:
        before = initial_state(seed=11)
        normal = step(before, InputState(left=True), 0.01)
        precise = step(before, InputState(left=True, precision=True), 0.01)
        self.assertGreater(before.player.x - precise.player.x, 0.0)
        self.assertAlmostEqual(before.player.x - precise.player.x, (before.player.x - normal.player.x) * 0.5)

    def test_player_center_stays_in_playfield(self) -> None:
        config = GameConfig(width=100, height=100, hud_height=20, player_radius=10, player_speed=1000.0)
        state = initial_state(seed=12, config=config)
        state.player.x = state.player.radius + 1.0
        state.player.y = config.hud_height + state.player.radius + 1.0
        state.step(InputState(left=True, up=True), 0.05)
        self.assertEqual(state.player.x, state.player.radius)
        self.assertEqual(state.player.y, config.hud_height + state.player.radius)
        for _ in range(4):
            state.step(InputState(right=True, down=True), 0.05)
        self.assertEqual(state.player.x, config.width - state.player.radius)
        self.assertEqual(state.player.y, config.height - state.player.radius)

    def test_zero_negative_and_nonfinite_dt(self) -> None:
        before = initial_state(seed=13)
        self.assertEqual(step(before, InputState(right=True), 0.0).snapshot(), before.snapshot())
        self.assertEqual(step(before, InputState(right=True), -1.0).snapshot(), before.snapshot())
        for invalid in (math.nan, math.inf, -math.inf):
            with self.assertRaises(ValueError):
                step(before, InputState(), invalid)


if __name__ == "__main__":
    unittest.main()
