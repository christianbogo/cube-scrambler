import random
import argparse
from typing import List, Tuple

import kociemba


# Faces in Kociemba order: U, R, F, D, L, B
FACES = ("U", "R", "F", "D", "L", "B")


# Corner indices and their home face colors (in URF order)
# Indices: 0..7 correspond to URF, UFL, ULB, UBR, DFR, DLF, DBL, DRB
CORNER_COLORS: Tuple[Tuple[str, str, str], ...] = (
    ("U", "R", "F"),  # URF
    ("U", "F", "L"),  # UFL
    ("U", "L", "B"),  # ULB
    ("U", "B", "R"),  # UBR
    ("D", "F", "R"),  # DFR
    ("D", "L", "F"),  # DLF
    ("D", "B", "L"),  # DBL
    ("D", "R", "B"),  # DRB
)


# Edge indices and their home face colors (in UR,UF,UL,UB,DR,DF,DL,DB,FR,FL,BL,BR order)
# Pairs: (face-of-first-sticker, face-of-second-sticker)
EDGE_COLORS: Tuple[Tuple[str, str], ...] = (
    ("U", "R"),  # UR
    ("U", "F"),  # UF
    ("U", "L"),  # UL
    ("U", "B"),  # UB
    ("D", "R"),  # DR
    ("D", "F"),  # DF
    ("D", "L"),  # DL
    ("D", "B"),  # DB
    ("F", "R"),  # FR
    ("F", "L"),  # FL
    ("B", "L"),  # BL
    ("B", "R"),  # BR
)


# Helper to map a facelet label like 'U1' to index in the 54-char facelet string
def idx(face: str, pos: int) -> int:
    base = {"U": 0, "R": 9, "F": 18, "D": 27, "L": 36, "B": 45}[face]
    return base + (pos - 1)


# Corner facelet positions for each corner position index (URF, UFL, ULB, UBR, DFR, DLF, DBL, DRB)
# Each triplet are the facelets (U/R/F etc) for that SOLVED position in order
CORNER_FACELETS: Tuple[Tuple[int, int, int], ...] = (
    (idx("U", 9), idx("R", 1), idx("F", 3)),  # URF
    (idx("U", 7), idx("F", 1), idx("L", 3)),  # UFL
    (idx("U", 1), idx("L", 1), idx("B", 3)),  # ULB
    (idx("U", 3), idx("B", 1), idx("R", 3)),  # UBR
    (idx("D", 3), idx("F", 9), idx("R", 7)),  # DFR
    (idx("D", 1), idx("L", 9), idx("F", 7)),  # DLF
    (idx("D", 7), idx("B", 9), idx("L", 7)),  # DBL
    (idx("D", 9), idx("R", 9), idx("B", 7)),  # DRB
)


# Edge facelet positions for each edge position index (UR,UF,UL,UB,DR,DF,DL,DB,FR,FL,BL,BR)
EDGE_FACELETS: Tuple[Tuple[int, int], ...] = (
    (idx("U", 6), idx("R", 2)),  # UR
    (idx("U", 8), idx("F", 2)),  # UF
    (idx("U", 4), idx("L", 2)),  # UL
    (idx("U", 2), idx("B", 2)),  # UB
    (idx("D", 6), idx("R", 8)),  # DR
    (idx("D", 2), idx("F", 8)),  # DF
    (idx("D", 4), idx("L", 8)),  # DL
    (idx("D", 8), idx("B", 8)),  # DB
    (idx("F", 6), idx("R", 4)),  # FR
    (idx("F", 4), idx("L", 6)),  # FL
    (idx("B", 6), idx("L", 4)),  # BL
    (idx("B", 4), idx("R", 6)),  # BR
)


def permutation_parity(perm: List[int]) -> int:
    seen = [False] * len(perm)
    parity = 0
    for i in range(len(perm)):
        if not seen[i]:
            cycle_len = 0
            j = i
            while not seen[j]:
                seen[j] = True
                j = perm[j]
                cycle_len += 1
            if cycle_len > 0:
                parity ^= (cycle_len - 1) & 1
    return parity


