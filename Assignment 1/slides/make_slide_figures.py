"""
make_slide_figures.py — presentation figures for the Components 1 & 2 meeting deck.

Each block below is the SAME code as the corresponding notebook cell
(component1_classical.ipynb / component2_quantum.ipynb) — same definitions, same
plotting calls, same axis scaling, titles, colors, and legend positions. The only
additions are the short annotation labels for the slides (the `ann(...)` lines) and
the output path (assets/). Styling uses the group's `apply_group_style`, exactly as
the notebooks do via `setup()`.
"""
import sys, os
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from qutip import destroy, basis, coherent, sesolve, wigner

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "shared"))
from group_plot_style import apply_group_style
apply_group_style()

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(OUT, exist_ok=True)
m = omega = hbar = 1.0

def ann(ax, text, xy, xytext_frac, ha="left", va="top", fs=11.5):
    """Slide-only label: arrow to a data feature (xy), text at an axes-fraction spot."""
    ax.annotate(text, xy=xy, xycoords="data", xytext=xytext_frac, textcoords="axes fraction",
                ha=ha, va=va, fontsize=fs, fontweight="bold", color="#0B1F3A",
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#2EC4B6", lw=1.6),
                arrowprops=dict(arrowstyle="-|>", color="#B23A48", lw=2.0))
def savefig(name):
    plt.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight"); plt.close()

# ===== Component 1, Task 1 — energy() and contours (notebook cells 4 & 7) =====
def energy(x, p, m=m, omega=omega):
    kinetic = p**2 / (2.0 * m)
    potential = 0.5 * m * omega**2 * x**2
    return kinetic + potential

x_vals = np.linspace(-3, 3, 400)
p_vals = np.linspace(-3, 3, 400)
X, P = np.meshgrid(x_vals, p_vals)
E_grid = energy(X, P)
fig, ax = plt.subplots(figsize=(6.2, 5.4))
filled = ax.contourf(X, P, E_grid, levels=30, cmap="viridis")
lines = ax.contour(X, P, E_grid, levels=[0.5, 1.5, 3.0, 4.5], colors="white", linewidths=1.2)
ax.clabel(lines, inline=True, fontsize=9, fmt="E=%.1f")
cbar = fig.colorbar(filled, ax=ax, shrink=0.82, pad=0.02)
cbar.set_label("Energy E  (dimensionless)")
ax.set_xlabel("Position x  (dimensionless)")
ax.set_ylabel("Momentum p  (dimensionless)")
ax.set_title("Constant-energy contours are circles in natural units", fontsize=13, pad=12)
ax.set_aspect("equal")
ann(ax, "fixed-energy orbit", xy=(-1.05, 1.05), xytext_frac=(0.03, 0.97))
ann(ax, "lowest energy", xy=(0, 0), xytext_frac=(0.03, 0.12))
plt.tight_layout(); savefig("c1_contours.png")

# ===== Component 1, Task 2 — hamilton_rhs() and single trajectory (notebook cell 10) =====
def hamilton_rhs(t, state, m=m, omega=omega):
    x, p = state
    dxdt = p / m
    dpdt = -m * omega**2 * x
    return [dxdt, dpdt]

T = 2 * np.pi / omega
t_span = (0.0, 2 * T)
t_eval = np.linspace(*t_span, 600)
x0, p0 = 2.0, 0.0
sol = solve_ivp(hamilton_rhs, t_span, [x0, p0], t_eval=t_eval, method="RK45", rtol=1e-9, atol=1e-9)
x_exact = x0*np.cos(omega*sol.t) + (p0/(m*omega))*np.sin(omega*sol.t)
p_exact = -m*omega*x0*np.sin(omega*sol.t) + p0*np.cos(omega*sol.t)
fig, ax = plt.subplots(figsize=(5.6, 5.4))
ax.plot(sol.y[0], sol.y[1], color="#1f77b4", lw=2.5, label="numerical (solve_ivp)")
ax.plot(x_exact, p_exact, "--", color="white", lw=1.2, label="analytic check")
ax.plot(x0, p0, "o", color="crimson", ms=9, label="start $(x_0,p_0)$")
ax.set_xlabel("Position x  (dimensionless)")
ax.set_ylabel("Momentum p  (dimensionless)")
ax.set_title("A classical orbit is a closed loop in phase space")
ax.set_aspect("equal"); ax.grid(alpha=0.3); ax.legend(loc="lower left")
ann(ax, "numerical = exact\n(curves overlap)", xy=(-1.4, 1.43), xytext_frac=(0.02, 0.98))
ann(ax, "closed orbit:\nenergy conserved", xy=(1.42, 1.42), xytext_frac=(0.60, 0.98))
plt.tight_layout(); savefig("c1_single.png")

