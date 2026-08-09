#!/usr/bin/env python3
"""Exact, dependency-free checks for the proof and website submission."""

from __future__ import annotations

import json
import re
import sys
from fractions import Fraction
from itertools import combinations
from math import factorial, prod
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from generate_matrix import build_internal_matrix, matrix_rank  # noqa: E402


def projective_point_count(q: int, r: int) -> int:
    return (q**r - 1) // (q - 1)


def projective_basis_count(q: int, r: int) -> int:
    ordered_vector_bases = prod(q**r - q**index for index in range(r))
    return ordered_vector_bases // ((q - 1) ** r * factorial(r))


def z_sum(q: int, m: int) -> Fraction:
    from math import comb

    return sum(
        (
            Fraction(comb(m, support) * (q - 1) ** (support - 1), support + 1)
            for support in range(2, m + 1)
        ),
        Fraction(0),
    )


def z_closed(q: int, m: int) -> Fraction:
    return Fraction(1, q - 1) * (
        Fraction(q ** (m + 1) - 1, (m + 1) * (q - 1))
        - 1
        - Fraction(m * (q - 1), 2)
    )


def block_counts(q: int, r: int) -> tuple[int, int, int, int]:
    """Return b,c,h,s for one punctured projective block."""
    v = projective_point_count(q, r)
    full_bases = projective_basis_count(q, r)
    c_value = Fraction(r * full_bases, v)
    b_value = full_bases - c_value
    h_value = c_value * z_closed(q, r - 1)
    s_value = full_bases * z_closed(q, r) - b_value - h_value
    values = (b_value, c_value, h_value, s_value)
    assert all(value.denominator == 1 for value in values)
    return tuple(int(value) for value in values)


def local_ratios(q: int, r: int) -> tuple[Fraction, Fraction, Fraction]:
    b_value, c_value, h_value, s_value = block_counts(q, r)
    return (
        Fraction(c_value, b_value),
        Fraction(h_value, b_value),
        Fraction(s_value, b_value),
    )


def compact_w(q: int, r: int) -> Fraction:
    v = projective_point_count(q, r)
    x_value = Fraction(r, v - r)
    return (
        Fraction(q, q - 1) * (r - x_value)
        + r * x_value
        + Fraction(r - 1, 2) * x_value**2
    ) / (r + 1)


