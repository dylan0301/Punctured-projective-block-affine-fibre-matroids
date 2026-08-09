# Proof for the punctured-projective-block affine-fibre family

## 1. Main theorem

Let $q$ be a prime power and let $k,r\ge2$. There is a finite
$\mathbf F_q$-representable matroid $M_{q,k,r}$ with a distinguished pair
$i,j$ such that

$$
\mathrm{rk}(M_{q,k,r})=kr+1
$$

and

$$
|E(M_{q,k,r})|
=\frac{kq^2(q^{r-1}-1)}{q-1}+2.
$$

Put

$$
v=\frac{q^r-1}{q-1},
\qquad
x=\frac{r}{v-r},
$$

and define

$$
w=w_{q,r}
=\frac{1}{r+1}
\left(
\frac{q(r-x)}{q-1}+rx+\frac{r-1}{2}x^2
\right).
$$

Then the exact unweighted correlation ratio of the distinguished pair is

$$
\boxed{
R_{ij}(M_{q,k,r})
=\frac{k^2w}{1+k/(q-1)+k(k-1)w}
}.
$$

For fixed $q,k$ this gives

$$
\boxed{
\lim_{r\to\infty}R_{ij}(M_{q,k,r})
=\frac{k^2q}{(k^2-k+1)q+k-1}
}.
$$

For the submitted $k=2$ subfamily, fixing $r$ instead gives the reverse
limit

$$
\boxed{
\lim_{q\to\infty}R_{ij}(M_{q,2,r})
=\frac{4r}{3r+1}
},
$$

where $q$ tends to infinity through prime powers. Thus both iterated orders
converge to $4/3$. The exact finite $k=2$ values have two-parameter supremum
$4/3$, and no finite member attains it.

The general fixed-$q$ limit above is largest among integers $k\ge2$ when
$k=2$. Consequently,

$$
\boxed{
\overline{\alpha}(\mathbf F_q)
\ge \frac{4q}{3q+1}
}.
$$

This last inequality is a supremum statement over finite matroids: for every
finite $r$, $M_{q,2,r}$ is an actual finite $\mathbf F_q$-representable
matroid, and its distinguished-pair ratio converges to the displayed value.
There is no use of an infinite-rank matroid.

For completeness, if $\mathcal B(M)$ is the set of bases of $M$, write

$$
\begin{aligned}
N_{11}&=|\{B\in\mathcal B(M):i,j\in B\}|,\\
N_{10}&=|\{B\in\mathcal B(M):i\in B,\ j\notin B\}|,\\
N_{01}&=|\{B\in\mathcal B(M):i\notin B,\ j\in B\}|,\\
N_{00}&=|\{B\in\mathcal B(M):i,j\notin B\}|.
\end{aligned}
$$

Then

$$
R_{ij}(M)=\frac{N_{11}N_{00}}{N_{10}N_{01}}.
$$

Call a pair $e,f$ **eligible** if $e\ne f$ and neither element is a loop or a
coloop. For such a pair, basis exchange ensures that $N_{10}$ and $N_{01}$
are positive, so the displayed ratio is defined.

The unweighted matroid invariant is

$$
\overline{\alpha}(M)=\max_{e\ne f}R_{ef}(M),
$$

where the maximum ranges over eligible pairs. If $M$ has no eligible pair,
set $\overline{\alpha}(M)=0$. Finally,

$$
\overline{\alpha}(F)
=\sup\{\overline{\alpha}(M):M\text{ is a finite }F\text{-representable matroid}\}.
$$

Thus $\overline{\alpha}(M_{q,k,r})\ge R_{ij}(M_{q,k,r})$. The usual weighted
correlation constant also dominates the unweighted one, so every lower bound
proved here remains valid for the weighted field constant. Equality between
$R_{ij}$ and the full invariant of each finite member is not asserted.

## 2. Construction

Let $F=\mathbf F_q$. Take $k$ mutually independent $r$-dimensional spaces

$$
U_\ell=\langle a_\ell,u_{\ell,2},\ldots,u_{\ell,r}\rangle_F
\qquad (1\le\ell\le k).
$$

Let $e_0$ be a basis vector for an additional one-dimensional $F$-space, and
put

$$
W=\bigoplus_{\ell=1}^k U_\ell,
\qquad
V=F e_0\oplus W,
\qquad
\bar j=a_1+\cdots+a_k.
$$

