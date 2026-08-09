#!/usr/bin/env python3
"""Generate representation matrices for finite submitted-family members.

Supported fields are GF(2), GF(3), GF(4), GF(5), and GF(7), the five fields
used by the plotted submission curves. GF(4) elements are encoded internally
as 0, 1, a, 1+a in GF(2)[a]/(a^2+a+1). JSON output uses coefficient lists
for the two nonscalar GF(4) elements.
"""

from __future__ import annotations

import argparse
import json
from itertools import product
from typing import Any, Iterator

SUPPORTED_FIELDS = (2, 3, 4, 5, 7)


def field_elements(q: int) -> list[int]:
    if q not in SUPPORTED_FIELDS:
        raise ValueError(f"matrix generator supports only {SUPPORTED_FIELDS}")
    return list(range(q))


def add(x: int, y: int, q: int) -> int:
    if q == 4:
        return x ^ y
    if q in (2, 3, 5, 7):
        return (x + y) % q
    raise ValueError(q)


def sub(x: int, y: int, q: int) -> int:
    if q == 4:
        return x ^ y
    if q in (2, 3, 5, 7):
        return (x - y) % q
    raise ValueError(q)


def mul(x: int, y: int, q: int) -> int:
    if q in (2, 3, 5, 7):
        return (x * y) % q
    if q != 4:
        raise ValueError(q)

    # Polynomial-basis multiplication modulo a^2+a+1.
    x0, x1 = x & 1, (x >> 1) & 1
    y0, y1 = y & 1, (y >> 1) & 1
    c0 = x0 * y0
    c1 = x0 * y1 + x1 * y0
    c2 = x1 * y1
    # In characteristic two, a^2=a+1.
    return ((c0 + c2) & 1) | (((c1 + c2) & 1) << 1)


def inv(x: int, q: int) -> int:
    if x == 0:
        raise ZeroDivisionError("zero has no inverse")
    for y in field_elements(q)[1:]:
        if mul(x, y, q) == 1:
            return y
    raise AssertionError("finite-field inverse not found")


def projective_representatives(q: int, r: int) -> Iterator[tuple[int, ...]]:
    """Yield canonical representatives with first nonzero coordinate one."""
    elements = field_elements(q)
    for pivot in range(r):
        prefix = (0,) * pivot + (1,)
        for tail in product(elements, repeat=r - pivot - 1):
            yield prefix + tail


def build_internal_matrix(q: int, r: int = 2, k: int = 2) -> list[list[int]]:
    """Return a (kr+1)-by-n row matrix over the internal field encoding."""
    if q not in SUPPORTED_FIELDS:
        raise ValueError(f"matrix generator supports only {SUPPORTED_FIELDS}")
    if r < 2 or k < 2:
        raise ValueError("r and k must be at least 2")

    elements = field_elements(q)
    dimension = k * r + 1
    columns: list[list[int]] = []

    # Coordinate order: e0, then r coordinates in each block U_ell.
    i_column = [0] * dimension
    i_column[0] = 1
    columns.append(i_column)

    j_column = [0] * dimension
    for block in range(k):
        j_column[1 + block * r] = 1
    columns.append(j_column)

    marked_direction = (1,) + (0,) * (r - 1)
    directions = [
        direction
        for direction in projective_representatives(q, r)
        if direction != marked_direction
    ]
    expected_directions = (q**r - 1) // (q - 1) - 1
    assert len(directions) == expected_directions

    for block in range(k):
        offset = 1 + block * r
        for direction in directions:
            for t in elements:
                column = [0] * dimension
                column[0] = t
                column[offset : offset + r] = direction
                columns.append(column)

    expected_n = k * q * expected_directions + 2
    assert len(columns) == expected_n
    return [[column[row] for column in columns] for row in range(dimension)]


def matrix_rank(matrix: list[list[int]], q: int) -> int:
    a = [row[:] for row in matrix]
    rows = len(a)
    cols = len(a[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = next((row for row in range(rank, rows) if a[row][col] != 0), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = inv(a[rank][col], q)
        a[rank] = [mul(scale, value, q) for value in a[rank]]
        for row in range(rows):
            if row == rank or a[row][col] == 0:
                continue
            factor = a[row][col]
            a[row] = [
                sub(a[row][index], mul(factor, a[rank][index], q), q)
                for index in range(cols)
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def encode(value: int, q: int) -> Any:
    if q != 4 or value in (0, 1):
        return value
    return [value & 1, (value >> 1) & 1]


def encoded_matrix(q: int, r: int = 2, k: int = 2) -> list[list[Any]]:
    return [
        [encode(value, q) for value in row]
        for row in build_internal_matrix(q, r=r, k=k)
    ]


def coordinate_order(k: int, r: int) -> list[str]:
    return ["e0"] + [
        f"u{block}_{coordinate}"
        for block in range(1, k + 1)
        for coordinate in range(1, r + 1)
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("q", type=int, choices=SUPPORTED_FIELDS)
    parser.add_argument("--r", type=int, default=2, help="block dimension")
    parser.add_argument("--k", type=int, default=2, help="number of blocks")
    parser.add_argument(
        "--matrix-only",
        action="store_true",
        help="print only the row matrix rather than the metadata wrapper",
    )
    args = parser.parse_args()
    if args.r < 2 or args.k < 2:
        parser.error("--r and --k must be at least 2")

    matrix = build_internal_matrix(args.q, r=args.r, k=args.k)
    expected_rank = args.k * args.r + 1
    assert matrix_rank(matrix, args.q) == expected_rank
    encoded = [[encode(value, args.q) for value in row] for row in matrix]

    if args.matrix_only:
        output: Any = encoded
    else:
        output = {
            "field": args.q,
            "field_encoding": (
                "GF(2)[a]/(a^2+a+1), Conway basis [c0,c1]"
                if args.q == 4
                else f"integers modulo {args.q}"
            ),
            "parameters": {"q": args.q, "k": args.k, "r": args.r},
            "coordinate_order": coordinate_order(args.k, args.r),
            "distinguished_pair_columns": [0, 1],
            "rank": expected_rank,
            "n": len(matrix[0]),
            "matrix": encoded,
        }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
