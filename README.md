# Punctured-projective-block affine-fibre matroids

This repository proves an explicit fixed-field lower bound for matroid
correlation constants. For every prime power $q$,

$$
\boxed{\overline{\alpha}(\mathbf F_q)\ge \frac{4q}{3q+1}}.
$$

The bound comes from finite matroids, not from an infinite-rank object. For
every $r\ge2$, the construction gives a finite rank-$(2r+1)$,
$\mathbf F_q$-representable matroid $M_{q,r}$ with a distinguished pair
$i,j$. Its exact finite ratio is proved in [`PROOF.md`](PROOF.md), and

$$
\lim_{r\to\infty}R_{ij}(M_{q,r})=\frac{4q}{3q+1}.
$$

Taking the supremum over the finite members gives the field bound. No
monotonicity in $r$ is claimed; the sequence can initially decrease. Taking
$q\to\infty$ afterwards gives the displayed family's iterated supremum
$4/3$.

## General construction

The proof treats a three-parameter family $M_{q,k,r}$ for every prime power
$q$ and integers $k,r\ge2$. It uses $k$ copies of
$\mathrm{PG}(r-1,q)$ with one marked point deleted from each copy, replaces
every retained projective direction by its complete $q$-element affine fibre,
and adds a distinguished pair. The resulting matroid has

$$
\mathrm{rk}(M_{q,k,r})=kr+1,
\qquad
|E(M_{q,k,r})|
=\frac{kq^2(q^{r-1}-1)}{q-1}+2.
$$

For fixed $q,k$,

$$
\lim_{r\to\infty}R_{ij}(M_{q,k,r})
=\frac{k^2q}{(k^2-k+1)q+k-1}.
$$

Among integers $k\ge2$, this limit is largest at $k=2$, which gives
$4q/(3q+1)$.

## The previous result is a special case

The original three-punctured-line affine-fibre matroid is exactly
$M_{q,3,2}$. Substitution gives

$$
\mathrm{rk}(M_{q,3,2})=7,
\qquad
|E(M_{q,3,2})|=3q^2+2,
$$

and recovers the previous exact finite formula

$$
R_{ij}(M_{q,3,2})=\frac{6(q+1)}{5q+6}.
$$

The earlier GF(4) and GF(7) basis-cell certificates are retained in
[`data/improved_members.json`](data/improved_members.json) as regression data
for this special case.

## Current fixed-field improvements

Against the website database snapshot of 2026-08-09, the limiting bounds are
strict improvements for GF(4), GF(5), and GF(7).

| field | new fixed-field lower bound | website record | exact difference | first plotted $k=2$ witness above the record |
|---:|---:|---:|---:|---:|
| $\mathbf F_4$ | $16/13$ | $8/7$ | $8/91$ | $r=5$, $50590/44111$ |
| $\mathbf F_5$ | $5/4$ | $4664/4007$ | $1379/16028$ | $r=5$, $104950/90111$ |
| $\mathbf F_7$ | $14/11$ | $280043/243256$ | $325111/2675816$ | $r=4$, $3068/2623$ |

For GF(2), the limit equals $8/7$. For GF(3), the limit $6/5$ is below the
website's concrete value $100/81$. Exact comparisons and finite witnesses are
stored in [`data/fixed_field_bounds.json`](data/fixed_field_bounds.json).

Every finite member here is represented directly over the stated field
$\mathbf F_q$. This differs from the website's affine- and projective-geometry
double-extension families, whose free extension and coextension may require a
larger field. Their larger-looking geometry limit therefore does not imply a
fixed-$\mathbf F_q$ bound.

## Website submission

The result belongs in the website's **Infinite family** form. It is a
certified distinguished-pair lower bound, not a claim that $i,j$ maximizes the
full invariant of every finite member. The submission uses:

- claim type `lower`;
- supremum `4/3`;
- supremum status `iterated limit`;
- grouped GF(2), GF(3), GF(4), GF(5), and GF(7) curves containing only exact
  finite-$r$ values.

See [`WEBSITE_SUBMISSION.md`](WEBSITE_SUBMISSION.md) and the exact payload in
[`submission/family_form.json`](submission/family_form.json). The plotted data
are in [`submission/plotted_members.json`](submission/plotted_members.json).

## Verification and matrix generation

Run

```bash
python3 scripts/verify.py
```

to check the local counting identities, exact finite ratios, limiting
formulas, old special case, record comparisons, submission schema, matrix
ranks, small brute-force basis counts, and Markdown style constraints.

The deterministic generator supports the five plotted fields. For example,

```bash
python3 scripts/generate_matrix.py 4 --r 5 --k 2
python3 scripts/generate_matrix.py 4 --r 2 --k 3
```

generate respectively a new-family member and the old three-line special
case.

## Attribution and AI disclosure

Discovered by Jeewon Kim. GPT-5.6 Pro assisted with mathematical exploration,
exact counting, asymptotic simplification, proof auditing, and preparation of
the reproducible submission materials. The research conversation is available
at [ChatGPT's public share link](https://chatgpt.com/share/6a77e552-a1dc-83e8-b0bb-05ff004d1084).
