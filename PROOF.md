# Proof for the three-punctured-line affine-fibre family

## 1. Statement

For every prime power $q\ge2$, there exists a rank-$7$,
$\mathbf F_q$-representable matroid $M_q$ on $3q^2+2$ elements and a
pair of elements $i,j\in E(M_q)$ such that

$$
R_{ij}(M_q)=\frac{6(q+1)}{5q+6}.
$$

Here, if $\mathcal B(M)$ is the set of bases of a matroid $M$, then

$$
R_{ij}(M)=
\frac{N_{11}N_{00}}{N_{10}N_{01}},
$$

where

$$
\begin{aligned}
N_{11}&=|\{B\in\mathcal B(M):i,j\in B\}|,\\
N_{10}&=|\{B\in\mathcal B(M):i\in B,\ j\notin B\}|,\\
N_{01}&=|\{B\in\mathcal B(M):i\notin B,\ j\in B\}|,\\
N_{00}&=|\{B\in\mathcal B(M):i,j\notin B\}|.
\end{aligned}
$$

Define the unweighted invariant

$$
\overline{\alpha}(M)=\max_{e\ne f} R_{ef}(M),
$$

where the maximum is over eligible nonloop, noncoloop pairs, and define the
unweighted field supremum

$$
\overline{\alpha}(F)=
\sup\{\overline{\alpha}(M):M\text{ is }F\text{-representable}\}.
$$

Consequently,

$$
\overline{\alpha}(M_q)\ge R_{ij}(M_q)
\quad\text{and}\quad
\overline{\alpha}(\mathbf F_q)\ge \frac{6(q+1)}{5q+6}.
$$

The usual weighted correlation constant $\alpha(M)$ also dominates
$\overline{\alpha}(M)$, so the same ratio is a lower bound for the
weighted field correlation constant.  The proved formula is a distinguished-pair
lower bound; equality with either full invariant of $M_q$ is not asserted.

## 2. Construction

Let $F=\mathbf F_q$.  Take three two-dimensional vector spaces

$$
U_r=\langle a_r,z_r\rangle_F\qquad (r=1,2,3)
$$

and put

$$
W=U_1\oplus U_2\oplus U_3,
\qquad
V=F e_0\oplus W,
\qquad
\bar j=a_1+a_2+a_3.
$$

On the projective line $\operatorname{PG}(U_r)$, delete the point
$[a_r]$.  Use the following representatives for the remaining $q$
projective directions:

$$
\mathcal L_r=
\{z_r\}\cup\{a_r+s z_r:s\in F^\times\}.
$$

For each $g\in\mathcal L_1\cup\mathcal L_2\cup\mathcal L_3$, include the
complete affine fibre

$$
F_g=\{t e_0+g:t\in F\}\subset V.
$$

Finally include

$$
i=e_0,
\qquad
j=(0,\bar j).
$$

Let $M_q$ be the vector matroid of these columns.  There are $3q$ retained
quotient directions, each with $q$ affine lifts, together with $i,j$.
Therefore

$$
|E(M_q)|=3q^2+2.
$$

Any two distinct directions of $\mathcal L_r$ span $U_r$, so the retained
directions span $W$.  Together with $i=e_0$, they span $V$.  Hence

$$
\operatorname{rk}(M_q)=7.
$$

## 3. Two elementary lemmas

### Lemma 3.1: quotient rank by block occupancy

Let $S$ be a set of distinct retained quotient directions in $W$, and let
$m_r$ be the number of members of $S$ lying in $U_r$.  Then

$$
\operatorname{rk}_W(S)=\sum_{r=1}^3\min(m_r,2).
$$

Moreover,

$$
\operatorname{rk}_W(S\cup\{\bar j\})
=
\operatorname{rk}_W(S)+
\begin{cases}
0,&m_1,m_2,m_3\ge2,\\
1,&\text{otherwise}.
\end{cases}
$$

#### Proof