# ===== Component 1, Task 2 — many trajectories (notebook cell 13) =====
rng = np.random.default_rng(42)
n_traj = 12
fig, ax = plt.subplots(figsize=(7.4, 5.8))
cmap = plt.cm.plasma
for k in range(n_traj):
    x0 = rng.uniform(-2.5, 2.5)
    p0 = rng.uniform(-2.5, 2.5)
    sol = solve_ivp(hamilton_rhs, (0, T), [x0, p0], t_eval=np.linspace(0, T, 400),
                    method="RK45", rtol=1e-9, atol=1e-9)
    E0 = energy(x0, p0)
    color = cmap(E0 / 6.0)
    ax.plot(sol.y[0], sol.y[1], color=color, lw=1.6)
    ax.plot(x0, p0, "o", color=color, ms=5)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, 6))
cbar = fig.colorbar(sm, ax=ax, shrink=0.82, pad=0.02); cbar.set_label("Initial energy E  (dimensionless)")
ax.set_xlabel("Position x  (dimensionless)")
ax.set_ylabel("Momentum p  (dimensionless)")
ax.set_title("Larger starting energy gives a larger, non-crossing orbit", fontsize=13, pad=12)
ax.set_aspect("equal"); ax.grid(alpha=0.3)
ann(ax, "larger E →\nlarger orbit", xy=(2.0, 2.0), xytext_frac=(0.32, 0.97))
ann(ax, "orbits never cross", xy=(-0.9, 0.5), xytext_frac=(0.02, 0.09))
plt.tight_layout(); savefig("c1_many.png")

# ===== Component 2, Task 1 — operators (notebook cell 5) and matrices (cell 6) =====
N = 30
a = destroy(N)
adag = a.dag()
x_op = (a + adag) / np.sqrt(2)
p_op = -1j * (a - adag) / np.sqrt(2)
H = p_op**2 / (2*m) + 0.5 * m * omega**2 * x_op**2
fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.2))
for ax, op, name in zip(axes, [x_op, p_op, H], [r"$|\hat x|$", r"$|\hat p|$", r"$|\hat H|$"]):
    im = ax.imshow(np.abs(op.full()), cmap="viridis")
    ax.set_title(name)
    ax.set_xlabel("column index n")
    ax.set_ylabel("row index m")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
fig.suptitle("Operator matrices in the energy (Fock) basis", y=1.02)
ann(axes[0], "off-diagonal:\ncouples neighbors", xy=(2, 1), xytext_frac=(0.34, 0.74))
ann(axes[2], "diagonal:\ndefinite energy", xy=(8, 8), xytext_frac=(0.42, 0.86))
plt.tight_layout(); savefig("c2_operators.png")

# ===== Component 2, Task 1 — energy spectrum (notebook cell 9) =====
eigvals = H.eigenenergies()
n_index = np.arange(N)
analytic = hbar * omega * (n_index + 0.5)
fig, ax = plt.subplots(figsize=(6.6, 4.6))
ax.plot(n_index, analytic, "-", color="crimson", lw=2, label=r"analytic  $E_n=\hbar\omega(n+\frac{1}{2})$")
ax.plot(n_index, eigvals, "o", color="#1f77b4", ms=6, mfc="none", label="QuTiP eigenvalues")
ax.set_xlabel("Level index n  (dimensionless)")
ax.set_ylabel("Energy $E_n$  (dimensionless)")
ax.set_title("Quantized, evenly spaced energy levels")
ax.legend(loc="upper left"); ax.grid(alpha=0.3)
ann(ax, "$E_0=\\frac{1}{2}\\hbar\\omega\\neq0$", xy=(0, 0.5), xytext_frac=(0.10, 0.30))
ann(ax, "spacing $\\Delta E=\\hbar\\omega$", xy=(10, 10.5), xytext_frac=(0.40, 0.30))
ann(ax, "high-n drift =\ntruncation", xy=(27, 24), xytext_frac=(0.66, 0.90))
plt.tight_layout(); savefig("c2_spectrum.png")

