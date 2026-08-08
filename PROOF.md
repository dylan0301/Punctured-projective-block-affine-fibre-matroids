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
weighted field correlation constant. The proved formula is a distinguished-pair
lower bound; equality with either full invariant of $M_q$ is not asserted.

## 2. Construction

Let $F=\mathbf F_q$. Take three two-dimensional vector spaces

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

On the projective line $\mathrm{PG}(U_r)$, delete the point $[a_r]$. Use the
following representatives for the remaining $q$ projective directions:

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
j=(0,\bar j),
$$

where the coordinates of $j$ refer to the decomposition $V=F e_0\oplus W$.
Let $M_q$ be the vector matroid of these columns.

The quotient map used throughout the proof is

$$
\pi:V\longrightarrow W,
\qquad
\pi(t e_0+w)=w.
$$

Its kernel is $F e_0$, and $\pi$ maps every element of $F_g$ to the same
quotient direction $g$. Thus the construction has $3q$ retained quotient
directions, each with $q$ affine lifts, together with $i,j$. Therefore

$$
|E(M_q)|=3q^2+2.
$$

Since $q\ge2$, each $\mathcal L_r$ contains at least two distinct projective
directions. Any two such directions span $U_r$, so the retained directions
span $W$. Together with $i=e_0$, they span $V$. Hence

$$
\mathrm{rk}(M_q)=7.
$$

## 3. Two elementary lemmas

### Lemma 3.1: quotient rank by block occupancy

Let $S$ be a set of distinct retained quotient directions in $W$, and let
$m_r$ be the number of members of $S$ lying in $U_r$. Then

$$
\mathrm{rk}_W(S)=\sum_{r=1}^3\min(m_r,2).
$$

Moreover,

$$
\mathrm{rk}_W(S\cup\{\bar j\}) =
\mathrm{rk}_W(S)+
\begin{cases}
0,&m_1,m_2,m_3\ge2,\\
1,&\text{otherwise}.
\end{cases}
$$

#### Proof

Write $S_r=S\cap U_r$. If $m_r=0$, then $\langle S_r\rangle$ has dimension
zero; if $m_r=1$, it has dimension one; and if $m_r\ge2$, two distinct
projective directions in $S_r$ already span the two-dimensional space $U_r$.
Thus

$$
\dim\langle S_r\rangle=\min(m_r,2).
$$

The direct-sum decomposition of $W$ gives

$$
\langle S\rangle =
\langle S_1\rangle\oplus
\langle S_2\rangle\oplus
\langle S_3\rangle,
$$

which proves the first formula.

Next, $a_r\in\langle S_r\rangle$ if and only if $m_r\ge2$. The forward
implication for $m_r=1$ fails precisely because the direction $[a_r]$ was
deleted: a single retained direction is not proportional to $a_r$. The
reverse implication follows because two distinct retained directions span
$U_r$. Since the three summands $U_r$ are independent,

$$
\bar j=a_1+a_2+a_3\in\langle S\rangle
$$

if and only if $a_r\in\langle S_r\rangle$ for every $r$. Thus $\bar j$ is
already in the span exactly when $m_1,m_2,m_3\ge2$; otherwise it increases the
rank by one. $\square$

### Lemma 3.2: affine lifting of a unique relation

Suppose quotient vectors $w_1,\dots,w_m\in W$ have rank $m-1$, with unique
relation up to scale

$$
\sum_{k=1}^m c_k w_k=0.
$$

Then the lifts $v_k=t_k e_0+w_k\in V$ are independent if and only if

$$
\sum_{k=1}^m c_k t_k\ne0.
$$

Consequently, if all $t_k$ range independently over $F$, exactly
$(q-1)q^{m-1}$ choices give independent lifts.

#### Proof

Suppose

$$
\sum_{k=1}^m d_k v_k=0.
$$

Applying $\pi$ gives $\sum d_k w_k=0$. Since the relation space among the
$w_k$ is one-dimensional, there is a scalar $\lambda\in F$ such that
$d_k=\lambda c_k$ for every $k$. The original relation upstairs therefore
reduces to

$$
\lambda\left(\sum_{k=1}^m c_k t_k\right)e_0=0.
$$

If $\sum c_k t_k\ne0$, this forces $\lambda=0$, so the lifts are independent.
If $\sum c_k t_k=0$, the nonzero coefficient vector $(c_1,\dots,c_m)$ gives a
nontrivial relation among the lifts. This proves the equivalence.