def generate_random_cubie_state(rng: random.Random = random) -> Tuple[List[int], List[int], List[int], List[int]]:
    # corners
    corners_perm = list(range(8))
    rng.shuffle(corners_perm)
    corners_ori = [rng.randrange(3) for _ in range(7)]
    corners_ori.append((-sum(corners_ori)) % 3)

    # edges
    edges_perm = list(range(12))
    rng.shuffle(edges_perm)

    # fix global parity: corner parity XOR edge parity must be 0
    if permutation_parity(corners_perm) ^ permutation_parity(edges_perm):
        # swap last two edges to flip parity
        edges_perm[-1], edges_perm[-2] = edges_perm[-2], edges_perm[-1]

    edges_ori = [rng.randrange(2) for _ in range(11)]
    edges_ori.append((-sum(edges_ori)) % 2)

    return corners_perm, corners_ori, edges_perm, edges_ori


def cubie_to_facelet_string(
    corners_perm: List[int],
    corners_ori: List[int],
    edges_perm: List[int],
    edges_ori: List[int],
) -> str:
    # Start with centers fixed
    facelets: List[str] = [
        *("U" * 9), *("R" * 9), *("F" * 9), *("D" * 9), *("L" * 9), *("B" * 9)
    ]  # type: ignore

    # Place corners
    for pos in range(8):
        cubie = corners_perm[pos]
        o = corners_ori[pos] % 3
        colors = CORNER_COLORS[cubie]
        positions = CORNER_FACELETS[pos]
        # orientation rotates the color order
        for i in range(3):
            color = colors[(i - o) % 3]
            facelets[positions[i]] = color

    # Place edges
    for pos in range(12):
        cubie = edges_perm[pos]
        o = edges_ori[pos] % 2
        colors = EDGE_COLORS[cubie]
        positions = EDGE_FACELETS[pos]
        if o == 0:
            facelets[positions[0]] = colors[0]
            facelets[positions[1]] = colors[1]
        else:
            facelets[positions[0]] = colors[1]
            facelets[positions[1]] = colors[0]

    return "".join(facelets)


def invert_moves(solution: str) -> str:
    if not solution.strip():
        return ""
    inv = []
    for move in reversed(solution.strip().split()):
        if move.endswith("2"):
            inv.append(move)  # U2 inverted is still U2
        elif move.endswith("'"):
            inv.append(move[:-1])
        else:
            inv.append(move + "'")
    return " ".join(inv)


def random_state_scramble(rng: random.Random = random) -> Tuple[str, str, str]:
    corners_perm, corners_ori, edges_perm, edges_ori = generate_random_cubie_state(rng)
    facelets = cubie_to_facelet_string(corners_perm, corners_ori, edges_perm, edges_ori)
    solution = kociemba.solve(facelets)
    scramble = invert_moves(solution)
    return facelets, solution, scramble


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate true random-state 3x3 scrambles using Kociemba.")
    parser.add_argument("--count", "-n", type=int, default=1, help="Number of scrambles to generate")
    parser.add_argument("--seed", type=int, default=None, help="Seed for RNG (for reproducibility)")
    parser.add_argument(
        "--mode",
        choices=["scramble", "full"],
        default="scramble",
        help="Output only the scramble, or full details (facelets, solution, scramble)",
    )
    args = parser.parse_args()

    rng = random.Random(args.seed) if args.seed is not None else random

    for i in range(args.count):
        facelets, solution, scramble = random_state_scramble(rng)
        if args.mode == "scramble":
            print(scramble)
        else:
            print(f"Facelets: {facelets}")
            print(f"Solution: {solution}")
            print(f"Scramble: {scramble}")
            if i < args.count - 1:
                print()


if __name__ == "__main__":
    main()


