#!/usr/bin/env python3
"""Exact, offline checks for the proof data and website submission."""

from __future__ import annotations

import hashlib
import io
import json
import re
import sys
from datetime import datetime
from fractions import Fraction
from itertools import combinations
from math import factorial, prod
from pathlib import Path
from typing import Any, NoReturn

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from generate_matrix import (  # noqa: E402
    SUPPORTED_FIELDS,
    build_internal_matrix,
    encoded_matrix,
    inv,
    matrix_rank,
    mul,
    projective_representatives,
    write_encoded_matrix,
)

SNAPSHOT_DATE = "2026-08-09"
SNAPSHOT_FILENAME = "website_database_2026-08-09.json"
SNAPSHOT_URL = "https://matroid-correlation-constants.icarm.cloud/database.json"
SNAPSHOT_RETRIEVED_AT = "2026-08-09T05:23:28Z"
SNAPSHOT_ETAG = '"e914a97cae79909837dfa9980ee465a6"'
SNAPSHOT_SHA256 = "e914a97cae79909837dfa9980ee465a60139783da4114c6c5052659d9edf4db7"
SOURCE_REPOSITORY = "https://github.com/icarm/matroid-correlation-constants"
SOURCE_COMMIT = "d9fc87242e3128df5516401908064e9edc541e42"
EXPECTED_FIELDS = (2, 3, 4, 5, 7)


class VerificationError(RuntimeError):
    """A reproducibility or mathematical regression check failed."""


def fail(message: str) -> NoReturn:
    raise VerificationError(message)