The map

$$
F^m\longrightarrow F,
\qquad
(t_1,\dots,t_m)\longmapsto\sum_{k=1}^m c_k t_k
$$

is a nonzero linear functional, so its kernel has $q^{m-1}$ elements. Hence
$q^m-q^{m-1}=(q-1)q^{m-1}$ choices give independent lifts. $\square$

Three observations will be used repeatedly:

1. A set containing $i=e_0$ contains at most one element from each affine
   fibre. Indeed, if $t e_0+g$ and $t'e_0+g$ are both present, then their
   difference is $(t-t')i$.
2. A linearly independent set not containing $i$ contains at most two points
   from any fibre, because $F_g\subset\langle e_0,g\rangle$, a
   two-dimensional subspace.
3. For every set $X\subset V$,

   $$
   \mathrm{rk}_V(X)\le \mathrm{rk}_W(\pi(X))+1,
   $$

   because $\ker\pi=F e_0$ is one-dimensional.

## 4. Basis-cell counts

Write

$$
Q=\binom q2,
\qquad
T=\binom q3.
$$

We count bases according to whether they contain $i$ and $j$. An occupancy
vector $(m_1,m_2,m_3)$ always records the numbers of distinct quotient
directions in the three blocks; repeated selections from one affine fibre are
handled separately.

### 4.1. Bases containing both $i$ and $j$

After choosing $i,j$, five fibre elements remain. By Observation 1 their
quotient directions are distinct. A set

$$
\{i,j,t_1e_0+g_1,\dots,t_5e_0+g_5\}
$$

is independent if and only if $\{\bar j,g_1,\dots,g_5\}$ is a basis of $W$.
Indeed, a quotient dependence can be lifted to a dependence in $V$ by using
$i$ to cancel its $e_0$-coordinate, while a quotient basis forces all
coefficients except that of $i$ to vanish and then forces the coefficient of
$i$ to vanish as well.

The five occupancies sum to $5$. They cannot all be at least $2$, so Lemma
3.1 says that $\bar j$ must contribute the sixth quotient rank. Consequently
the five directions must have rank $5$, which occurs exactly for a permutation
of $(1,2,2)$. Choose the singleton block in three ways, its single direction
in $q$ ways, and an unordered pair of distinct directions in each other block.
Define

$$
A_0=3qQ^2.
$$

Once the quotient basis is fixed, every selected direction has $q$ arbitrary
affine lifts, since the presence of $i$ absorbs all changes in the
$e_0$-coordinates. Therefore

$$
N_{11}=q^5A_0.
$$

### 4.2. Bases containing $i$ but not $j$

The same quotient argument shows that the six fibre elements must project to a
basis of $W$. Thus

$$
\sum_{r=1}^3\min(m_r,2)=6.
$$

Every summand must equal $2$, and the six occupancies sum to $6$, so the only
possibility is $(2,2,2)$. Define

$$
B_0=Q^3.
$$

Again every affine coordinate is arbitrary, so

$$
N_{10}=q^6B_0.
$$

### 4.3. Bases containing $j$ but not $i$

Choose six fibre elements together with $j$. By Observation 2, a fibre is
used at most twice. If two fibres were doubled, there would be at most four
distinct fibre directions. Together with $\bar j$, their quotient rank would
be at most five, and Observation 3 would bound the rank of the seven lifted
vectors by six. Therefore only the multiplicity types $1^6$ and $2,1^4$ can
contribute.

#### Case A: six distinct quotient directions

Let $(m_1,m_2,m_3)$ be the occupancy vector, so $m_1+m_2+m_3=6$. If every
$m_r\ge2$, then the occupancy is $(2,2,2)$, the six directions already span
$W$, and $\bar j$ adds no rank. If some $m_r<2$, then $\bar j$ adds one rank
by Lemma 3.1, so the six directions themselves must have rank five. The rank
formula shows that this happens exactly for a permutation of $(1,2,3)$.
Hence the admissible occupancies are

$$
(2,2,2)
\quad\text{or a permutation of}\quad
(1,2,3).
$$

The first type contributes $B_0$. For the second type, assign the three
distinct occupancies to the blocks in $6$ ways and then choose the directions,
giving $6qTQ$. Thus the number of quotient configurations is

$$
B_0+6qTQ.
$$

The seven projected vectors, namely the six selected directions and $\bar j$,
have rank six and hence a one-dimensional relation space. Apply Lemma 3.2
with the affine coordinate of $j$ fixed at zero. The resulting linear
functional in the six fibre coordinates is nonzero: otherwise the unique
relation would be supported only on the nonzero vector $\bar j$. Therefore
exactly $q^5$ of the $q^6$ affine choices are dependent, and

$$
(q-1)q^5
$$

choices are independent.

#### Case B: one doubled quotient direction

There are five distinct fibre directions. Observation 3 forces these five
directions together with $\bar j$ to have rank six, so they form a basis of
$W$. By the calculation in Section 4.1, there are $A_0$ such quotient
configurations. There are five choices for the direction to double. For a
fixed choice, select two distinct points from that fibre and one point from
each of the other four fibres:

$$
\binom q2q^4=\frac12(q-1)q^5.
$$

All these selections are independent. To see this, write the two selected
lifts over the doubled direction as $t e_0+g$ and $t'e_0+g$, with $t\ne t'$.
Replacing the second by its difference with the first is an invertible column
operation and produces the nonzero vector $(t'-t)e_0$. The remaining six
vectors project bijectively to a basis of $W$, so they are independent and
their span meets $F e_0$ trivially. Adjoining the nonzero difference therefore
gives a basis of $V$.

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

Choose seven fibre elements. If at least two fibres were doubled, there would
be at most five distinct quotient directions. Their quotient rank would then
be at most five, and Observation 3 would bound the rank upstairs by six. Hence
only the multiplicity types $1^7$ and $2,1^5$ can contribute.

#### Case A: seven distinct quotient directions

The seven lifts can have rank seven only if their quotient rank is six. By
Lemma 3.1, this means

$$
\sum_{r=1}^3\min(m_r,2)=6.
$$

Thus every block contains at least two directions. Since the occupancies sum
to seven, the occupancy vector is a permutation of $(3,2,2)$. The number of
quotient configurations is

$$
3TQ^2.
$$

The seven quotient vectors have rank six and therefore a unique relation.
Lemma 3.2 gives $(q-1)q^6$ independent affine choices.

#### Case B: one doubled quotient direction

There are six distinct quotient directions. Observation 3 forces them to have
rank six, so they form a basis of $W$. Their occupancy vector is therefore
$(2,2,2)$, giving $B_0$ quotient configurations. There are six choices for
the doubled direction, and for each choice there are

$$
\binom q2q^5=\frac12(q-1)q^6
$$

affine selections. Every such selection is independent by the same difference
argument as in Section 4.3: one lift from each quotient direction projects to
a basis of $W$, while the difference of the two lifts over the doubled
direction supplies a nonzero vector in $F e_0$.

Consequently, this case contributes

$$
6B_0\binom q2q^5=3(q-1)q^6B_0.
$$

Define

$$
D_0=3TQ^2+3B_0.
$$

Then

$$
N_{00}=(q-1)q^6D_0.
$$

## 5. Closed formula

Using

$$
Q=\frac{q(q-1)}2,
\qquad
T=\frac{q(q-1)(q-2)}6,
$$

we first obtain

$$
A_0=3qQ^2=\frac{3q^3(q-1)^2}{4},
\qquad
B_0=Q^3=\frac{q^3(q-1)^3}{8}.
$$

For the two less immediate simplifications,

$$
\begin{aligned}
C_0
&=B_0+6qTQ+\frac52A_0\\
&=\frac{q^3(q-1)^2}{8}
  \bigl((q-1)+4(q-2)+15\bigr)\\
&=\frac{q^3(q-1)^2(5q+6)}{8},
\end{aligned}
$$

and

$$
\begin{aligned}
D_0
&=3TQ^2+3B_0\\
&=\frac{q^3(q-1)^3}{8}\bigl((q-2)+3\bigr)\\
&=\frac{q^3(q-1)^3(q+1)}{8}.
\end{aligned}
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

The lift factors cancel in the correlation ratio:

$$
\begin{aligned}
R_{ij}(M_q)
&=\frac{N_{11}N_{00}}{N_{10}N_{01}}\\
&=\frac{(q^5A_0)((q-1)q^6D_0)}
        {(q^6B_0)((q-1)q^5C_0)}\\
&=\frac{A_0D_0}{B_0C_0}\\
&=\frac{6(q+1)}{5q+6}.
\end{aligned}
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
