# Three-punctured-line affine-fibre matroids

This repository contains the proof and submission data for one explicit family
of finite-field-representable matroids.

For every prime power \(q\ge 2\), the construction gives a rank-\(7\)
\(\mathbf F_q\)-representable matroid \(M_q\) on \(3q^2+2\) elements with a
distinguished pair \(i,j\) satisfying

\[
\overline{\alpha}(M_q)\;\ge\;R_{ij}(M_q)
   =\frac{6(q+1)}{5q+6}.
\]

The displayed quantity is a proved **distinguished-pair lower bound**.  The
repository does not claim that it is the full correlation constant of \(M_q\)
for every \(q\).

## Record-improving members

The website submission deliberately plots only the two members that improve the
field records displayed by the Matroid Correlation Constants website on
2026-08-08.

| field | member | size | rank | proved lower bound | previous website record | exact improvement |
|---:|---:|---:|---:|---:|---:|---:|
| \(\mathbf F_4\) | \(M_4\) | 50 | 7 | \(15/13\) | \(8/7\) | \(1/91\) |
| \(\mathbf F_7\) | \(M_7\) | 149 | 7 | \(48/41\) | \(280043/243256\) | \(194525/9973496\) |

Thus

\[
\overline{\alpha}(\mathbf F_4)\ge \frac{15}{13}>\frac87,
\qquad
\overline{\alpha}(\mathbf F_7)\ge \frac{48}{41}>
\frac{280043}{243256}.
\]

The comparison snapshot is recorded in
[`data/improved_members.json`](data/improved_members.json).  The live source is
<https://matroid-correlation-constants.icarm.cloud/database.json>.

## Website submission route

The two relevant matroids have \(n=50\) and \(n=149\), so they are presented
through the website's **Infinite family** form rather than as small concrete
matroid submissions.  The form must use:

- claim type: `lower`;
- supremum: `6/5`;
- supremum status: `approached`;
- plotted members: only \(q=4\) and \(q=7\).

Use [`WEBSITE_SUBMISSION.md`](WEBSITE_SUBMISSION.md) for the field-by-field
copying instructions and [`submission/family_form.json`](submission/family_form.json)
for the exact form payload.

## Files

- [`PROOF.md`](PROOF.md): complete construction and basis-cell count.
- [`WEBSITE_SUBMISSION.md`](WEBSITE_SUBMISSION.md): submission classification,
  exact record comparisons, and copy-paste fields.
- [`submission/family_form.json`](submission/family_form.json): exact website
  form keys and values.
- [`submission/plotted_members.json`](submission/plotted_members.json): the two
  plotted record-improving members.
- [`data/improved_members.json`](data/improved_members.json): exact basis-cell
  counts and record comparisons.
- [`scripts/verify.py`](scripts/verify.py): dependency-free exact checks of all
  formulas and submission data.
- [`scripts/generate_matrix.py`](scripts/generate_matrix.py): deterministic row-matrix
  generator for the two submitted members over GF(4) and GF(7).

Run

```bash
python3 scripts/verify.py
```

to verify the closed formulas, the \(q=4,7\) basis-cell counts, both strict
record comparisons, the generated representation matrices, and the website payload
schema.  For example, generate the GF(4) representation with

```bash
python3 scripts/generate_matrix.py 4
```

## Attribution and AI disclosure

Discovered by Jeewon Kim, with GPT-5.6 Pro used for computational exploration,
exact symbolic simplification, proof auditing, and preparation of the public
submission materials.  The public discovery conversation is linked in the
website payload.