In every projective geometry $\mathrm{PG}(U_\ell)$, delete the marked point
$[a_\ell]$. Choose one nonzero vector representative for each retained
projective point; call the resulting set $\mathcal P_\ell$. For every
$g\in\mathcal P_1\cup\cdots\cup\mathcal P_k$, include the complete affine
fibre

$$
F_g=\{t e_0+g:t\in F\}\subset V.
$$

Finally include

$$
i=e_0,
\qquad
j=(0,\bar j).
$$

Let $M_{q,k,r}$ be the vector matroid of these columns. The definition is
independent of the chosen nonzero representatives up to rescaling and
reparametrizing each complete fibre.

The number of projective points in $\mathrm{PG}(r-1,q)$ is

$$
v=\frac{q^r-1}{q-1}.
$$

There are $v-1$ retained directions in each of the $k$ blocks, and every
direction supplies $q$ columns. Therefore

$$
|E(M_{q,k,r})|
=kq(v-1)+2
=\frac{kq^2(q^{r-1}-1)}{q-1}+2.
$$

The retained projective points span each $U_\ell$: after deleting one point,
the remaining projective geometry is not contained in a hyperplane. Hence the
fibre columns span $W$, and adjoining $i=e_0$ spans $V$. Thus

$$
\mathrm{rk}(M_{q,k,r})=\dim_F V=kr+1.
$$

Let

$$
\pi:V\longrightarrow W,
\qquad
\pi(t e_0+w)=w.
$$

Its kernel is $F e_0$, and it collapses every affine fibre $F_g$ to the
single quotient direction $g$.

## 3. Four local counts in one punctured block

Fix one $r$-dimensional block $U$ with marked nonzero vector $a$, and let

$$
P=\mathrm{PG}(U)\setminus\{[a]\}.
$$

We need four numbers:

- $b$: the number of $r$-element bases contained in $P$;
- $c$: the number of independent $(r-1)$-subsets $X\subset P$ with
  $a\notin\langle X\rangle$;
- $h$: the number of $r$-subsets $X\subset P$ with
  $\dim\langle X\rangle=r-1$ and $a\notin\langle X\rangle$;
- $s$: the number of spanning $(r+1)$-subsets of $P$.

Let $G_m$ denote the number of unordered projective bases of
$\mathrm{PG}(m-1,q)$. Explicitly,

$$
G_m=\frac{|\mathrm{GL}(m,q)|}{(q-1)^m m!}
=\frac{1}{(q-1)^m m!}
\prod_{t=0}^{m-1}(q^m-q^t).
$$

Set $G=G_r$. By point transitivity, each of the $v$ projective points lies in
exactly $rG/v$ projective bases. Removing $[a]$ therefore gives

$$
c=\frac{rG}{v},
\qquad
b=G-c=\frac{(v-r)G}{v},
$$

and hence

$$
x:=\frac cb=\frac{r}{v-r}.
$$

To express $h$ and $s$, define for $m\ge1$

$$
z_m
=\sum_{t=2}^{m}
\binom mt\frac{(q-1)^{t-1}}{t+1}.
$$

The empty sum gives $z_1=0$.

### Lemma 3.1: spanning one-more-than-bases

The number of spanning $(m+1)$-subsets of $\mathrm{PG}(m-1,q)$ is
$G_mz_m$.

#### Proof

Double-count pairs $(B,S)$ in which $B$ is a projective basis and $S$ is a
spanning $(m+1)$-set containing $B$. Fix a basis
$B=\{b_1,\ldots,b_m\}$. An extra projective point $p\notin B$ has an
expression in the basis whose support has some size $t\ge2$. After projective
rescaling, the number of points with a prescribed support of size $t$ is
$(q-1)^{t-1}$. Thus the number of choices with support size $t$ is

$$
\binom mt(q-1)^{t-1}.
$$

For $S=B\cup\{p\}$, the unique projective dependence has support size $t+1$.
Exactly the $t+1$ sets obtained by deleting one point of this circuit are
bases contained in $S$. Dividing the count for each support size by $t+1$
and summing proves the formula. $\square$

The binomial identity

$$
\sum_{t=0}^{m}\binom mt\frac{(q-1)^t}{t+1}
=\frac{q^{m+1}-1}{(m+1)(q-1)}
$$

