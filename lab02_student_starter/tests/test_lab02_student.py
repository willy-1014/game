import unittest
from star_sprout_lab.model import InputState, World


class StudentLab02Tests(unittest.TestCase):
    def test_student_diagonal_normalization_speed(self) -> None:
        """Verify that diagonal movement maintains correct normalized displacement."""
        world = World.create(seed=42)
        initial_x, initial_y = world.player.x, world.player.y

        # Move right + down diagonally for 0.05s
        inputs = InputState(right=True, down=True)
        world.step(inputs, dt=0.05)

        dx = world.player.x - initial_x
        dy = world.player.y - initial_y

        # Distance moved diagonally should equal player.speed * dt (300.0 * 0.05 = 15.0)
        distance = (dx**2 + dy**2) ** 0.5
        self.assertAlmostEqual(distance, world.player.speed * 0.05, places=5)

    def test_student_hud_boundary_clamping(self) -> None:
        """Verify that moving up clamps player position at the HUD boundary."""
        world = World.create(seed=42)
        inputs = InputState(up=True)

        # Move up repeatedly to hit top boundary
        for _ in range(50):
            world.step(inputs, dt=0.05)

        expected_min_y = world.config.hud_height + world.player.radius
        self.assertAlmostEqual(world.player.y, expected_min_y, places=5)


if __name__ == "__main__":
    unittest.main()