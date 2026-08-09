# Website submission instructions

Target: <https://matroid-correlation-constants.icarm.cloud/#submit-family>

Use the **Infinite family** form. The family theorem is proved uniformly, but
most useful finite members are far beyond the concrete verifier's ground-set
limit. The submission must be classified as a certified lower bound: it proves
the exact value of one distinguished-pair ratio, not the full invariant of
every member.

The exact machine-readable payload is
[`submission/family_form.json`](submission/family_form.json). The values below
are a human-readable guide; the JSON file is the authoritative copy-paste
source.

## Submission classification

- Claim type: `lower`
- Supremum: `4/3`
- Supremum status: `iterated limit`
- Finite family submitted: $M_{q,2,r}$ for prime powers $q$ and $r\ge2$
- Fixed-field limit: $4q/(3q+1)$ as $r\to\infty$
- Global displayed supremum: $4/3$ as $q\to\infty$ afterwards

Every plotted point is an actual finite-$r$ ratio. The value $4q/(3q+1)$ is
not inserted as a finite point.

## Exact form fields

### Family name

```text
Punctured-projective-block affine-fibre matroids
```

### Short chart name

```text
Punctured PG fibres
```

### Claim type

```text
lower
```

### Parameter

```text
prime powers q and integers r >= 2; the submitted curves use the k = 2 subfamily
```

### Formula

The website requests TeX without delimiters in this field:

```text
R_{ij}(M_{q,r})=\frac{4w_{q,r}}{1+2/(q-1)+2w_{q,r}},\quad x_{q,r}=\frac{r}{(q^r-1)/(q-1)-r},\quad w_{q,r}=\frac{q(r-x_{q,r})/(q-1)+rx_{q,r}+(r-1)x_{q,r}^2/2}{r+1},\quad \lim_{r\to\infty}R_{ij}(M_{q,r})=\frac{4q}{3q+1}
```

### Size and rank

The website again requests TeX without delimiters:

```text
|E(M_{q,r})|=\frac{2q^2(q^{r-1}-1)}{q-1}+2,\qquad \mathrm{rk}(M_{q,r})=2r+1
```

### Supremum

```text
4/3
```

### Supremum status

```text
iterated limit
```

### Summary

```text
For every prime power q and finite r >= 2, an explicit GF(q)-representable matroid has the displayed exact distinguished-pair ratio. As r tends to infinity this gives the fixed-field bound alpha-bar(GF(q)) >= 4q/(3q+1); these bounds tend to 4/3 as q tends to infinity.
```

### Construction

```text
Let F=GF(q). Take two independent r-dimensional spaces U_1,U_2 with marked nonzero vectors a_1,a_2, and let W=U_1 direct-sum U_2 and V=F e_0 direct-sum W. In each PG(U_l), delete [a_l]. For every retained projective direction g, include its complete affine fibre {t e_0+g:t in F}. Finally include i=e_0 and j=a_1+a_2. The vector matroid of these columns has rank 2r+1 and the stated size. A more general proof with k blocks contains the earlier three-punctured-line family as (k,r)=(3,2).
```

### What the curve shows

```text
Each grouped curve fixes q and plots exact finite-r distinguished-pair values, so every point is realized by a finite matroid represented directly over GF(q). The curve is dashed because the proof gives alpha-bar(M_{q,r}) >= R_ij(M_{q,r}), not equality with the full invariant. A fixed-q curve converges to 4q/(3q+1), and the resulting fixed-field bounds converge to the iterated supremum 4/3 as q grows. The finite values need not be monotone in r.
```

### Proof status

```text
Complete proof of the representation, rank, size, four basis-cell counts, exact finite ratio, fixed-q limit, optimization over the block count, iterated supremum, and the old (k,r)=(3,2) special case is provided in the linked repository. Equality with the full invariant of each finite member is not claimed.
```

### Proof URL

```text
https://github.com/dylan0301/Punctured-projective-block-affine-fibre-matroids/blob/main/PROOF.md
```

### Plotted members

The form's `series` field is a JSON-encoded string. Copy it from
[`submission/family_form.json`](submission/family_form.json), or use the
formatted equivalent in
[`submission/plotted_members.json`](submission/plotted_members.json). It
contains five grouped curves, for $q=2,3,4,5,7$, and only exact finite values.
Every point includes its actual ground-set size, rank, exact reduced fraction,
and base-field tag.

### Discovery record

```text
Discovered by: Jeewon Kim
Discovery date: 2026-08-09
AI used: yes
AI model: GPT-5.6 Pro
Public AI conversation: https://chatgpt.com/share/6a77e552-a1dc-83e8-b0bb-05ff004d1084
```

### AI role

```text
AI assisted with mathematical exploration, exact projective-geometry and affine-fibre counting, asymptotic simplification, proof auditing, record comparison, and preparation of reproducible submission files. The submitted claim is the distinguished-pair lower bound proved in the linked writeup.
```

The linked public conversation documents the higher-rank construction, its
exact counting formula, asymptotic bound, finite witnesses, and verification
status.

## Previous result recovered exactly

The proof treats $k$ punctured blocks before specializing the submitted curves
to $k=2$. At $(k,r)=(3,2)$ it recovers the former construction:

$$
|E(M_{q,3,2})|=3q^2+2,
\qquad
\mathrm{rk}(M_{q,3,2})=7,
$$

and

$$
R_{ij}(M_{q,3,2})=\frac{6(q+1)}{5q+6}.
$$

Thus the old result is a literal finite-parameter special case, not merely an
analogy or an asymptotic consequence.

## Exact fixed-field comparisons

The live website database snapshot used here is dated 2026-08-09.

### GF(4)

$$
\frac{16}{13}-\frac87=\frac8{91}>0.
$$

The first plotted $k=2$ witness above $8/7$ is $r=5$, with rank $11$, size
$2722$, and ratio $50590/44111$.

### GF(5)

$$
\frac54-\frac{4664}{4007}=\frac{1379}{16028}>0.
$$

The first plotted $k=2$ witness above $4664/4007$ is $r=5$, with rank $11$,
size $7802$, and ratio $104950/90111$.

### GF(7)

$$
\frac{14}{11}-\frac{280043}{243256}
=\frac{325111}{2675816}>0.
$$

The first plotted $k=2$ witness above $280043/243256$ is $r=4$, with rank
$9$, size $5588$, and ratio $3068/2623$.

For GF(2), the limiting bound ties $8/7$. For GF(3),
$6/5<100/81$, so neither is described as a strict improvement.

## Difference from the website's geometry families

Every finite member here has an explicit representation over the stated base
field $\mathbf F_q$. The website's affine- and projective-geometry
double-extension families may require passing to a larger extension field.
Their limit $4q^2/(3q^2+1)$ therefore does not by itself give a bound for the
correlation constant of the fixed field $\mathbf F_q$.

## Before submitting

Run

```bash
python3 scripts/verify.py
python3 -m compileall scripts
git diff --check
```

and confirm that the verifier prints `all checks passed`. The proposal remains
pending until a site administrator reviews the proof.