also gives the closed form

$$
z_m
=\frac{1}{q-1}
\left(
\frac{q^{m+1}-1}{(m+1)(q-1)}
-1-\frac{m(q-1)}2
\right).
$$

Every $c$-set spans a hyperplane avoiding $[a]$. Within each such hyperplane,
Lemma 3.1 with dimension $r-1$ shows that the ratio of spanning $r$-sets to
bases is $z_{r-1}$. Therefore

$$
\frac hb=\frac cb\frac hc=xz_{r-1}.
$$

Write

$$
e:=\frac hb=xz_{r-1}.
$$

There are $Gz_r$ spanning $(r+1)$-sets in the full projective geometry. A
spanning $(r+1)$-set containing $[a]$ becomes, after deleting $[a]$, either a
basis counted by $b$ or a rank-$(r-1)$ set counted by $h$. Conversely, every
set of either type becomes spanning after $[a]$ is restored. Hence

$$
s=Gz_r-b-h.
$$

Since $G/b=1+c/b=1+x$, we obtain

$$
y:=\frac sb=(1+x)z_r-1-e.
$$

These formulas show directly that all four local counts are exact integers,
even though their normalized ratios need not be integers.

## 4. Quotient and affine-lifting lemmas

### Lemma 4.1: when $\bar j$ enters a blockwise span

Let

$$
S\subseteq U_1\cup\cdots\cup U_k,
$$

so every vector in $S$ is supported in a single block, and put
$S_\ell=S\cap U_\ell$. Then

$$
\langle S\rangle
=\bigoplus_{\ell=1}^k\langle S_\ell\rangle.
$$

Moreover,

$$
\bar j\in\langle S\rangle
\quad\Longleftrightarrow\quad
a_\ell\in\langle S_\ell\rangle
\text{ for every }\ell.
$$

#### Proof

Both assertions follow from the direct-sum decomposition
$W=U_1\oplus\cdots\oplus U_k$ and the equality
$\bar j=a_1+\cdots+a_k$. Every application below takes $S$ from the
block-supported quotient directions
$\mathcal P_1\cup\cdots\cup\mathcal P_k$, so the hypothesis is satisfied.
$\square$

### Lemma 4.2: affine lifting of a unique relation

Suppose quotient vectors $w_1,\ldots,w_m\in W$ have rank $m-1$, with unique
relation up to scale

$$
\sum_{t=1}^m d_t w_t=0.
$$

For lifts $v_t=\lambda_t e_0+w_t$, the vectors $v_1,\ldots,v_m$ are
independent exactly when

$$
\sum_{t=1}^m d_t\lambda_t\ne0.
$$

If the $\lambda_t$ range independently over $F$, exactly
$(q-1)q^{m-1}$ choices are independent.

#### Proof

Any relation among the $v_t$ projects to a scalar multiple of the unique
relation among the $w_t$. The coefficient of $e_0$ in that scalar multiple is
the displayed linear form. It is a nonzero linear functional on $F^m$, so its
kernel has $q^{m-1}$ elements. $\square$

We also use three immediate observations.

1. An independent set containing $i=e_0$ contains at most one point from any
   affine fibre.
2. An independent set not containing $i$ contains at most two points from any
   fibre, since a fibre lies in the two-dimensional space $\langle e_0,g\rangle$.
3. For every $X\subset V$,

   $$
   \mathrm{rk}_V(X)\le \mathrm{rk}_W(\pi(X))+1.
   $$

## 5. The four basis cells

We now count bases of $M_{q,k,r}$ according to their intersection with
$\{i,j\}$. Define normalized quantities

$$
A_0=kcb^{k-1},
\qquad
B_0=b^k,
$$

$$
C_0
=b^k+khb^{k-1}+k(k-1)csb^{k-2}
+\frac{kr-1}{2}A_0,
$$

and

$$
D_0
=ksb^{k-1}+\frac{kr}{2}B_0.
$$

The factors $1/2$ are normalization artifacts from choosing two distinct
points in one fibre. The actual basis counts below are integers.

### 5.1. Bases containing both $i$ and $j$

