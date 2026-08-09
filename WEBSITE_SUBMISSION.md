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
- Reverse fixed-$r$ limit: $4r/(3r+1)$ as $q\to\infty$
- Global displayed supremum: the unattained value $4/3$ in either iterated
  order

Every plotted point is an actual finite-$r$ ratio. The value $4q/(3q+1)$ is
not inserted as a finite point. The website status `iterated limit` says that
the supremum is limiting rather than attained; it does not prescribe a unique
order of limits.

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
prime powers \(q\) and integers \(r\ge 2\); the submitted curves use the \(k=2\) subfamily
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
For every prime power \(q\) and finite \(r\ge 2\), an explicit \(\mathbf F_q\)-representable matroid has the displayed exact distinguished-pair ratio. As \(r\to\infty\), this gives the fixed-field bound \(\overline{\alpha}(\mathbf F_q)\ge \frac{4q}{3q+1}\); these bounds tend to \(\frac43\) as \(q\to\infty\).
```

### Construction

```text
Let \(F=\mathbf F_q\). Take two independent \(r\)-dimensional spaces \(U_1,U_2\) with marked nonzero vectors \(a_1,a_2\), and put \(W=U_1\oplus U_2\) and \(V=F e_0\oplus W\). In each \(\mathrm{PG}(U_\ell)\), delete \([a_\ell]\). For every retained projective direction \(g\), include its complete affine fibre \(\{t e_0+g:t\in F\}\). Finally include \(i=e_0\) and \(j=a_1+a_2\). The vector matroid of these columns has rank \(2r+1\) and the stated size.
```

### What the curve shows

```text
Each grouped curve fixes \(q\) and plots exact finite-\(r\) distinguished-pair values, so every point is realized by a finite matroid represented directly over \(\mathbf F_q\). The curve is dashed because the proof gives \(\overline{\alpha}(M_{q,r})\ge R_{ij}(M_{q,r})\), not equality with the full invariant. A fixed-\(q\) curve converges to \(\frac{4q}{3q+1}\), and these fixed-field bounds converge to the displayed, unattained two-parameter supremum \(\frac43\) as \(q\) grows. For fixed \(r\), the reverse limit is \(\lim_{q\to\infty}R_{ij}(M_{q,r})=\frac{4r}{3r+1}\), so the opposite iterated order also tends to \(\frac43\). The finite values need not be monotone in \(r\).
```

### Proof status

```text
A complete analytic proof of the representation, rank, size, four basis-cell counts, exact finite ratio, fixed-\(q\) and fixed-\(r\) limits, optimization over the block count, and unattained two-parameter supremum is provided in the linked repository. The verifier supplies independent small-case enumeration and regression checks; it is not a substitute for the universal proof. Equality with the full invariant of each finite member is not claimed.
```

### Proof URL

```text
https://github.com/dylan0301/Punctured-projective-block-affine-fibre-matroids/blob/8b79fef1ceef5a6d90622b22d8167360b503e229/PROOF.md
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

## Exact fixed-field comparisons

The website database response used here is frozen in
[`data/website_database_2026-08-09.json`](data/website_database_2026-08-09.json),
with retrieval provenance and a SHA-256 digest in
[`data/website_database_snapshot_manifest.json`](data/website_database_snapshot_manifest.json).

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
python3 -m pip install -r requirements-dev.txt
python3 scripts/verify.py
python3 -O scripts/verify.py
python3 -m compileall -q scripts
mypy scripts
git diff --check
```

and confirm that the verifier prints `all checks passed`. The proposal remains
pending until a site administrator reviews the proof. These commands perform
validation and regression checks; the linked analytic proof establishes the
uniform theorem.