# ===== Component 2, Task 1 — convergence in N (notebook cell 12) =====
fig, ax = plt.subplots(figsize=(6.8, 4.6))
for N_test in [10, 30, 50]:
    a_t = destroy(N_test)
    x_t = (a_t + a_t.dag()) / np.sqrt(2)
    p_t = -1j * (a_t - a_t.dag()) / np.sqrt(2)
    H_t = p_t**2 / 2 + x_t**2 / 2
    err_t = np.abs(H_t.eigenenergies() - (np.arange(N_test) + 0.5))
    ax.semilogy(np.arange(N_test), err_t + 1e-18, marker="o", ms=3, label=f"N = {N_test}")
ax.axhline(1e-6, ls="--", color="k", alpha=0.6, label="1e-6 threshold")
ax.set_xlabel("Level index n  (dimensionless)")
ax.set_ylabel("Eigenvalue error  (dimensionless)")
ax.set_title("Higher truncation N extends the trustworthy energy range")
ax.legend(loc="lower right")
ann(ax, "bigger N →\nmore exact levels", xy=(24, 1e-15), xytext_frac=(0.30, 0.55))
plt.tight_layout(); savefig("c2_convergence.png")

# ===== Component 2, Task 2 — three states + sesolve (notebook cell 16) =====
psi_fock  = basis(N, 1)
psi_super = (basis(N, 0) + basis(N, 1)).unit()
alpha = 1.5
psi_coh   = coherent(N, alpha)
states = {"Fock |1>": psi_fock, "Superposition (|0>+|1>)/sqrt2": psi_super,
          f"Coherent |a={alpha}>": psi_coh}
tlist = np.linspace(0, T, 200)
results = {}
for name, psi0 in states.items():
    results[name] = sesolve(H, psi0, tlist, e_ops=[x_op, p_op], options={"store_states": True})

# ===== Component 2, Task 2 — Wigner functions at t=0 (notebook cell 18) =====
xvec = np.linspace(-4, 4, 200)
pvec = np.linspace(-4, 4, 200)
wnotes = {0: "negative core\n(non-classical)", 1: "interference\nfringes", 2: "all positive\n(classical-like)"}
wxy = {0: (0, 0), 1: (-0.6, 0), 2: (2.1, 0)}
fig, axes = plt.subplots(1, 3, figsize=(14, 4.4))
for i, (ax, (name, psi0)) in enumerate(zip(axes, states.items())):
    W = wigner(psi0, xvec, pvec)
    wmax = np.abs(W).max()
    cf = ax.contourf(xvec, pvec, W, levels=80, cmap="RdBu_r", vmin=-wmax, vmax=wmax)
    ax.set_title(name); ax.set_xlabel("x  (dimensionless)")
    ax.set_ylabel("p  (dimensionless)"); ax.set_aspect("equal")
    fig.colorbar(cf, ax=ax, fraction=0.046, pad=0.04, label="W(x,p)")
    ann(ax, wnotes[i], xy=wxy[i], xytext_frac=(0.03, 0.97), fs=11)
fig.suptitle("Wigner functions at t = 0  (blue = negative = non-classical)", y=1.03)
plt.tight_layout(); savefig("c2_wigner.png")

# ===== Component 2, Task 2 — expectation values vs classical (notebook cell 24) =====
def classical_rhs(t, s):
    x, p = s
    return [p/m, -m*omega**2*x]
enote = {0: "<x>=<p>=0\n(all time)", 1: "interference\norbit", 2: "traces classical\n(Ehrenfest)"}
fig, axes = plt.subplots(1, 3, figsize=(14, 4.6))
for i, (ax, (name, res)) in enumerate(zip(axes, results.items())):
    xq, pq = res.expect[0], res.expect[1]
    x0, p0 = xq[0], pq[0]
    csol = solve_ivp(classical_rhs, (0, T), [x0, p0], t_eval=tlist, rtol=1e-9, atol=1e-9)
    ax.plot(csol.y[0], csol.y[1], "-", color="crimson", lw=3, alpha=0.6, label="classical")
    ax.plot(xq, pq, "--", color="#1f77b4", lw=2, label=r"quantum $\langle\hat x\rangle,\langle\hat p\rangle$")
    ax.plot(x0, p0, "ko", ms=6)
    ax.set_title(name, fontsize=12); ax.set_xlabel("x"); ax.set_ylabel("p")
    ax.set_aspect("equal"); ax.grid(alpha=0.3); ax.legend(fontsize=9, loc="upper right")
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3)
    ann(ax, enote[i], xy=(x0, p0), xytext_frac=(0.03, 0.22), fs=10.5)
fig.suptitle(r"Quantum averages vs. classical orbits", y=1.03)
plt.tight_layout(); savefig("c2_expectation.png")

print("Slide figures written to", OUT)
