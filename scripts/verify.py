#!/usr/bin/env python3
"""Exact, dependency-free checks for the website submission."""

from __future__ import annotations

import json
import re
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from generate_matrix import build_internal_matrix, matrix_rank  # noqa: E402


def normalized_counts(q: int) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    Q = Fraction(q * (q - 1), 2)
    T = Fraction(q * (q - 1) * (q - 2), 6)
    A0 = 3 * q * Q**2
    B0 = Q**3
    C0 = B0 + 6 * q * T * Q + Fraction(5, 2) * A0
    D0 = 3 * T * Q**2 + 3 * B0
    return A0, B0, C0, D0


def basis_cell_counts(q: int) -> tuple[int, int, int, int]:
    A0, B0, C0, D0 = normalized_counts(q)
    values = (
        q**5 * A0,
        q**6 * B0,
        (q - 1) * q**5 * C0,
        (q - 1) * q**6 * D0,
    )
    assert all(value.denominator == 1 for value in values)
    return tuple(int(value) for value in values)


def ratio(q: int) -> Fraction:
    n11, n10, n01, n00 = basis_cell_counts(q)
    return Fraction(n11 * n00, n10 * n01)


def check_closed_form() -> None:
    for q in range(2, 1001):
        A0, B0, C0, D0 = normalized_counts(q)
        assert A0 == Fraction(3 * q**3 * (q - 1) ** 2, 4)
        assert B0 == Fraction(q**3 * (q - 1) ** 3, 8)
        assert C0 == Fraction(q**3 * (q - 1) ** 2 * (5 * q + 6), 8)
        assert D0 == Fraction(q**3 * (q - 1) ** 3 * (q + 1), 8)
        assert ratio(q) == Fraction(6 * (q + 1), 5 * q + 6)
        assert ratio(q) == Fraction(6, 5) - Fraction(6, 25 * q + 30)
        if q > 2:
            assert ratio(q) > ratio(q - 1)


def check_member_data() -> None:
    data = json.loads((ROOT / "data" / "improved_members.json").read_text())
    assert data["snapshot_date"] == "2026-08-08"
    members = data["members"]
    assert [member["field"] for member in members] == [4, 7]

    old_records = {4: Fraction(8, 7), 7: Fraction(280043, 243256)}
    expected_differences = {
        4: Fraction(1, 91),
        7: Fraction(194525, 9973496),
    }

    for member in members:
        q = member["q"]
        assert q == member["field"]
        assert member["n"] == 3 * q * q + 2
        assert member["rank"] == 7
        observed_ratio = Fraction(member["distinguished_pair_ratio"])
        assert observed_ratio == ratio(q)

        n11, n10, n01, n00 = basis_cell_counts(q)
        counts = member["basis_cell_counts"]
        assert counts == {
            "contain_both": n11,
            "only_i": n10,
            "only_j": n01,
            "avoid_both": n00,
        }

        improvement = observed_ratio - old_records[q]
        assert improvement == expected_differences[q]
        assert Fraction(member["difference"]) == improvement
        assert improvement > 0
        assert member["strict_improvement"] is True


def check_generated_matrices() -> None:
    for q in (4, 7):
        matrix = build_internal_matrix(q)
        assert len(matrix) == 7
        assert all(len(row) == 3 * q * q + 2 for row in matrix)
        assert matrix_rank(matrix, q) == 7
        assert [row[0] for row in matrix] == [1, 0, 0, 0, 0, 0, 0]
        assert [row[1] for row in matrix] == [0, 1, 0, 1, 0, 1, 0]


def check_submission_payload() -> None:
    form = json.loads((ROOT / "submission" / "family_form.json").read_text())
    required = {
        "name",
        "short",
        "claim",
        "parameter",
        "formula_tex",
        "size_rank_tex",
        "supremum",
        "supremum_kind",
        "summary",
        "construction",
        "curve_explanation",
        "proof_status",
        "proof_url",
        "series",
        "contributors",
        "discovery_date",
        "ai_used",
        "ai_model",
        "ai_role",
        "ai_chat_url",
    }
    assert set(form) == required
    assert form["claim"] == "lower"
    assert Fraction(form["supremum"]) == Fraction(6, 5)
    assert form["supremum_kind"] == "approached"
    assert form["contributors"] == "Jeewon Kim"
    assert form["ai_used"] == "yes"
    assert form["proof_url"].endswith("/blob/main/PROOF.md")
    assert re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])", form["discovery_date"])

    limits = {
        "name": 120,
        "short": 40,
        "parameter": 200,
        "formula_tex": 500,
        "size_rank_tex": 500,
        "summary": 1000,
        "construction": 4000,
        "curve_explanation": 4000,
        "proof_status": 2000,
        "proof_url": 500,
        "contributors": 500,
        "ai_model": 200,
        "ai_role": 1000,
        "ai_chat_url": 500,
    }
    for key, limit in limits.items():
        assert 0 < len(form[key]) <= limit, (key, len(form[key]), limit)
    assert form["proof_url"].startswith("https://")
    assert form["ai_chat_url"].startswith("https://")

    series = json.loads(form["series"])
    plotted = json.loads((ROOT / "submission" / "plotted_members.json").read_text())
    assert series == plotted
    assert [point["field"] for point in series] == [4, 7]
    assert len(series) == 2

    for point in series:
        q = point["field"]
        assert point["parameter"] == f"q = {q}"
        assert point["n"] == 3 * q * q + 2
        assert point["rank"] == 7
        assert Fraction(point["alpha"]) == ratio(q)


def main() -> None:
    check_closed_form()
    check_member_data()
    check_generated_matrices()
    check_submission_payload()
    print("all checks passed")


if __name__ == "__main__":
    main()