After selecting $i,j$, choose $kr-1$ fibre points. Their quotient directions
must be distinct, and together with $\bar j$ they must form a basis of $W$.
The quotient directions themselves therefore have rank $kr-1$. Exactly one
block has rank $r-1$, the other $k-1$ blocks have rank $r$, and the deficient
block must not span its marked vector. Thus one block contributes a $c$-set
and every other block contributes a basis. There are

$$
A_0=kcb^{k-1}
$$

quotient configurations. The presence of $i$ makes all $q^{kr-1}$ affine
coordinates arbitrary, so

$$
N_{11}=q^{kr-1}A_0.
$$

### 5.2. Bases containing $i$ but not $j$

The $kr$ quotient directions must form a basis of $W$, so every block
contributes one of its $b$ bases. Hence

$$
N_{10}=q^{kr}B_0.
$$

### 5.3. Bases containing $j$ but not $i$

Choose $kr$ fibre points. If two fibres were doubled, there would be at most
$kr-2$ distinct quotient directions. Together with $\bar j$ they would have
quotient rank at most $kr-1$, so Observation 3 would give rank at most $kr$
upstairs. Therefore either all quotient directions are distinct or exactly one
direction is doubled.

Suppose first that all $kr$ directions are distinct. Their union with
$\bar j$ must have quotient rank $kr$. There are three disjoint types.

1. The directions themselves form a basis of $W$: $b^k$ choices.
2. One block contains an $h$-set and all other blocks contain bases:
   $khb^{k-1}$ choices.
3. One block contains a deficient $c$-set, a different block contains a
   spanning $(r+1)$-set, and all remaining blocks contain bases:
   $k(k-1)csb^{k-2}$ choices.

These are exhaustive. If the directions do not already form a basis as in
type 1, their rank is $kr-1$. The total quotient-rank deficiency and the
nullity of the selected directions are then both one. Thus exactly one block
has rank $r-1$, and exactly one block has one selected point more than its
rank. The excess occurs either in the deficient block, giving type 2, or in a
different full-rank block, giving type 3.

For each all-distinct configuration, the $kr+1$ projected vectors have a
unique relation. Its restriction to the fibre directions is nonzero, since a
relation supported only on the single nonzero vector $\bar j$ is impossible.
Lemma 4.2, with the affine coordinate of $j$ fixed at zero, therefore gives
$(q-1)q^{kr-1}$ independent lift choices.

Now suppose one direction is doubled. The $kr-1$ distinct directions together
with $\bar j$ must form a basis of $W$, giving $A_0$ configurations. There are
$kr-1$ choices for the doubled direction. For a fixed choice, selecting two
different points in that fibre and one point in each remaining fibre gives

$$
\binom q2 q^{kr-2}
=\frac12(q-1)q^{kr-1}
$$

choices. Subtracting the two doubled lifts produces a nonzero multiple of
$e_0$, while the remaining vectors project to a basis of $W$; hence every such
selection is independent.

Combining the two multiplicity types gives

$$
N_{01}=(q-1)q^{kr-1}C_0.
$$

### 5.4. Bases containing neither $i$ nor $j$

Choose $kr+1$ fibre points. Again, two doubled fibres would leave at most
$kr-1$ distinct quotient directions and could not give rank $kr+1$ upstairs.

If all directions are distinct, they must span $W$. The number selected
exceeds $\dim W$ by one, so exactly one block contributes a spanning
$(r+1)$-set and every other block contributes a basis. This gives
$ksb^{k-1}$ quotient configurations. Lemma 4.2 gives
$(q-1)q^{kr}$ independent affine choices for each.

If one direction is doubled, the $kr$ distinct directions must form a basis
of $W$, giving $B_0=b^k$ configurations. Choose the doubled direction in
$kr$ ways. For each choice there are

$$
\binom q2q^{kr-1}
=\frac12(q-1)q^{kr}
$$

affine selections, all independent by the same difference argument. Therefore

$$
N_{00}=(q-1)q^{kr}D_0.
$$

## 6. Exact distinguished-pair formula

The affine factors cancel:

$$
R_{ij}(M_{q,k,r})
=\frac{N_{11}N_{00}}{N_{10}N_{01}}
=\frac{A_0D_0}{B_0C_0}.
$$

Using

$$
x=\frac cb,
\qquad
e=\frac hb,
\qquad
y=\frac sb,
$$

we have

$$
\frac{A_0}{B_0}=kx,
\qquad
\frac{D_0}{B_0}=k\left(y+\frac r2\right),
$$