Distinct projective directions in the two-dimensional space $U_r$ have span
of dimension $\min(m_r,2)$.  Since $W=U_1\oplus U_2\oplus U_3$, the first
formula follows by addition of dimensions.

The vector $a_r$ lies in the span of the selected directions in $U_r$ if
and only if $m_r\ge2$: it is excluded as a retained direction, so it does not
lie in the span of a single retained direction.  By the direct-sum
decomposition, $\bar j=a_1+a_2+a_3$ lies in $\langle S\rangle$ if and only
if this holds in every block.  This proves the second formula. $\square$

### Lemma 3.2: affine lifting of a unique relation

Suppose quotient vectors $w_1,\dots,w_m\in W$ have rank $m-1$, with unique
relation up to scale

$$
\sum_{k=1}^m c_k w_k=0.
$$

Then the lifts $t_k e_0+w_k\in V$ are independent if and only if

$$
\sum_{k=1}^m c_k t_k\ne0.
$$

Consequently, if all $t_k$ range independently over $F$, exactly
$(q-1)q^{m-1}$ choices give independent lifts.

#### Proof

Any linear relation among the lifts projects to a scalar multiple of the unique
quotient relation.  The corresponding $e_0$-coordinate is
$\sum c_k t_k$.  Thus the quotient relation survives upstairs exactly when
this scalar is zero.  Since the displayed linear functional is nonzero, its
kernel has $q^{m-1}$ elements among the $q^m$ choices. $\square$

Two further observations will be used repeatedly:

1. A set containing $i=e_0$ contains at most one element from each affine
   fibre, because two points in the same fibre differ by a multiple of $i$.
2. A linearly independent set not containing $i$ contains at most two points
   from any fibre, because a fibre lies in the two-dimensional space
   $\langle e_0,g\rangle$.

## 4. Basis-cell counts

Write

$$
Q=\binom q2,
\qquad
T=\binom q3.
$$

We count bases according to whether they contain $i$ and $j$.

### 4.1. Bases containing both $i$ and $j$

After choosing $i,j$, five fibre elements remain.  By Observation 1 their
quotient directions are distinct.  Since $i$ supplies the $e_0$-direction,
the five quotient directions together with $\bar j$ must form a basis of
$W$.

By Lemma 3.1, the occupancy vector across $(U_1,U_2,U_3)$ must be a
permutation of $(1,2,2)$.  Choose the singleton block in three ways, its
single direction in $q$ ways, and an unordered pair of distinct directions in
each other block.  Define

$$
A_0=3qQ^2.
$$

Every selected direction has $q$ arbitrary affine lifts, so

$$
N_{11}=q^5A_0.
$$

### 4.2. Bases containing $i$ but not $j$

The six fibre elements must project to a basis of $W$.  Lemma 3.1 forces two
distinct directions in each block.  Define

$$
B_0=Q^3.
$$

Again every affine coordinate is arbitrary, so

$$
N_{10}=q^6B_0.
$$

### 4.3. Bases containing $j$ but not $i$

Choose six fibre elements together with $j$.  By Observation 2, a fibre is
used at most twice.  If two fibres were doubled, there would be at most four
distinct fibre directions; together with $\bar j$, the quotient rank would
be at most five, and the seven lifted vectors could not be independent.
Therefore there are exactly two cases.

#### Case A: six distinct quotient directions

By Lemma 3.1, the six directions together with $\bar j$ span $W$ exactly
for occupancies

$$
(2,2,2)
\quad\text{or a permutation of}\quad
(1,2,3).
$$

The number of quotient configurations is therefore

$$
B_0+6qTQ.
$$

The seven projected vectors have rank six and hence one relation.  Lemma 3.2,
with the affine coordinate of $j$ fixed at zero, gives
$(q-1)q^5$ independent affine choices.

#### Case B: one doubled quotient direction

The five distinct fibre directions together with $\bar j$ must form a basis
of $W$, giving $A_0$ configurations.  There are five choices for the
direction to double.  For a fixed choice, select two distinct points from that
fibre and one point from each of the other four fibres:

$$
\binom q2q^4=\frac12(q-1)q^5.
$$

The relation between the two equal quotient directions lifts to a nonzero
multiple of $e_0$, because their affine coordinates are distinct.  Thus all
these choices are independent.

Combining the cases, define the normalized quantity

$$
C_0=B_0+6qTQ+\frac52A_0.
$$

Then

$$
N_{01}=(q-1)q^5C_0.
$$

The normalization permits $C_0$ itself to be a half-integer for odd $q$;
the actual count $N_{01}$ is always an integer.

### 4.4. Bases containing neither $i$ nor $j$

Choose seven fibre elements.  If at least two fibres were doubled, there would
be at most five distinct quotient directions, so the quotient rank would be at
most five.  Since the projection $V\to W$ has one-dimensional kernel, the
rank upstairs would then be at most six.  Hence only two cases are possible.

#### Case A: seven distinct quotient directions

To have quotient rank six, Lemma 3.1 forces an occupancy vector that is a
permutation of $(3,2,2)$.  The number of quotient configurations is

$$
3TQ^2.
$$

The quotient vectors have a unique relation, and Lemma 3.2 gives
$(q-1)q^6$ independent affine choices.

#### Case B: one doubled quotient direction

The six distinct quotient directions must form a basis of $W$, giving
$B_0$ configurations.  There are six choices for the doubled direction, and
for each choice

$$
\binom q2q^5=\frac12(q-1)q^6
$$

independent affine selections.

Define

$$
D_0=3TQ^2+3B_0.
$$

Then

$$
N_{00}=(q-1)q^6D_0.
$$

## 5. Closed formula

Direct simplification gives

$$
A_0=\frac{3q^3(q-1)^2}{4},
\qquad
B_0=\frac{q^3(q-1)^3}{8},
$$

$$
C_0=\frac{q^3(q-1)^2(5q+6)}{8},
\qquad
D_0=\frac{q^3(q-1)^3(q+1)}{8}.
$$

Equivalently, the four actual basis-cell counts are

$$
N_{11}=\frac{3q^8(q-1)^2}{4},
\qquad
N_{10}=\frac{q^9(q-1)^3}{8},
$$

$$
N_{01}=\frac{q^8(q-1)^3(5q+6)}{8},
\qquad
N_{00}=\frac{q^9(q-1)^4(q+1)}{8}.
$$

Therefore

$$
R_{ij}(M_q)
=\frac{N_{11}N_{00}}{N_{10}N_{01}}
=\frac{A_0D_0}{B_0C_0}
=\frac{6(q+1)}{5q+6}.
$$

Finally,

$$
\frac{6(q+1)}{5q+6}
=\frac65-\frac{6}{25q+30}.
$$

Thus the values increase strictly with $q$, are always below $6/5$, and
approach $6/5$ without attaining it.

## 6. The two website-record improvements

For $q=4$,

$$
|E(M_4)|=50,
\qquad
R_{ij}(M_4)=\frac{30}{26}=\frac{15}{13},
$$

and

$$
\frac{15}{13}-\frac87=\frac1{91}>0.
$$

For $q=7$,

$$
|E(M_7)|=149,
\qquad
R_{ij}(M_7)=\frac{48}{41},
$$

and, relative to the website record present on 2026-08-08,

$$
\frac{48}{41}-\frac{280043}{243256}
=\frac{194525}{9973496}>0.
$$

Hence the construction yields the strict lower-bound improvements

$$
\boxed{\overline{\alpha}(\mathbf F_4)\ge\frac{15}{13}}
\qquad\text{and}\qquad
\boxed{\overline{\alpha}(\mathbf F_7)\ge\frac{48}{41}}.
$$

The exact counts used for these two members are recorded in
[`data/improved_members.json`](data/improved_members.json), and all displayed
identities are checked by [`scripts/verify.py`](scripts/verify.py).