def check(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        fail(f"could not read valid JSON from {path.relative_to(ROOT)}: {error}")


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def exact_fraction(value: object, where: str) -> Fraction:
    """Mirror the website's unsigned, at-most-nine-digit fraction parser."""
    if not isinstance(value, str):
        fail(f"{where}: expected an exact fraction string")
    text = value.strip()
    match = re.fullmatch(r"(\d{1,9})(?:\s*/\s*([1-9]\d{0,8}))?", text)
    if match is None:
        fail(f"{where}: invalid exact fraction {value!r}")
    numerator = int(match.group(1))
    denominator = int(match.group(2) or "1")
    return Fraction(numerator, denominator)


def signed_data_fraction(value: object, where: str) -> Fraction:
    """Parse a reduced signed fraction used by offline comparison data."""
    if not isinstance(value, str):
        fail(f"{where}: expected a fraction string")
    check(
        re.fullmatch(r"-?\d+(?:/[1-9]\d*)?", value) is not None,
        f"{where}: invalid signed fraction {value!r}",
    )
    parsed = Fraction(value)
    check(value == fraction_text(parsed), f"{where}: fraction is not in reduced canonical form")
    return parsed


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
    check(
        all(value.denominator == 1 for value in values),
        f"block counts are not integral for q={q}, r={r}: {values}",
    )
    return int(b_value), int(c_value), int(h_value), int(s_value)


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
    D0 = k * s_value * b_value ** (k - 1) + Fraction(k * r, 2) * B0
    return A0, B0, C0, D0


def basis_cell_counts(q: int, r: int, k: int) -> tuple[int, int, int, int]:
    A0, B0, C0, D0 = normalized_basis_cells(q, r, k)
    values = (
        q ** (k * r - 1) * A0,
        q ** (k * r) * B0,
        (q - 1) * q ** (k * r - 1) * C0,
        (q - 1) * q ** (k * r) * D0,
    )
    check(
        all(value.denominator == 1 for value in values),
        f"basis-cell counts are not integral for q={q}, r={r}, k={k}: {values}",
    )
    return int(values[0]), int(values[1]), int(values[2]), int(values[3])


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


def reverse_limiting_ratio(r: int) -> Fraction:
    return Fraction(4 * r, 3 * r + 1)


def family_size(q: int, r: int, k: int = 2) -> int:
    return k * q * (projective_point_count(q, r) - 1) + 2


def check_closed_formulas() -> None:
    fields = (2, 3, 4, 5, 7, 8, 9, 11)
    for q in fields:
        for r in range(2, 11):
            context = f"q={q}, r={r}"
            check(z_sum(q, r) == z_closed(q, r), f"z formula mismatch at {context}")
            x_value, e_value, y_value = local_ratios(q, r)
            v = projective_point_count(q, r)
            check(x_value == Fraction(r, v - r), f"x formula mismatch at {context}")
            check(
                e_value == x_value * z_closed(q, r - 1),
                f"e formula mismatch at {context}",
            )
            check(
                y_value == (1 + x_value) * z_closed(q, r) - 1 - e_value,
                f"y formula mismatch at {context}",
            )
            check(
                e_value == Fraction(1, q - 1) - Fraction(r - 1, 2) * x_value,
                f"compact e formula mismatch at {context}",
            )
            check(
                compact_w(q, r) == x_value * (y_value + Fraction(r, 2)),
                f"compact w formula mismatch at {context}",
            )

            for k in range(2, 7):
                check(
                    ratio_from_cells(q, r, k) == exact_ratio(q, r, k),
                    f"basis-cell ratio mismatch at {context}, k={k}",
                )

            check(
                exact_ratio(q, r, 2) < Fraction(4, 3),
                f"finite k=2 ratio reaches 4/3 at {context}",
            )

        check(exact_ratio(q, 2, 2) == Fraction(8, 7), f"r=2 k=2 mismatch for q={q}")
        check(
            exact_ratio(q, 2, 3) == Fraction(6 * (q + 1), 5 * q + 6),
            f"old special-case formula mismatch for q={q}",
        )

        # These are exact regression checks for the proved convergence theorem.
        error_20 = abs(exact_ratio(q, 20, 2) - limiting_ratio(q, 2))
        error_200 = abs(exact_ratio(q, 200, 2) - limiting_ratio(q, 2))
        check(error_200 < error_20, f"convergence regression failed for q={q}")
        check(error_200 < Fraction(1, 100), f"convergence tolerance failed for q={q}")
        for k in range(2, 51):
            limiting_denominator = (k * k - k + 1) * q + k - 1
            check(
                limiting_ratio(q, k) * limiting_denominator == k * k * q,
                f"limiting-ratio substitution certificate failed for q={q}, k={k}",
            )
            check(
                4 * limiting_denominator - k * k * (3 * q + 1)
                == (k - 2) ** 2 * (q - 1),
                f"limiting k-optimality identity failed for q={q}, k={k}",
            )
        for k in range(3, 51):
            check(
                limiting_ratio(q, 2) > limiting_ratio(q, k),
                f"limiting k optimization regression failed for q={q}, k={k}",
            )

    for r in range(2, 11):
        limiting_w = Fraction(r, r + 1)
        substituted_ratio = 4 * limiting_w / (1 + 2 * limiting_w)
        check(
            substituted_ratio == reverse_limiting_ratio(r),
            f"reverse-limit substitution certificate failed for r={r}",
        )
        error_101 = abs(exact_ratio(101, r, 2) - reverse_limiting_ratio(r))
        error_1009 = abs(exact_ratio(1009, r, 2) - reverse_limiting_ratio(r))
        if r == 2:
            check(error_101 == error_1009 == 0, "r=2 reverse-limit identity changed")
        else:
            check(error_1009 < error_101, f"reverse-limit regression failed for r={r}")

    # The first terms are not monotone; the analytic argument uses convergence.
    check(exact_ratio(2, 3, 2) < exact_ratio(2, 2, 2), "q=2 nonmonotonicity changed")
    check(exact_ratio(4, 3, 2) < exact_ratio(4, 2, 2), "q=4 nonmonotonicity changed")


def load_database_snapshot() -> tuple[dict[str, Any], dict[int, dict[str, Any]]]:
    manifest_path = ROOT / "data" / "website_database_snapshot_manifest.json"
    manifest = load_json(manifest_path)
    check(isinstance(manifest, dict), "snapshot manifest must be a JSON object")
    expected_keys = {
        "schema_version",
        "snapshot_date",
        "snapshot_file",
        "source_url",
        "retrieved_at_utc",
        "etag",
        "sha256",
        "source_repository",
        "source_commit",
    }
    check(set(manifest) == expected_keys, "snapshot manifest keys do not match schema version 1")
    check(manifest["schema_version"] == 1, "unsupported snapshot manifest schema version")
    check(manifest["snapshot_date"] == SNAPSHOT_DATE, "snapshot manifest date mismatch")
    check(manifest["snapshot_file"] == SNAPSHOT_FILENAME, "snapshot filename mismatch")
    check(manifest["source_url"] == SNAPSHOT_URL, "snapshot source URL mismatch")
    check(manifest["source_repository"] == SOURCE_REPOSITORY, "source repository mismatch")
    check(manifest["source_commit"] == SOURCE_COMMIT, "website source commit mismatch")
    check(
        manifest["retrieved_at_utc"] == SNAPSHOT_RETRIEVED_AT,
        "snapshot retrieval timestamp differs from the archived response",
    )
    check(manifest["etag"] == SNAPSHOT_ETAG, "snapshot ETag differs from the archived response")
    check(manifest["sha256"] == SNAPSHOT_SHA256, "snapshot SHA-256 differs from the known digest")
    check(
        isinstance(manifest["retrieved_at_utc"], str)
        and re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", manifest["retrieved_at_utc"])
        is not None,
        "snapshot retrieval time must be an exact UTC timestamp",
    )
    retrieval = datetime.strptime(manifest["retrieved_at_utc"], "%Y-%m-%dT%H:%M:%SZ")
    check(retrieval.date().isoformat() == SNAPSHOT_DATE, "retrieval date differs from snapshot date")
    check(
        isinstance(manifest["etag"], str)
        and 0 < len(manifest["etag"]) <= 200
        and "\n" not in manifest["etag"],
        "snapshot ETag must be a nonempty single-line string",
    )
    check(
        isinstance(manifest["sha256"], str)
        and re.fullmatch(r"[0-9a-f]{64}", manifest["sha256"]) is not None,
        "snapshot SHA-256 must be 64 lowercase hexadecimal characters",
    )

    snapshot_path = ROOT / "data" / manifest["snapshot_file"]
    try:
        snapshot_bytes = snapshot_path.read_bytes()
    except OSError as error:
        fail(f"could not read archived website database: {error}")
    observed_hash = hashlib.sha256(snapshot_bytes).hexdigest()
    check(observed_hash == manifest["sha256"], "archived database SHA-256 mismatch")
    snapshot = load_json(snapshot_path)
    check(isinstance(snapshot, dict), "archived website database must be an object")
    check(set(snapshot) == {"count", "matroids"}, "archived database top-level shape changed")
    check(isinstance(snapshot["matroids"], list), "archived database matroids must be a list")
    check(snapshot["count"] == len(snapshot["matroids"]), "archived database count mismatch")

    records: dict[int, dict[str, Any]] = {}
    for index, record in enumerate(snapshot["matroids"]):
        where = f"archived database record {index + 1}"
        check(isinstance(record, dict), f"{where} must be an object")
        record_id = record.get("id")
        check(isinstance(record_id, int) and record_id > 0, f"{where} has an invalid id")
        check(record_id not in records, f"archived database repeats record id {record_id}")
        check(record.get("name") is None or isinstance(record.get("name"), str), f"{where} name invalid")
        check(
            isinstance(record.get("field"), str) and record["field"].isdigit(),
            f"{where} field invalid",
        )
        check(isinstance(record.get("n"), int) and record["n"] >= 1, f"{where} n invalid")
        check(
            isinstance(record.get("rank"), int) and 0 <= record["rank"] <= record["n"],
            f"{where} rank invalid",
        )
        alpha = record.get("alpha")
        check(isinstance(alpha, dict), f"{where} alpha must be an object")
        check(
            isinstance(alpha.get("numerator"), int)
            and isinstance(alpha.get("denominator"), int)
            and alpha["numerator"] >= 0
            and alpha["denominator"] > 0,
            f"{where} alpha fraction invalid",
        )
        check(isinstance(record.get("current"), bool), f"{where} current flag invalid")
        records[record_id] = record

    for q in EXPECTED_FIELDS:
        current = [
            record
            for record in records.values()
            if record["field"] == str(q) and record["current"] is True
        ]
        check(len(current) == 1, f"expected exactly one current archived record for GF({q})")
    return manifest, records


def record_fraction(record: dict[str, Any]) -> Fraction:
    alpha = record["alpha"]
    return Fraction(alpha["numerator"], alpha["denominator"])


def record_metadata(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": record["id"],
        "name": record["name"],
        "field": record["field"],
        "n": record["n"],
        "rank": record["rank"],
        "alpha": fraction_text(record_fraction(record)),
        "current": record["current"],
    }


def current_records_by_field(records: dict[int, dict[str, Any]]) -> dict[int, dict[str, Any]]:
    return {
        q: next(
            record
            for record in records.values()
            if record["field"] == str(q) and record["current"] is True
        )
        for q in EXPECTED_FIELDS
    }


def check_snapshot_reference(data: dict[str, Any], where: str) -> None:
    check(data.get("snapshot_date") == SNAPSHOT_DATE, f"{where}: snapshot date mismatch")
    check(
        data.get("website_database_snapshot") == f"data/{SNAPSHOT_FILENAME}",
        f"{where}: archived database path mismatch",
    )
    check(
        data.get("website_database_manifest")
        == "data/website_database_snapshot_manifest.json",
        f"{where}: snapshot manifest path mismatch",
    )


def check_old_special_case_data(records: dict[int, dict[str, Any]]) -> None:
    data = load_json(ROOT / "data" / "improved_members.json")
    check(isinstance(data, dict), "improved_members.json must contain an object")
    check_snapshot_reference(data, "improved_members.json")
    check(
        data.get("role") == "regression data for the old (k,r)=(3,2) special case",
        "old-special-case role changed",
    )
    check(data.get("special_case_parameters") == {"k": 3, "r": 2}, "special-case parameters changed")
    check(data.get("family_formula") == "6(q+1)/(5q+6)", "special-case family formula changed")
    members = data.get("members")
    check(isinstance(members, list), "improved_members members must be a list")
    check([member.get("field") for member in members] == [4, 7], "special-case fields changed")

    current = current_records_by_field(records)
    for member in members:
        q = member["q"]
        context = f"old special-case member q={q}"
        check(member["field"] == q, f"{context}: field and q differ")
        check(member["previous_record"] == record_metadata(current[q]), f"{context}: archived record mismatch")
        previous_ratio = record_fraction(current[q])
        observed_ratio = exact_fraction(member["distinguished_pair_ratio"], f"{context} ratio")
        check(observed_ratio == exact_ratio(q, 2, 3), f"{context}: ratio formula mismatch")
        check(member["n"] == family_size(q, 2, 3), f"{context}: size mismatch")
        check(member["rank"] == 7, f"{context}: rank mismatch")

        n11, n10, n01, n00 = basis_cell_counts(q, 2, 3)
        check(
            member["basis_cell_counts"]
            == {
                "contain_both": n11,
                "only_i": n10,
                "only_j": n01,
                "avoid_both": n00,
            },
            f"{context}: regression basis-cell counts mismatch",
        )
        difference = observed_ratio - previous_ratio
        check(
            signed_data_fraction(member["difference"], f"{context} difference") == difference,
            f"{context}: difference mismatch",
        )
        check(difference > 0, f"{context}: no longer improves the archived record")
        check(member["strict_improvement"] is True, f"{context}: improvement flag must be true")


def plotted_points_by_field() -> dict[int, list[tuple[int, dict[str, Any]]]]:
    plotted = load_json(ROOT / "submission" / "plotted_members.json")
    check(isinstance(plotted, list), "plotted_members.json must contain a list")
    result: dict[int, list[tuple[int, dict[str, Any]]]] = {}
    for series_index, curve in enumerate(plotted):
        check(isinstance(curve, dict), f"plotted curve {series_index + 1} must be an object")
        label = curve.get("label")
        match = re.fullmatch(r"q = (\d+)", label) if isinstance(label, str) else None
        if match is None:
            fail(f"plotted curve {series_index + 1} label is invalid")
        q = int(match.group(1))
        points = curve.get("points")
        check(isinstance(points, list) and len(points) > 0, f"q={q} plotted points must be nonempty")
        result[q] = []
        for point in points:
            parameter = point.get("parameter") if isinstance(point, dict) else None
            point_match = re.fullmatch(r"q = (\d+), r = (\d+)", parameter) if isinstance(parameter, str) else None
            if point_match is None:
                fail(f"q={q} has an invalid plotted parameter")
            point_q, r = map(int, point_match.groups())
            check(point_q == q, f"q={q}, r={r} parameter has the wrong field")
            result[q].append((r, point))
    return result


EXPECTED_SUBFAMILY = {
    "k": 2,
    "finite_ratio": "4w/(1+2/(q-1)+2w)",
    "fixed_field_limit": "4q/(3q+1)",
    "iterated_supremum": "4/3",
    "size": "2q^2(q^(r-1)-1)/(q-1)+2",
    "rank": "2r+1",
}


def check_fixed_field_data(records: dict[int, dict[str, Any]]) -> None:
    data = load_json(ROOT / "data" / "fixed_field_bounds.json")
    check(isinstance(data, dict), "fixed_field_bounds.json must contain an object")
    check_snapshot_reference(data, "fixed_field_bounds.json")
    check(data.get("submitted_subfamily") == EXPECTED_SUBFAMILY, "submitted_subfamily strings changed")
    check(
        exact_fraction(data["submitted_subfamily"]["iterated_supremum"], "iterated supremum")
        == Fraction(4, 3),
        "iterated supremum is not 4/3",
    )

    entries = data.get("fields")
    check(isinstance(entries, list), "fixed-field entries must be a list")
    check([entry.get("field") for entry in entries] == list(EXPECTED_FIELDS), "fixed-field order changed")
    current = current_records_by_field(records)
    plotted = plotted_points_by_field()
    check(set(plotted) == set(EXPECTED_FIELDS), "plotted field set differs from fixed-field data")

    for entry in entries:
        q = entry["field"]
        context = f"fixed-field entry q={q}"
        record = current[q]
        check(entry["previous_record"] == record_metadata(record), f"{context}: archived record mismatch")
        previous_ratio = record_fraction(record)
        bound = exact_fraction(entry["fixed_field_lower_bound"], f"{context} bound")
        check(bound == limiting_ratio(q, 2), f"{context}: fixed-field formula mismatch")
        difference = bound - previous_ratio
        check(
            signed_data_fraction(entry["difference"], f"{context} difference") == difference,
            f"{context}: difference mismatch",
        )
        comparison = "tie" if difference == 0 else "strict improvement" if difference > 0 else "below"
        check(entry["comparison"] == comparison, f"{context}: comparison label mismatch")

        plotted_above = [
            (r, point)
            for r, point in plotted[q]
            if exact_fraction(point["alpha"], f"q={q}, r={r} plotted alpha") > previous_ratio
        ]
        first_plotted = plotted_above[0] if plotted_above else None
        witness = entry["first_plotted_k2_witness_above_record"]
        if witness is None:
            check(difference <= 0, f"{context}: positive limiting improvement lacks a witness")
            check(first_plotted is None, f"{context}: null witness overlooks an improving plotted point")
            continue

        if first_plotted is None:
            fail(f"{context}: witness is not among plotted points")
        r, point = first_plotted
        witness_ratio = exact_fraction(witness["distinguished_pair_ratio"], f"{context} witness ratio")
        expected_witness = {
            "r": r,
            "n": point["n"],
            "rank": point["rank"],
            "distinguished_pair_ratio": point["alpha"],
            "difference": fraction_text(witness_ratio - previous_ratio),
        }
        check(witness == expected_witness, f"{context}: first plotted witness metadata mismatch")
        check(witness_ratio == exact_ratio(q, r, 2), f"{context}: witness ratio formula mismatch")
        check(witness_ratio > previous_ratio, f"{context}: witness does not improve the record")
        for earlier_r in range(2, r):
            check(
                exact_ratio(q, earlier_r, 2) <= previous_ratio,
                f"{context}: r={earlier_r} is an earlier unreported witness",
            )


EXPECTED_SUBMISSION_TEXT = {
    "name": "Punctured-projective-block affine-fibre matroids",
    "short": "Punctured PG fibres",
    "parameter": (
        "prime powers \\(q\\) and integers \\(r\\ge 2\\); the submitted curves use the "
        "\\(k=2\\) subfamily"
    ),
    "formula_tex": (
        "R_{ij}(M_{q,r})=\\frac{4w_{q,r}}{1+2/(q-1)+2w_{q,r}},\\quad "
        "x_{q,r}=\\frac{r}{(q^r-1)/(q-1)-r},\\quad "
        "w_{q,r}=\\frac{q(r-x_{q,r})/(q-1)+rx_{q,r}+(r-1)x_{q,r}^2/2}{r+1},"
        "\\quad \\lim_{r\\to\\infty}R_{ij}(M_{q,r})=\\frac{4q}{3q+1}"
    ),
    "size_rank_tex": (
        "|E(M_{q,r})|=\\frac{2q^2(q^{r-1}-1)}{q-1}+2,\\qquad "
        "\\mathrm{rk}(M_{q,r})=2r+1"
    ),
    "summary": (
        "For every prime power \\(q\\) and finite \\(r\\ge 2\\), an explicit "
        "\\(\\mathbf F_q\\)-representable matroid has the displayed exact distinguished-pair "
        "ratio. As \\(r\\to\\infty\\), this gives the fixed-field bound "
        "\\(\\overline{\\alpha}(\\mathbf F_q)\\ge \\frac{4q}{3q+1}\\); these bounds tend "
        "to \\(\\frac43\\) as \\(q\\to\\infty\\)."
    ),
    "construction": (
        "Let \\(F=\\mathbf F_q\\). Take two independent \\(r\\)-dimensional spaces "
        "\\(U_1,U_2\\) with marked nonzero vectors \\(a_1,a_2\\), and put "
        "\\(W=U_1\\oplus U_2\\) and \\(V=F e_0\\oplus W\\). In each "
        "\\(\\mathrm{PG}(U_\\ell)\\), delete \\([a_\\ell]\\). For every retained projective "
        "direction \\(g\\), include its complete affine fibre \\(\\{t e_0+g:t\\in F\\}\\). "
        "Finally include \\(i=e_0\\) and \\(j=a_1+a_2\\). The vector matroid of these columns "
        "has rank \\(2r+1\\) and the stated size."
    ),
    "curve_explanation": (
        "Each grouped curve fixes \\(q\\) and plots exact finite-\\(r\\) distinguished-pair "
        "values, so every point is realized by a finite matroid represented directly over "
        "\\(\\mathbf F_q\\). The curve is dashed because the proof gives "
        "\\(\\overline{\\alpha}(M_{q,r})\\ge R_{ij}(M_{q,r})\\), not equality with the full "
        "invariant. A fixed-\\(q\\) curve converges to \\(\\frac{4q}{3q+1}\\), and these "
        "fixed-field bounds converge to the displayed, unattained two-parameter supremum "
        "\\(\\frac43\\) as \\(q\\) grows. For fixed \\(r\\), the reverse limit is "
        "\\(\\lim_{q\\to\\infty}R_{ij}(M_{q,r})=\\frac{4r}{3r+1}\\), so the opposite iterated "
        "order also tends to \\(\\frac43\\). The finite values need not be monotone in \\(r\\)."
    ),
    "proof_status": (
        "A complete analytic proof of the representation, rank, size, four basis-cell counts, "
        "exact finite ratio, fixed-\\(q\\) and fixed-\\(r\\) limits, optimization over the block "
        "count, and unattained two-parameter supremum is provided in the linked repository. The "
        "verifier supplies independent small-case enumeration and regression checks; it is not "
        "a substitute for the universal proof. Equality with the full invariant of each finite "
        "member is not claimed."
    ),
    "contributors": "Jeewon Kim",
    "ai_model": "GPT-5.6 Pro",
    "ai_role": (
        "AI assisted with mathematical exploration, exact projective-geometry and affine-fibre "
        "counting, asymptotic simplification, proof auditing, record comparison, and preparation "
        "of reproducible submission files. The submitted claim is the distinguished-pair lower "
        "bound proved in the linked writeup."
    ),
}


def website_code_block(markdown: str, heading: str) -> str:
    pattern = rf"^### {re.escape(heading)}\s*$.*?^```text\s*$\n(.*?)\n^```\s*$"
    matches = re.findall(pattern, markdown, flags=re.MULTILINE | re.DOTALL)
    check(len(matches) == 1, f"WEBSITE_SUBMISSION.md must have one text block for {heading!r}")
    return matches[0]


def check_website_submission_parity(form: dict[str, Any]) -> None:
    try:
        markdown = (ROOT / "WEBSITE_SUBMISSION.md").read_text(encoding="utf-8")
    except OSError as error:
        fail(f"could not read WEBSITE_SUBMISSION.md: {error}")
    headings = {
        "Family name": "name",
        "Short chart name": "short",
        "Claim type": "claim",
        "Parameter": "parameter",
        "Formula": "formula_tex",
        "Size and rank": "size_rank_tex",
        "Supremum": "supremum",
        "Supremum status": "supremum_kind",
        "Summary": "summary",
        "Construction": "construction",
        "What the curve shows": "curve_explanation",
        "Proof status": "proof_status",
        "Proof URL": "proof_url",
        "AI role": "ai_role",
    }
    for heading, key in headings.items():
        check(
            website_code_block(markdown, heading) == form[key],
            f"WEBSITE_SUBMISSION.md {heading!r} differs from family_form.json {key!r}",
        )
    expected_discovery = "\n".join(
        (
            f'Discovered by: {form["contributors"]}',
            f'Discovery date: {form["discovery_date"]}',
            f'AI used: {form["ai_used"]}',
            f'AI model: {form["ai_model"]}',
            f'Public AI conversation: {form["ai_chat_url"]}',
        )
    )
    check(
        website_code_block(markdown, "Discovery record") == expected_discovery,
        "WEBSITE_SUBMISSION.md discovery record differs from family_form.json",
    )


def check_submission_payload() -> None:
    form = load_json(ROOT / "submission" / "family_form.json")
    check(isinstance(form, dict), "family_form.json must contain an object")
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
    check(set(form) == required, "family_form.json fields differ from the official form")
    for key, expected in EXPECTED_SUBMISSION_TEXT.items():
        check(form[key] == expected, f"family_form.json exact text changed in {key}")

    check(form["claim"] in {"exact", "lower"}, "invalid family claim type")
    check(form["claim"] == "lower", "submitted claim must remain a lower bound")
    supremum = exact_fraction(form["supremum"], "family supremum")
    check(supremum == Fraction(4, 3), "family supremum changed")
    check(supremum <= 2, "family supremum exceeds the HSW bound")
    check(
        form["supremum_kind"] in {"attained", "approached", "iterated limit"},
        "invalid supremum kind",
    )
    check(form["supremum_kind"] == "iterated limit", "supremum classification changed")
    check(form["ai_used"] in {"yes", "no"}, "AI-use declaration must be yes or no")
    check(form["ai_used"] == "yes", "AI-use declaration changed")
    check(
        form["ai_chat_url"]
        == "https://chatgpt.com/share/6a77e552-a1dc-83e8-b0bb-05ff004d1084",
        "AI chat URL changed",
    )

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
        "discovery_date": 10,
        "ai_model": 200,
        "ai_role": 1000,
        "ai_chat_url": 500,
    }
    for key, limit in limits.items():
        value = form[key]
        check(isinstance(value, str), f"family form field {key} must be text")
        check(value == value.strip(), f"family form field {key} has surrounding whitespace")
        check(0 < len(value) <= limit, f"family form field {key} exceeds its {limit}-character limit")
    check(
        re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])(?:-(0[1-9]|[12]\d|3[01]))?", form["discovery_date"])
        is not None,
        "discovery date must be YYYY-MM or YYYY-MM-DD",
    )
    check(re.match(r"^https?://", form["proof_url"]) is not None, "proof URL must be HTTP(S)")
    check(
        re.fullmatch(
            r"https://github\.com/dylan0301/Punctured-projective-block-affine-fibre-matroids/"
            r"blob/(?:main|[0-9a-f]{40})/PROOF\.md",
            form["proof_url"],
        )
        is not None,
        "proof URL must target this repository's main branch or an immutable commit",
    )
    check(re.match(r"^https?://", form["ai_chat_url"]) is not None, "AI chat URL must be HTTP(S)")
    if form["ai_used"] == "yes":
        check(bool(form["ai_model"]), "AI model is required when AI use is declared")
        check(bool(form["ai_role"]), "AI role is required when AI use is declared")

    check(len(form["series"]) <= 100_000, "plotted-members form value exceeds 100000 characters")
    try:
        series = json.loads(form["series"])
    except json.JSONDecodeError as error:
        fail(f"plotted-members form value is invalid JSON: {error}")
    plotted = load_json(ROOT / "submission" / "plotted_members.json")
    check(series == plotted, "family-form series differs from plotted_members.json")
    check(isinstance(series, list) and len(series) > 0, "plotted members must be a nonempty list")
    check(len(series) <= 12, "plotted members exceed the 12-curve limit")
    check(
        [curve.get("label") for curve in series]
        == ["q = 2", "q = 3", "q = 4", "q = 5", "q = 7"],
        "plotted curve labels changed",
    )

    total_points = 0
    for curve_index, curve in enumerate(series):
        where = f"curve {curve_index + 1}"
        check(isinstance(curve, dict), f"{where} must be an object")
        check(set(curve) == {"label", "points"}, f"{where} has unexpected fields")
        label = curve["label"]
        check(isinstance(label, str) and 0 < len(label.strip()) <= 80, f"{where} label invalid")
        label_match = re.fullmatch(r"q = (\d+)", label)
        if label_match is None:
            fail(f"{where} label format invalid")
        q = int(label_match.group(1))
        points = curve["points"]
        check(isinstance(points, list) and len(points) > 0, f"{where} points must be nonempty")
        previous_r = 1
        for point_index, point in enumerate(points):
            pwhere = f"{where}, point {point_index + 1}"
            check(isinstance(point, dict), f"{pwhere} must be an object")
            check(
                set(point) == {"parameter", "n", "rank", "alpha", "field"},
                f"{pwhere} has unexpected fields",
            )
            parameter = point["parameter"]
            check(
                isinstance(parameter, str) and 0 < len(parameter.strip()) <= 80,
                f"{pwhere} parameter invalid",
            )
            match = re.fullmatch(r"q = (\d+), r = (\d+)", parameter)
            if match is None:
                fail(f"{pwhere} parameter format invalid")
            point_q, r = map(int, match.groups())
            check(point_q == q == point["field"], f"{pwhere} field mismatch")
            check(r > previous_r, f"{pwhere} parameter order is not strictly increasing")
            previous_r = r
            n = point["n"]
            rank = point["rank"]
            check(isinstance(n, int) and 1 <= n <= 1_000_000, f"{pwhere} n invalid")
            check(isinstance(rank, int) and 0 <= rank <= n, f"{pwhere} rank invalid")
            check(point["n"] == family_size(q, r, 2), f"{pwhere} family size mismatch")
            check(point["rank"] == 2 * r + 1, f"{pwhere} family rank mismatch")
            alpha = exact_fraction(point["alpha"], f"{pwhere} alpha")
            check(alpha <= 2, f"{pwhere} alpha exceeds the HSW bound")
            check(alpha == exact_ratio(q, r, 2), f"{pwhere} alpha formula mismatch")
            check(
                isinstance(point["field"], int) and point["field"] >= 2,
                f"{pwhere} optional field must be an integer at least 2",
            )
            total_points += 1
            check(total_points <= 400, "plotted members exceed the 400-point total limit")

    check_website_submission_parity(form)


