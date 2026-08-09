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
import sys
from itertools import product
from typing import Iterator, TextIO

SUPPORTED_FIELDS = (2, 3, 4, 5, 7)
EncodedValue = int | list[int]


def validate_parameters(q: int, r: int, k: int) -> None:
    if q not in SUPPORTED_FIELDS:
        raise ValueError(f"matrix generator supports only {SUPPORTED_FIELDS}")
    if r < 2 or k < 2:
        raise ValueError("r and k must be at least 2")


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
    raise ArithmeticError(f"no inverse for {x} in GF({q})")


def projective_representatives(q: int, r: int) -> Iterator[tuple[int, ...]]:
    """Yield canonical representatives with first nonzero coordinate one."""
    elements = field_elements(q)
    for pivot in range(r):
        prefix = (0,) * pivot + (1,)
        for tail in product(elements, repeat=r - pivot - 1):
            yield prefix + tail


def direction_count(q: int, r: int) -> int:
    """Return the number of unmarked projective directions in a block."""
    return (q**r - 1) // (q - 1) - 1


def matrix_size(q: int, r: int = 2, k: int = 2) -> int:
    """Return the number of represented columns."""
    validate_parameters(q, r, k)
    return k * q * direction_count(q, r) + 2


def _iter_internal_row(q: int, r: int, k: int, row_index: int) -> Iterator[int]:
    """Yield one matrix row in the construction's deterministic column order."""
    # The first two entries are the distinguished columns i and j.
    yield int(row_index == 0)
    if row_index == 0:
        yield 0
        target_block = -1
        target_coordinate = -1
    else:
        target_block, target_coordinate = divmod(row_index - 1, r)
        yield int(target_coordinate == 0)

    elements = field_elements(q)
    marked_direction = (1,) + (0,) * (r - 1)
    for block in range(k):
        for direction in projective_representatives(q, r):
            if direction == marked_direction:
                continue
            for t in elements:
                if row_index == 0:
                    yield t
                elif block == target_block:
                    yield direction[target_coordinate]
                else:
                    yield 0


def iter_internal_rows(q: int, r: int = 2, k: int = 2) -> Iterator[Iterator[int]]:
    """Return a one-pass iterator over lazily generated internal matrix rows."""
    validate_parameters(q, r, k)
    dimension = k * r + 1
    return (_iter_internal_row(q, r, k, row) for row in range(dimension))


def build_internal_matrix(q: int, r: int = 2, k: int = 2) -> list[list[int]]:
    """Return a (kr+1)-by-n row matrix over the internal field encoding."""
    matrix = [list(row) for row in iter_internal_rows(q, r=r, k=k)]
    expected_rows = k * r + 1
    expected_columns = matrix_size(q, r=r, k=k)
    if len(matrix) != expected_rows:
        raise RuntimeError(
            f"generated {len(matrix)} rows, expected {expected_rows}"
        )
    for row_index, row in enumerate(matrix):
        if len(row) != expected_columns:
            raise RuntimeError(
                f"generated row {row_index} with {len(row)} columns, "
                f"expected {expected_columns}"
            )
    return matrix


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


def encode(value: int, q: int) -> EncodedValue:
    if q != 4 or value in (0, 1):
        return value
    return [value & 1, (value >> 1) & 1]


def encoded_matrix(q: int, r: int = 2, k: int = 2) -> list[list[EncodedValue]]:
    return [
        [encode(value, q) for value in row]
        for row in iter_internal_rows(q, r=r, k=k)
    ]


def coordinate_order(k: int, r: int) -> list[str]:
    return ["e0"] + [
        f"u{block}_{coordinate}"
        for block in range(1, k + 1)
        for coordinate in range(1, r + 1)
    ]


