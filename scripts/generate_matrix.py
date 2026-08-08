#!/usr/bin/env python3
"""Generate the q=4 or q=7 representation matrix from the construction.

Internal GF(4) elements are encoded as integers 0,1,2,3 representing
0, 1, a, 1+a in GF(2)[a]/(a^2+a+1).  JSON output uses the website's Conway
basis convention: 0, 1, [0,1], [1,1].
"""

from __future__ import annotations

import argparse
import json
from typing import Any


def field_elements(q: int) -> list[int]:
    if q not in (4, 7):
        raise ValueError("this submission generator supports only q=4 and q=7")
    return list(range(q))


def add(x: int, y: int, q: int) -> int:
    if q == 4:
        return x ^ y
    if q == 7:
        return (x + y) % 7
    raise ValueError(q)


def sub(x: int, y: int, q: int) -> int:
    if q == 4:
        return x ^ y
    if q == 7:
        return (x - y) % 7
    raise ValueError(q)


def mul(x: int, y: int, q: int) -> int:
    if q == 7:
        return (x * y) % 7
    if q != 4:
        raise ValueError(q)
    # Polynomial-basis multiplication modulo a^2+a+1.
    x0, x1 = x & 1, (x >> 1) & 1
    y0, y1 = y & 1, (y >> 1) & 1
    c0 = x0 * y0
    c1 = x0 * y1 + x1 * y0
    c2 = x1 * y1
    # a^2 = a+1 in characteristic two.
    return ((c0 + c2) & 1) | (((c1 + c2) & 1) << 1)


def inv(x: int, q: int) -> int:
    if x == 0:
        raise ZeroDivisionError("zero has no inverse")
    for y in field_elements(q)[1:]:
        if mul(x, y, q) == 1:
            return y
    raise AssertionError("finite-field inverse not found")


def build_internal_matrix(q: int) -> list[list[int]]:
    """Return a 7-by-(3q^2+2) row matrix over the internal field encoding."""
    elements = field_elements(q)
    nonzero = elements[1:]
    columns: list[list[int]] = []

    # Coordinate order: e0, a1, z1, a2, z2, a3, z3.
    columns.append([1, 0, 0, 0, 0, 0, 0])  # i=e0
    columns.append([0, 1, 0, 1, 0, 1, 0])  # j=a1+a2+a3

    for r in range(3):
        a_index = 1 + 2 * r
        z_index = 2 + 2 * r

        directions: list[tuple[int, int]] = [(0, 1)]  # z_r
        directions.extend((1, s) for s in nonzero)  # a_r+s z_r

        for a_coeff, z_coeff in directions:
            for t in elements:
                column = [0] * 7
                column[0] = t
                column[a_index] = a_coeff
                column[z_index] = z_coeff
                columns.append(column)

    assert len(columns) == 3 * q * q + 2
    return [[column[row] for column in columns] for row in range(7)]


def matrix_rank(matrix: list[list[int]], q: int) -> int:
    a = [row[:] for row in matrix]
    rows = len(a)
    cols = len(a[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if a[r][col] != 0), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = inv(a[rank][col], q)
        a[rank] = [mul(scale, value, q) for value in a[rank]]
        for r in range(rows):
            if r == rank or a[r][col] == 0:
                continue
            factor = a[r][col]
            a[r] = [sub(a[r][c], mul(factor, a[rank][c], q), q) for c in range(cols)]
        rank += 1
        if rank == rows:
            break
    return rank


def encode(value: int, q: int) -> Any:
    if q == 7:
        return value
    if value in (0, 1):
        return value
    return [value & 1, (value >> 1) & 1]


def encoded_matrix(q: int) -> list[list[Any]]:
    return [[encode(value, q) for value in row] for row in build_internal_matrix(q)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("q", type=int, choices=(4, 7))
    parser.add_argument(
        "--matrix-only",
        action="store_true",
        help="print only the row matrix rather than the metadata wrapper",
    )
    args = parser.parse_args()

    matrix = build_internal_matrix(args.q)
    assert matrix_rank(matrix, args.q) == 7
    encoded = encoded_matrix(args.q)
    if args.matrix_only:
        output: Any = encoded
    else:
        output = {
            "field": args.q,
            "field_encoding": (
                "GF(2)[a]/(a^2+a+1), Conway basis [c0,c1]"
                if args.q == 4
                else "integers modulo 7"
            ),
            "coordinate_order": ["e0", "a1", "z1", "a2", "z2", "a3", "z3"],
            "distinguished_pair_columns": [0, 1],
            "rank": 7,
            "n": 3 * args.q * args.q + 2,
            "matrix": encoded,
        }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