def vector_set_rank(vectors: tuple[tuple[int, ...], ...], q: int) -> int:
    if not vectors:
        return 0
    matrix = [list(coordinates) for coordinates in zip(*vectors)]
    return matrix_rank(matrix, q)


def enumerate_block_counts(q: int, r: int) -> tuple[int, int, int, int]:
    """Independently enumerate the four local projective-block definitions."""
    marked = (1,) + (0,) * (r - 1)
    points = [point for point in projective_representatives(q, r) if point != marked]
    b_value = sum(vector_set_rank(choice, q) == r for choice in combinations(points, r))
    c_value = sum(
        vector_set_rank(choice, q) == r - 1
        and vector_set_rank(choice + (marked,), q) == r
        for choice in combinations(points, r - 1)
    )
    h_value = sum(
        vector_set_rank(choice, q) == r - 1
        and vector_set_rank(choice + (marked,), q) == r
        for choice in combinations(points, r)
    )
    s_value = sum(vector_set_rank(choice, q) == r for choice in combinations(points, r + 1))
    return b_value, c_value, h_value, s_value


def check_independent_local_counts() -> None:
    for q, r in ((2, 3), (3, 3)):
        enumerated = enumerate_block_counts(q, r)
        check(enumerated[2] > 0 and enumerated[3] > 0, f"q={q}, r={r} is degenerate for h or s")
        check(enumerated == block_counts(q, r), f"independent local counts mismatch for q={q}, r={r}")