def normalized_basis_cells(
    q: int, r: int, k: int
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    b_value, c_value, h_value, s_value = block_counts(q, r)
    A0 = Fraction(k * c_value * b_value ** (k - 1))
    B0 = Fraction(b_value**k)
    C0 = (
        B0
        + k * h_value * b_value ** (k - 1)
        + k * (k - 1) * c_value * s_value * b_value ** (k - 2)
        + Fraction(k * r - 1, 2) * A0
    )
    D0 = (
        k * s_value * b_value ** (k - 1)
        + Fraction(k * r, 2) * B0
    )
    return A0, B0, C0, D0


def basis_cell_counts(q: int, r: int, k: int) -> tuple[int, int, int, int]:
    A0, B0, C0, D0 = normalized_basis_cells(q, r, k)
    values = (
        q ** (k * r - 1) * A0,
        q ** (k * r) * B0,
        (q - 1) * q ** (k * r - 1) * C0,
        (q - 1) * q ** (k * r) * D0,
    )
    assert all(value.denominator == 1 for value in values)
    return tuple(int(value) for value in values)


def ratio_from_cells(q: int, r: int, k: int) -> Fraction:
    n11, n10, n01, n00 = basis_cell_counts(q, r, k)
    return Fraction(n11 * n00, n10 * n01)


def exact_ratio(q: int, r: int, k: int = 2) -> Fraction:
    w_value = compact_w(q, r)
    return Fraction(k * k) * w_value / (
        1 + Fraction(k, q - 1) + k * (k - 1) * w_value
    )


def limiting_ratio(q: int, k: int = 2) -> Fraction:
    return Fraction(k * k * q, (k * k - k + 1) * q + k - 1)


def family_size(q: int, r: int, k: int = 2) -> int:
    return k * q * (projective_point_count(q, r) - 1) + 2


def check_closed_formulas() -> None:
    fields = (2, 3, 4, 5, 7, 8, 9, 11)
    for q in fields:
        for r in range(2, 11):
            assert z_sum(q, r) == z_closed(q, r)
            x_value, e_value, y_value = local_ratios(q, r)
            v = projective_point_count(q, r)
            assert x_value == Fraction(r, v - r)
            assert e_value == x_value * z_closed(q, r - 1)
            assert y_value == (1 + x_value) * z_closed(q, r) - 1 - e_value
            assert e_value == Fraction(1, q - 1) - Fraction(r - 1, 2) * x_value
            assert compact_w(q, r) == x_value * (y_value + Fraction(r, 2))

            for k in range(2, 7):
                assert ratio_from_cells(q, r, k) == exact_ratio(q, r, k)

            assert exact_ratio(q, r, 2) < Fraction(4, 3)

        assert exact_ratio(q, 2, 2) == Fraction(8, 7)
        assert exact_ratio(q, 2, 3) == Fraction(6 * (q + 1), 5 * q + 6)

        # Exact rational checks consistent with the proved convergence rate.
        error_20 = abs(exact_ratio(q, 20, 2) - limiting_ratio(q, 2))
        error_200 = abs(exact_ratio(q, 200, 2) - limiting_ratio(q, 2))
        assert error_200 < error_20
        assert error_200 < Fraction(1, 100)
        for k in range(3, 51):
            assert limiting_ratio(q, 2) > limiting_ratio(q, k)

    # The first terms are not monotone, so the proof must rely only on convergence.
    assert exact_ratio(2, 3, 2) < exact_ratio(2, 2, 2)
    assert exact_ratio(4, 3, 2) < exact_ratio(4, 2, 2)


def check_old_special_case_data() -> None:
    data = json.loads((ROOT / "data" / "improved_members.json").read_text())
    assert data["role"] == "regression data for the old (k,r)=(3,2) special case"
    assert data["special_case_parameters"] == {"k": 3, "r": 2}
    assert data["family_formula"] == "6(q+1)/(5q+6)"
    assert [member["field"] for member in data["members"]] == [4, 7]

    old_records = {4: Fraction(8, 7), 7: Fraction(280043, 243256)}
    for member in data["members"]:
        q = member["q"]
        observed_ratio = Fraction(member["distinguished_pair_ratio"])
        assert observed_ratio == exact_ratio(q, 2, 3)
        assert member["n"] == family_size(q, 2, 3)
        assert member["rank"] == 7

        n11, n10, n01, n00 = basis_cell_counts(q, 2, 3)
        assert member["basis_cell_counts"] == {
            "contain_both": n11,
            "only_i": n10,
            "only_j": n01,
            "avoid_both": n00,
        }
        difference = observed_ratio - old_records[q]
        assert Fraction(member["difference"]) == difference
        assert difference > 0
        assert member["strict_improvement"] is True


def check_fixed_field_data() -> None:
    data = json.loads((ROOT / "data" / "fixed_field_bounds.json").read_text())
    assert data["snapshot_date"] == "2026-08-09"
    assert data["submitted_subfamily"]["k"] == 2
    assert Fraction(data["submitted_subfamily"]["iterated_supremum"]) == Fraction(4, 3)

    old_records = {
        2: Fraction(8, 7),
        3: Fraction(100, 81),
        4: Fraction(8, 7),
        5: Fraction(4664, 4007),
        7: Fraction(280043, 243256),
    }
    expected_comparisons = {
        2: "tie",
        3: "below",
        4: "strict improvement",
        5: "strict improvement",
        7: "strict improvement",
    }

    assert [entry["field"] for entry in data["fields"]] == [2, 3, 4, 5, 7]
    for entry in data["fields"]:
        q = entry["field"]
        bound = Fraction(entry["fixed_field_lower_bound"])
        assert bound == limiting_ratio(q, 2)
        difference = bound - old_records[q]
        assert Fraction(entry["difference"]) == difference
        assert entry["comparison"] == expected_comparisons[q]
        assert Fraction(entry["previous_record"]["alpha"]) == old_records[q]

        witness = entry["first_plotted_k2_witness_above_record"]
        if witness is None:
            assert difference <= 0
            continue
        r = witness["r"]
        witness_ratio = Fraction(witness["distinguished_pair_ratio"])
        assert witness_ratio == exact_ratio(q, r, 2)
        assert witness["n"] == family_size(q, r, 2)
        assert witness["rank"] == 2 * r + 1
        assert Fraction(witness["difference"]) == witness_ratio - old_records[q]
        assert witness_ratio > old_records[q]


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
    assert Fraction(form["supremum"]) == Fraction(4, 3)
    assert form["supremum_kind"] == "iterated limit"
    assert form["contributors"] == "Jeewon Kim"
    assert form["ai_used"] == "yes"
    assert form["ai_chat_url"] == ""
    assert "4q}{3q+1" in form["formula_tex"]
    assert "\\mathrm{rk}" in form["size_rank_tex"]
    assert form["proof_url"].endswith(
        "/blob/agent/fixed-field-4q-over-3q-plus-1/PROOF.md"
    )
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
    }
    for key, limit in limits.items():
        assert 0 < len(form[key]) <= limit, (key, len(form[key]), limit)
    assert form["proof_url"].startswith("https://")

    series = json.loads(form["series"])
    plotted = json.loads((ROOT / "submission" / "plotted_members.json").read_text())
    assert series == plotted
    assert [curve["label"] for curve in series] == [
        "q = 2",
        "q = 3",
        "q = 4",
        "q = 5",
        "q = 7",
    ]
    assert len(series) <= 12
    assert sum(len(curve["points"]) for curve in series) <= 400

    for curve in series:
        q = int(curve["label"].split("=")[1])
        previous_r = 1
        for point in curve["points"]:
            match = re.fullmatch(r"q = (\d+), r = (\d+)", point["parameter"])
            assert match is not None
            point_q, r = map(int, match.groups())
            assert point_q == q == point["field"]
            assert r > previous_r
            previous_r = r
            assert point["n"] == family_size(q, r, 2)
            assert point["rank"] == 2 * r + 1
            alpha = Fraction(point["alpha"])
            assert alpha == exact_ratio(q, r, 2)
            assert point["n"] <= 1_000_000
            assert alpha.numerator <= 999_999_999
            assert alpha.denominator <= 999_999_999


