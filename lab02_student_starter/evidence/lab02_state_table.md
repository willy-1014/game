# Lab 02 State Table

Complete the **prediction** columns before running the scenario.

Configuration: `player_speed=100.0`, `max_dt=0.05`, initial player `(480, 504)`.

| Step | Input and `dt` | Predicted tick / elapsed / x / y | Calculation | Observed result | Difference and correction |
|---:|---|---|---|---|---|
| 1 | right, 0.05 | |485,504| |dx=1, dy=0; x = 480 + 100*0.05 = 485 |
| 2 | right + up, 0.05 | |488.53,500.46| |dx=0.7,dy=-0.7;x=3.53,y=3.53|
| 3 | left + right, 0.05 | |488.53,500.46| |dx = -1 + 1 = 0, dy = 0|
| 4 | neutral, 0.20 | |488.53,500.46| |raw dt 0.20 bounded to 0.05; elapsed=0.05;no input (dx=0, dy=0)|

Explain why diagonal input must be normalized:
Without diagonal normalization, moving diagonally combines the full speed along both the X and Y axes, resulting in a total speed vector magnitude of sqrt(1^2 + 1^2) = sqrt(2) ≈ 1.414 times faster than cardinal movement. Normalizing scales the diagonal vector back to a magnitude of 1.0, ensuring fair and uniform movement speed in all directions.