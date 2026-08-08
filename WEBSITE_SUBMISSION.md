# Website submission instructions

Target: <https://matroid-correlation-constants.icarm.cloud/?maxn=1000>

Use the **Infinite family** form.  This is not a concrete-verifier submission:
the two record-improving members have $n=50$ and $n=149$, while the family
claim is proved uniformly from the construction and basis-cell count.

The proposal must be classified as a **certified lower bound** (`lower`), not an
exact full-invariant claim.  The proof establishes one distinguished-pair ratio
for every prime power $q$; it does not establish
$\overline{\alpha}(M_q)=R_{ij}(M_q)$ for every $q$.

## Exact form fields

The machine-readable copy is
[`submission/family_form.json`](submission/family_form.json).  Enter these
values in the family form.

### Family name

```text
Three-punctured-line affine-fibre matroids
```

### Short chart name

```text
Three punctured lines
```

### Claim type

```text
lower
```

### Parameter

```text
prime powers $q\ge 2$; the plotted members are restricted to the record-improving cases $q=4$ and $q=7$
```

### Formula

```text
\overline{\alpha}(M_q)\ge R_{ij}(M_q)=\frac{6(q+1)}{5q+6}
```

### Size and rank

```text
|E(M_q)|=3q^2+2,\qquad \operatorname{rk}(M_q)=7
```

### Supremum

```text
6/5
```

### Supremum status

```text
approached
```

### Summary

```text
For every prime power q, an explicit rank-7 GF(q)-representable matroid has a distinguished-pair ratio 6(q+1)/(5q+6), increasing to 6/5. The plotted members are exactly the current-record improvements: q=4 gives 15/13 on 50 elements, and q=7 gives 48/41 on 149 elements.
```

### Construction

```text
Let F=GF(q), W=U_1 direct-sum U_2 direct-sum U_3 with U_r=<a_r,z_r>, and j-bar=a_1+a_2+a_3. In V=F e_0 direct-sum W, include i=e_0 and j=(0,j-bar). On each projective line PG(U_r), delete [a_r], retain the q directions represented by z_r and a_r+s z_r for nonzero s in F, and replace every retained direction g by its complete affine fibre {t e_0+g:t in F}. The resulting vector matroid has rank 7 and 3q^2+2 elements.
```

### What the curve shows

```text
This is a dashed certified lower-bound curve: it records the exact distinguished-pair value R_ij(M_q), not a proved formula for the full invariant $\overline{\alpha}(M_q)$. Only q=4 and q=7 are plotted because these are the members that strictly improve the website's field records in the 2026-08-08 database snapshot. The general formula tends increasingly to 6/5 and never attains it.
```

### Proof status

```text
Complete proof of the construction, rank, four basis-cell counts, distinguished-pair formula, monotonicity, and supremum is provided in the linked repository. The q=4 and q=7 record comparisons are exact. Equality with the full invariant of M_q for general q is not claimed.
```

### Proof URL

```text
https://github.com/dylan0301/Three-punctured-line-affine-fibre-matroids/blob/main/PROOF.md
```

### Plotted members

Paste the following JSON exactly.  It intentionally contains only GF(4) and
GF(7).

```json
[{"parameter":"q = 4","n":50,"rank":7,"alpha":"15/13","field":4},{"parameter":"q = 7","n":149,"rank":7,"alpha":"48/41","field":7}]
```

### Discovered by

```text
Jeewon Kim
```

### Discovery date

```text
2026-08-06
```

### AI used

```text
yes
```

### AI model

```text
GPT-5.6 Pro
```

### AI role

```text
AI assisted with computational exploration, exact finite-field counting, symbolic simplification, proof auditing, record comparison, and preparation of reproducible submission files. The submitted claim is the distinguished-pair lower bound proved in the linked writeup.
```

### Public AI conversation

```text
https://chatgpt.com/share/6a7698a2-c044-83ee-9851-1fcaac81cf25?ogimg=plain
```

## Exact record comparisons

The website database snapshot used here is dated 2026-08-08.

### GF(4)

$$
\frac{15}{13}-\frac87=\frac1{91}>0.
$$

The proposed member has rank $7$, size $50$, and a proved distinguished-pair
lower bound $15/13$.

### GF(7)

$$
\frac{48}{41}-\frac{280043}{243256}
=\frac{194525}{9973496}>0.
$$

The proposed member has rank $7$, size $149$, and a proved
distinguished-pair lower bound $48/41$.

## Before submitting

The two representation matrices can be generated deterministically with

```bash
python3 scripts/generate_matrix.py 4
python3 scripts/generate_matrix.py 7
```

Run

```bash
python3 scripts/verify.py
```

and confirm that it prints `all checks passed`.  Then copy the values from
`submission/family_form.json` into the website's Infinite family form.  The
proposal will be pending until a site administrator reviews the mathematics.