def check_generated_matrices() -> None:
    configurations = (
        (2, 2, 2),
        (3, 2, 2),
        (4, 2, 3),
        (5, 3, 2),
        (7, 2, 2),
    )
    for q, r, k in configurations:
        matrix = build_internal_matrix(q, r=r, k=k)
        expected_rank = k * r + 1
        expected_n = family_size(q, r, k)
        assert len(matrix) == expected_rank
        assert all(len(row) == expected_n for row in matrix)
        assert matrix_rank(matrix, q) == expected_rank
        assert [row[0] for row in matrix] == [1] + [0] * (expected_rank - 1)
        expected_j = [0] * expected_rank
        for block in range(k):
            expected_j[1 + block * r] = 1
        assert [row[1] for row in matrix] == expected_j


def brute_force_basis_cells(q: int, r: int, k: int) -> tuple[int, int, int, int]:
    matrix = build_internal_matrix(q, r=r, k=k)
    rank = k * r + 1
    n = len(matrix[0])
    cells = {(True, True): 0, (True, False): 0, (False, True): 0, (False, False): 0}
    for subset in combinations(range(n), rank):
        submatrix = [[row[column] for column in subset] for row in matrix]
        if matrix_rank(submatrix, q) != rank:
            continue
        cells[(0 in subset, 1 in subset)] += 1
    return (
        cells[(True, True)],
        cells[(True, False)],
        cells[(False, True)],
        cells[(False, False)],
    )


def check_small_brute_force_counts() -> None:
    for q, r, k in ((2, 2, 2), (2, 2, 3)):
        assert brute_force_basis_cells(q, r, k) == basis_cell_counts(q, r, k)


def check_markdown_style() -> None:
    forbidden_markdown = ("\\(", "\\)", "\\[", "\\]", "\\operatorname", "\\operatername")
    for path in ROOT.rglob("*.md"):
        text = path.read_text()
        for token in forbidden_markdown:
            assert token not in text, (path.relative_to(ROOT), token)

    for pattern in ("*.md", "*.json"):
        for path in ROOT.rglob(pattern):
            text = path.read_text()
            assert "\\operatorname" not in text, path.relative_to(ROOT)
            assert "\\operatername" not in text, path.relative_to(ROOT)


def check_all_json_parses() -> None:
    for path in ROOT.rglob("*.json"):
        json.loads(path.read_text())


def main() -> None:
    check_closed_formulas()
    check_old_special_case_data()
    check_fixed_field_data()
    check_submission_payload()
    check_generated_matrices()
    check_small_brute_force_counts()
    check_markdown_style()
    check_all_json_parses()
    print("all checks passed")


if __name__ == "__main__":
    main()