def canonical_projective_column(column: tuple[int, ...], q: int) -> tuple[int, ...]:
    pivot = next((value for value in column if value != 0), None)
    if pivot is None:
        fail("cannot normalize a zero column")
    scale = inv(pivot, q)
    return tuple(mul(scale, value, q) for value in column)


def check_generated_matrices() -> None:
    check(tuple(SUPPORTED_FIELDS) == EXPECTED_FIELDS, "supported matrix fields changed")
    for q in EXPECTED_FIELDS:
        for r in range(2, 5):
            for k in range(2, 5):
                context = f"generated matrix q={q}, r={r}, k={k}"
                matrix = build_internal_matrix(q, r=r, k=k)
                expected_rank = k * r + 1
                expected_n = family_size(q, r, k)
                check(len(matrix) == expected_rank, f"{context}: row count mismatch")
                check(all(len(row) == expected_n for row in matrix), f"{context}: column count mismatch")
                check(matrix_rank(matrix, q) == expected_rank, f"{context}: matrix is not full rank")
                check(
                    [row[0] for row in matrix] == [1] + [0] * (expected_rank - 1),
                    f"{context}: distinguished i column mismatch",
                )
                expected_j = [0] * expected_rank
                for block in range(k):
                    expected_j[1 + block * r] = 1
                check([row[1] for row in matrix] == expected_j, f"{context}: distinguished j column mismatch")

                normalized: set[tuple[int, ...]] = set()
                for column_index, column in enumerate(zip(*matrix)):
                    check(any(value != 0 for value in column), f"{context}: zero column {column_index}")
                    canonical = canonical_projective_column(column, q)
                    check(canonical not in normalized, f"{context}: parallel column {column_index}")
                    normalized.add(canonical)

    for q, r, k in ((2, 2, 2), (3, 2, 2), (4, 3, 3), (5, 2, 4), (7, 3, 2)):
        stream = io.StringIO()
        write_encoded_matrix(stream, q, r=r, k=k)
        streamed = json.loads(stream.getvalue())
        check(streamed == encoded_matrix(q, r=r, k=k), f"streamed/dense matrix mismatch for q={q}, r={r}, k={k}")


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
    for q, r, k in ((2, 2, 2), (2, 2, 3), (3, 2, 2)):
        check(
            brute_force_basis_cells(q, r, k) == basis_cell_counts(q, r, k),
            f"full basis-cell enumeration mismatch for q={q}, r={r}, k={k}",
        )