and

$$
\frac{C_0}{B_0}
=1+ke+k(k-1)xy+\frac{k(kr-1)}2x.
$$

Thus

$$
R_{ij}(M_{q,k,r})
=\frac{k^2x(y+r/2)}
{1+ke+k(k-1)xy+k(kr-1)x/2}.
$$

The closed form for $z_{r-1}$ simplifies $e$ exactly. Since

$$
z_{r-1}
=\frac{v-r}{r(q-1)}-\frac{r-1}{2},
$$

we get

$$
e=xz_{r-1}
=\frac1{q-1}-\frac{r-1}{2}x.
$$

Set

$$
w=x\left(y+\frac r2\right).
$$

Substituting $xy=w-rx/2$ and the formula for $e$ into the denominator gives

$$
1+ke+k(k-1)xy+\frac{k(kr-1)}2x
=1+\frac{k}{q-1}+k(k-1)w.
$$

Therefore

$$
R_{ij}(M_{q,k,r})
=\frac{k^2w}{1+k/(q-1)+k(k-1)w}.
$$

Finally, the closed form

$$
z_r
=\frac{qv-r}{(r+1)(q-1)}-\frac r2
$$

together with $y=(1+x)z_r-1-e$ yields, after collecting terms,

$$
w
=\frac{1}{r+1}
\left(
\frac{q(r-x)}{q-1}+rx+\frac{r-1}{2}x^2
\right).
$$

This proves the exact formula stated in Section 1.

## 7. Limits and optimization

Fix $q$. Since

$$
v=\frac{q^r-1}{q-1},
\qquad
x=\frac r{v-r},
$$

we have

$$
x\longrightarrow0,
\qquad
rx\longrightarrow0.
$$

The compact formula for $w$ then gives

$$
w\longrightarrow\frac q{q-1}.
$$

Hence, for fixed $q,k$,

$$
\begin{aligned}
\lim_{r\to\infty}R_{ij}(M_{q,k,r})
&=\frac{k^2q/(q-1)}
{1+k/(q-1)+k(k-1)q/(q-1)}\\
&=\frac{k^2q}{(k^2-k+1)q+k-1}.
\end{aligned}
$$

This limit can be rewritten as

$$
\frac{1}{1-\dfrac{(q-1)(k-1)}{qk^2}}.
$$

For integers $k\ge2$, the quantity $(k-1)/k^2$ is maximized at $k=2$.
Therefore the strongest limit in this block construction is

$$
\lim_{r\to\infty}R_{ij}(M_{q,2,r})
=\frac{4q}{3q+1}.
$$

Every $M_{q,2,r}$ is a finite $\mathbf F_q$-representable matroid, so

$$
\overline{\alpha}(\mathbf F_q)
\ge\sup_{r\ge2}R_{ij}(M_{q,2,r})
\ge\lim_{r\to\infty}R_{ij}(M_{q,2,r})
=\frac{4q}{3q+1}.
$$

No monotonicity in $r$ is needed or asserted. For example, when $q=2$, the
values at $r=2,3,4$ are respectively

$$
\frac87,
\qquad
\frac{78}{71},
\qquad
\frac{288}{265}.
$$

### The reverse limit and the unattained two-parameter supremum

Now fix $r\ge2$ and take $k=2$. As $q\to\infty$ through prime powers,

$$
v=\frac{q^r-1}{q-1}\longrightarrow\infty,
\qquad
x=\frac r{v-r}\longrightarrow0,
$$

and the compact formula gives

$$
w\longrightarrow\frac r{r+1}.
$$

Consequently,

$$
\lim_{q\to\infty}R_{ij}(M_{q,2,r})
=\frac{4r/(r+1)}{1+2r/(r+1)}
=\frac{4r}{3r+1}.
$$

Letting $r\to\infty$ now gives $4/3$, so the reverse iterated order has the
same limit as the fixed-field order proved above.

The lower bounds $4q/(3q+1)$ approach $4/3$ as $q\to\infty$ through prime
powers. We also verify that the displayed finite $k=2$ ratios are strictly
below $4/3$.

Put $a=q-1$ and $D=v-r$. Bernoulli's inequality gives

$$
D=\sum_{m=0}^{r-1}(q^m-1)
\ge a\sum_{m=0}^{r-1}m
=\frac{ar(r-1)}2,
$$

