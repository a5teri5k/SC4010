# SC4010 — ECDLP Weak Parameters

Explorations and implementations of attacks against the Elliptic Curve Discrete Logarithm Problem (ECDLP) on curves with weak parameters, built with **SageMath**.

- **SC4010 Project:** [Smart's Attack](#project-smarts-attack-anomalous-curves) targeting **anomalous elliptic curves** ($\#E(\mathbb{F}_p) = p$, trace of Frobenius $t = 1$).
- **Personal Interest:** [Pohlig-Hellman Attack](#personal-interest-pohlig-hellman-attack-smooth-order-curves) targeting **smooth-order elliptic curves** whose group order factors into small primes.

---

## Repository Structure

### Project — Smart's Attack (Anomalous Curves)

| File | Description |
| :--- | :--- |
| [`smart_attack.py`](smart_attack.py) | Core SageMath implementation of Smart's attack (`smart_attack` and `lift_points`). |
| [`Sample with small curve.ipynb`](Sample%20with%20small%20curve.ipynb) | Walkthrough and verification using the $p = 43$ curve example from Nigel Smart's 1999 paper. |
| [`204-bit Anomalous.ipynb`](204-bit%20Anomalous.ipynb) | Attack benchmark on a 204-bit anomalous curve from SafeCurves. |
| [`384-bit Generated Anomalous.ipynb`](384-bit%20Generated%20Anomalous.ipynb) | Attack script for a 384-bit anomalous curve generated using `ecgen`. |
| [`anomalous.json`](anomalous.json) | Raw `ecgen` JSON parameters (`p`, `a`, `b`, `order`, and base point) for the 384-bit anomalous curve. |

### Personal Interest — Pohlig–Hellman Attack

| File | Description |
| :--- | :--- |
| [`Pohlig-Hellman.ipynb`](Pohlig-Hellman.ipynb) | Standalone implementation of the Pohlig–Hellman attack on a 128-bit smooth-order elliptic curve, verified against SageMath's `Q.log(P)`. |

---

## Project: Smart's Attack (Anomalous Curves)

An elliptic curve $E / \mathbb{F}_p$ is **anomalous** when its order equals the field characteristic ($\#E(\mathbb{F}_p) = p$). Smart's attack solves $Q = mP$ in polynomial time by lifting the curve and points to the $p$-adic numbers $\mathbb{Q}_p$.

### Implementation ([`smart_attack.py`](smart_attack.py))

1. **Anomalous check:** Verifies `E.order() == p` and raises a `ValueError` otherwise.
2. **Curve & point lifting:** Defines `Eq` over `pAdicField(p, 8)` using the curve's Weierstrass invariants and lifts $P$ and $Q$ via `lift_points(Eq, x, y)` (matching `y` modulo $p$).
3. **Scalar multiplication & $p$-adic logarithm:** Computes $p\tilde{P}$ and $p\tilde{Q}$ on `Eq` and evaluates $\psi = -x/y$ in the formal group.
4. **Canonical lift guard & recovery:** Checks `logpq.valuation() == 1` to ensure the lift is not canonical, then recovers $m \equiv \psi(p\tilde{Q}) / \psi(p\tilde{P}) \pmod{p}$.

### Notebooks & Results

Each Smart's attack notebook compares `smart_attack(E, P, Q)` against SageMath's built-in `P.padic_elliptic_logarithm(Q, p)` and verifies the recovered scalar:

- **[`Sample with small curve.ipynb`](Sample%20with%20small%20curve.ipynb)**
  - Curve: $y^2 = x^3 - 4x^2 - 128x - 432$ over $\mathbb{F}_{43}$, with $P = (0, 16)$ and $Q = (12, 1)$.
  - Recovers the secret `m = 10` (recorded notebook runtime: `0:00:00.008937` for `smart_attack` vs. `0:00:00.006768` for SageMath's built-in).
- **[`204-bit Anomalous.ipynb`](204-bit%20Anomalous.ipynb)**
  - 204-bit anomalous curve from SafeCurves with a random secret $n \in [1, p - 1]$ and $Q = nP$.
  - Recovers `m == n` (recorded notebook runtime: `0:00:00.125589` for `smart_attack` vs. `0:00:00.097292` for SageMath's built-in).
- **[`384-bit Generated Anomalous.ipynb`](384-bit%20Generated%20Anomalous.ipynb)** & **[`anomalous.json`](anomalous.json)**
  - 384-bit anomalous curve (`cofactor = 1`) generated with `ecgen`.
  - Sets up the curve and base point $P$, samples a random secret $n \in [1, p - 1]$, and compares `smart_attack(E, P, Q)` against `P.padic_elliptic_logarithm(Q, p)` (`m == n`, `x == n`, `m == x`; cells saved without outputs).

---

## Personal Interest: Pohlig-Hellman Attack (Smooth-Order Curves)

Done separately out of personal interest, [`Pohlig-Hellman.ipynb`](Pohlig-Hellman.ipynb) demonstrates the vulnerability of an elliptic curve over a 128-bit prime field (`p = 0xa5dad2cb65b65ab89ed2248be2971c0d`) whose base point order `order(P)` factors into small primes.

1. Factors `order(P)` using `factor(order(P))`.
2. Projects $P$ and $Q = nP$ into each prime-order subgroup via `m = order(P) // i[0]` and solves each small subgroup DLP by iterating `j` until `j * mP == mQ`.
3. Recombines all subgroup residues using the Chinese Remainder Theorem (`CRT_list(residues, moduli)`).
4. Verifies that the recovered key `k` matches both the secret `n` and SageMath's built-in `Q.log(P)`.

---

## Prerequisites & Usage

### Requirements

- **SageMath** (notebooks were configured with the `SageMath 10.9` Jupyter kernel)
- Jupyter Notebook / JupyterLab / VS Code with Jupyter support (for `.ipynb` files)

### Running the Notebooks

1. Install SageMath and ensure the `sagemath` Jupyter kernel is available.
2. Launch Jupyter from the repository root (so `from smart_attack import smart_attack` resolves cleanly):

   ```bash
   sage -n jupyter
   ```

3. Open any of the `.ipynb` notebooks and run the cells sequentially.

### Using `smart_attack` in SageMath

```python
from sage.all import *
from smart_attack import smart_attack

# Given an anomalous elliptic curve E over GF(p) with E.order() == p
# and points P, Q on E where Q = n * P:
m = smart_attack(E, P, Q)
assert m * P == Q
```

---

## References

- Nigel P. Smart, *"The Discrete Logarithm Problem on Elliptic Curves of Trace One"*, Journal of Cryptology, 1999 — [SpringerLink](https://link.springer.com/article/10.1007/s001459900052)
- SafeCurves — [safecurves.cr.yp.to](https://safecurves.cr.yp.to/)
- `ecgen` (Elliptic Curve Generator) — [neuromancer.sk/page/ecgen](https://neuromancer.sk/page/ecgen) · [GitHub](https://github.com/J08nY/ecgen)