def check_markdown_style() -> None:
    # WEBSITE_SUBMISSION.md is a literal copy of website form fields, where
    # MathJax inline delimiters are required. Ordinary repository Markdown
    # continues to use dollar delimiters.
    forbidden_ordinary = ("\\(", "\\)", "\\[", "\\]")
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        if path.name != "WEBSITE_SUBMISSION.md":
            for token in forbidden_ordinary:
                check(token not in text, f"{path.relative_to(ROOT)} contains forbidden {token!r}")
        check("\\operatorname" not in text, f"{path.relative_to(ROOT)} uses \\operatorname")
        check("\\operatername" not in text, f"{path.relative_to(ROOT)} uses misspelled \\operatername")

    for path in ROOT.rglob("*.json"):
        text = path.read_text(encoding="utf-8")
        check("\\operatorname" not in text, f"{path.relative_to(ROOT)} uses \\operatorname")
        check("\\operatername" not in text, f"{path.relative_to(ROOT)} uses misspelled \\operatername")


def check_all_json_parses() -> None:
    for path in ROOT.rglob("*.json"):
        load_json(path)


def main() -> None:
    check_closed_formulas()
    _, records = load_database_snapshot()
    check_old_special_case_data(records)
    check_fixed_field_data(records)
    check_submission_payload()
    check_independent_local_counts()
    check_generated_matrices()
    check_small_brute_force_counts()
    check_markdown_style()
    check_all_json_parses()
    print("all checks passed")


if __name__ == "__main__":
    main()