so

$$
x=\frac rD\le\frac{2}{a(r-1)}.
$$

Since $r-q/a\ge0$, the bound on $x$ implies

$$
x\left(r-\frac qa\right)+\frac{r-1}{2}x^2
\le\frac2a.
$$

The compact formula for $w$ therefore gives

$$
\begin{aligned}
(r+1)\left(\frac{q+1}{a}-w\right)
&=\frac{r+q+1}{a}
-x\left(r-\frac qa\right)
-\frac{r-1}{2}x^2\\
&\ge\frac{r+q-1}{a}>0.
\end{aligned}
$$

Thus $w<(q+1)/(q-1)$, which is equivalent to

$$
\frac{4w}{1+2/(q-1)+2w}<\frac43.
$$

Therefore the exact distinguished-pair values in the submitted two-parameter
family have supremum $4/3$, which no finite pair $(q,r)$ attains. Both
iterated orders approach this supremum. A diagonal choice of increasing prime
powers $q_n$ and sufficiently large $r_n$ supplies joint paths approaching it
as well. The website label `iterated limit` records that the submitted
supremum is limiting rather than a finite member; it does not specify a unique
order of limits.

## 8. The previous three-punctured-line result

Take $r=2$ and $k=3$. Each punctured projective line contains $q$ retained
points. With

$$
Q=\binom q2,
\qquad
T=\binom q3,
$$

the four local counts are

$$
b=Q,
\qquad
c=q,
\qquad
h=0,
\qquad
s=T.
$$

Consequently,

$$
A_0=3qQ^2,
\qquad
B_0=Q^3,
$$

$$
C_0=Q^3+6qTQ+\frac52A_0,
\qquad
D_0=3TQ^2+3B_0,
$$

which are exactly the normalized counts in the original proof. Equivalently,

$$
x=\frac{2}{q-1},
\qquad
w=\frac{2(q+1)}{3(q-1)}.
$$

Substitution into the general formula gives

$$
R_{ij}(M_{q,3,2})
=\frac{6(q+1)}{5q+6}.
$$

The construction itself also specializes exactly: three copies of a
two-dimensional space give three projective lines, deleting $[a_\ell]$ leaves
the representatives

$$
\{z_\ell\}\cup
\{a_\ell+t z_\ell:t\in\mathbf F_q^\times\},
$$

and replacing these directions by full affine fibres reproduces the original
rank-$7$ matroid on $3q^2+2$ elements.

## 9. Fixed-field comparisons for the submission

The compact website record extract
[`data/website_record_extract_2026-08-09.json`](data/website_record_extract_2026-08-09.json),
retrieved 2026-08-09 at 08:15:12 UTC, gives the following exact comparisons as
of that retrieval. Its refreshed entries are GF(4) record #13,
`[C 0 u 0; 0 C u 0; h h 0 1]`, with ratio $55752/48391$, and GF(7) record
#12, `A variant of #11`, with ratio $147888/125779$.

For GF(4),

$$
\frac{16}{13}-\frac{55752}{48391}
=\frac{49480}{629083}>0.
$$

For GF(5),

$$
\frac{5}{4}-\frac{4664}{4007}
=\frac{1379}{16028}>0.
$$

For GF(7),

$$
\frac{14}{11}-\frac{147888}{125779}
=\frac{134138}{1383569}>0.
$$

These are limiting lower-bound comparisons. Genuine finite $k=2$ members
already beat the displayed records: $(q,r)=(4,6),(5,5),(7,5)$ give
respectively

$$
\frac{188104}{162455},
\qquad
\frac{104950}{90111},
\qquad
\frac{1902350}{1602643}.
$$

In particular, the first plotted GF(7) witness is now the $r=5$ member, and

$$
\frac{1902350}{1602643}-\frac{147888}{125779}
=\frac{2264012666}{201578833897}>0.
$$

For GF(2), the fixed-field limit equals $8/7$. For GF(3),

$$
\frac65-\frac{100}{81}=-\frac{14}{405}<0.
$$

All finite plotted ratios and comparisons are regression-checked exactly by
[`scripts/verify.py`](scripts/verify.py), and small cases are independently
enumerated there. These computations validate the formulas' implementation
and the submission data; the analytic arguments above establish the universal
claims.
