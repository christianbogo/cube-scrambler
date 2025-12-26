## Cube Scrambler (3x3 random-state)

Generates legitimate WCA-style random-state scrambles by:

- generating a uniformly random, solvable cube state in cubie coordinates
- solving it using Kociemba's 2-phase algorithm
- outputting the inverse of that solution as the scramble

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Usage

```bash
python scrambler.py                   # single scramble, scramble-only output
python scrambler.py -n 5              # five scrambles
python scrambler.py --seed 42         # deterministic
python scrambler.py --mode full       # facelets + solution + scramble
```

Example (full mode):

```
Facelets: URRDUULBFDBDBRUBUDURLBFLLRLDFULDLRDRRFFRLDBFBBUFFBDFLU
Solution: U2 R' B' R D F2 R2 F' B' D R L2 U F2 B2 L2 U D R2 F2 D'
Scramble: D F2 R2 D' U' L2 B2 F2 U' L2 R' D' B F R2 F2 D' R' B R U2
```

### Annual Scramble Generator

Generate a JSON file containing scrambles for an entire year, organized by year, month, week, day, and hour.

```bash
python generate_year_scrambles.py --year 2025
```

This will create `scrambles-2025.json` with the following structure:

```json
{
  "y-2025": "R U R' ...",
  "m-2025-01": "F2 D ...",
  "w-2025-01": "L U2 ...",
  "d-2025-01-01": "B2 R ...",
  "h-2025-01-01-00": "D' F ...",
  ...
}
```

Notes

- The random-state generator enforces edge/corner orientation sums and overall permutation parity.
- Kociemba does not always return a shortest solution; this does not affect scramble validity.
