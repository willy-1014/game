# Lab 02 Rubric - 100 points

| Dimension | Points | Full evidence |
|---|---:|---|
| Predict-first state reasoning | 15 | Four before/after rows, calculations, and a post-run comparison |
| Pure transition contract | 20 | The facade returns a new object, preserves its input, and matches the in-place observable result |
| Movement correctness | 25 | Direction cancellation, diagonal normalization, precision, delta time, and bounds are correct |
| Time and error boundaries | 15 | Zero/negative values do not advance; oversized values are clamped; non-finite values are rejected |
| Deterministic tests and evidence | 15 | At least two focused tests and a reproducible fixed-sequence replay |
| Code, Git, and explanation | 10 | Only required TODOs changed; names are clear; commit is reviewable; explain-back is accurate |

## Scoring constraints

- If the model imports Pygame or depends on a physical keyboard or clock, the total is capped at 60.
- If the pure facade mutates its input, Pure transition contract is capped at 5/20.
- Missing state-table or replay text earns 0 for the corresponding dimension.
- An L0 violation is handled under the Syllabus and academic-integrity policy.