def _basis_witness(q: int, r: int, k: int) -> list[list[int]]:
    """Return a square full-rank submatrix contained in the construction.

    Besides the distinguished column e0, each block contributes the affine
    parameter-zero columns in directions e1+e2, e2, ..., er.  All of those
    directions are canonical projective representatives distinct from the
    omitted marked direction e1.
    """
    validate_parameters(q, r, k)
    dimension = k * r + 1
    columns: list[list[int]] = []

    e0 = [0] * dimension
    e0[0] = 1
    columns.append(e0)

    for block in range(k):
        offset = 1 + block * r
        e1_plus_e2 = [0] * dimension
        e1_plus_e2[offset] = 1
        e1_plus_e2[offset + 1] = 1
        columns.append(e1_plus_e2)
        for coordinate in range(1, r):
            basis_column = [0] * dimension
            basis_column[offset + coordinate] = 1
            columns.append(basis_column)

    if len(columns) != dimension:
        raise RuntimeError(
            f"basis witness has {len(columns)} columns, expected {dimension}"
        )
    return [[column[row] for column in columns] for row in range(dimension)]


def validate_full_rank(q: int, r: int = 2, k: int = 2) -> int:
    """Validate full rank using a small explicit submatrix and return the rank."""
    expected_rank = k * r + 1
    witness_rank = matrix_rank(_basis_witness(q, r, k), q)
    if witness_rank != expected_rank:
        raise RuntimeError(
            f"basis witness has rank {witness_rank}, expected {expected_rank}"
        )
    return expected_rank


def _validate_direction_enumeration(q: int, r: int) -> None:
    marked_direction = (1,) + (0,) * (r - 1)
    actual = sum(
        direction != marked_direction
        for direction in projective_representatives(q, r)
    )
    expected = direction_count(q, r)
    if actual != expected:
        raise RuntimeError(
            f"generated {actual} unmarked directions, expected {expected}"
        )


def write_encoded_matrix(
    stream: TextIO,
    q: int,
    r: int = 2,
    k: int = 2,
    *,
    level: int = 0,
    indent: int = 2,
) -> None:
    """Stream the encoded row matrix as JSON without materializing it."""
    validate_parameters(q, r, k)
    array_padding = " " * (level * indent)
    row_padding = " " * ((level + 1) * indent)
    value_padding = " " * ((level + 2) * indent)

    stream.write("[")
    for row_index, row in enumerate(iter_internal_rows(q, r=r, k=k)):
        stream.write("\n" if row_index == 0 else ",\n")
        stream.write(f"{row_padding}[")
        value_count = 0
        for value_count, value in enumerate(row, start=1):
            stream.write("\n" if value_count == 1 else ",\n")
            stream.write(value_padding)
            json.dump(encode(value, q), stream)
        expected_columns = matrix_size(q, r=r, k=k)
        if value_count != expected_columns:
            raise RuntimeError(
                f"generated row {row_index} with {value_count} columns, "
                f"expected {expected_columns}"
            )
        stream.write(f"\n{row_padding}]")
    stream.write(f"\n{array_padding}]")


def _write_metadata_wrapper(
    stream: TextIO, q: int, r: int, k: int, rank: int
) -> None:
    metadata: dict[str, object] = {
        "field": q,
        "field_encoding": (
            "GF(2)[a]/(a^2+a+1), Conway basis [c0,c1]"
            if q == 4
            else f"integers modulo {q}"
        ),
        "parameters": {"q": q, "k": k, "r": r},
        "coordinate_order": coordinate_order(k, r),
        "distinguished_pair_columns": [0, 1],
        "rank": rank,
        "n": matrix_size(q, r=r, k=k),
    }
    stream.write("{\n")
    for key, value in metadata.items():
        stream.write("  ")
        json.dump(key, stream)
        stream.write(": ")
        json.dump(value, stream)
        stream.write(",\n")
    stream.write('  "matrix": ')
    write_encoded_matrix(stream, q, r=r, k=k, level=1)
    stream.write("\n}")


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

    _validate_direction_enumeration(args.q, args.r)
    expected_rank = validate_full_rank(args.q, r=args.r, k=args.k)
    if args.matrix_only:
        write_encoded_matrix(sys.stdout, args.q, r=args.r, k=args.k)
    else:
        _write_metadata_wrapper(
            sys.stdout, args.q, args.r, args.k, expected_rank
        )
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
