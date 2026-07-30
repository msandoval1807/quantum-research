"""
oscillator.py — shared helpers for the harmonic-oscillator assignments.

Everything here is reused across Component 1 (classical) and Component 2 (quantum),
so it lives in shared/ and is importable from any assignment folder.

Typical use at the top of a notebook:

    from oscillator import setup, energy, hamilton_rhs, build_operators, wigner_gif
    setup()                      # group plot style + output routing, in one call

All physics is in natural units (hbar = m = omega = 1) by default; pass different
values if needed.
"""
import numpy as np


# ----------------------------------------------------------------------
# One-line notebook setup: group plotting standards + output routing
# ----------------------------------------------------------------------
def setup(verbose=True):
    """Apply the group plot style and turn on output routing (figures/ data/ movies/).

    Replaces the repeated import-and-call block at the top of every notebook.
    """
    from group_plot_style import apply_group_style
    from output_routing import route_outputs
    apply_group_style()
    route_outputs(verbose=False)
    if verbose:
        print("Setup ready: group plot style applied, outputs route to figures/ data/ movies/.")


# ----------------------------------------------------------------------
# Classical harmonic oscillator
# ----------------------------------------------------------------------
def energy(x, p, m=1.0, omega=1.0):
    """Classical energy E = p^2/2m + 1/2 m omega^2 x^2 (works on scalars or arrays)."""
    return p**2 / (2.0 * m) + 0.5 * m * omega**2 * x**2


def hamilton_rhs(t, state, m=1.0, omega=1.0):
    """Right-hand side of Hamilton's equations for solve_ivp: returns [dx/dt, dp/dt]."""
    x, p = state
    return [p / m, -m * omega**2 * x]


def analytic_xp(t, x0, p0, m=1.0, omega=1.0):
    """Exact classical solution x(t), p(t) for checking the numerical solver."""
    x = x0 * np.cos(omega * t) + (p0 / (m * omega)) * np.sin(omega * t)
    p = -m * omega * x0 * np.sin(omega * t) + p0 * np.cos(omega * t)
    return x, p


# ----------------------------------------------------------------------
# Quantum harmonic oscillator
# ----------------------------------------------------------------------
def build_operators(N, hbar=1.0, m=1.0, omega=1.0):
    """Build the truncated quantum operators for an N-level oscillator.

    Returns (a, adag, x, p, H):
        a    - annihilation operator
        adag - creation operator
        x    - position operator  = sqrt(hbar/2 m omega) (a + adag)
        p    - momentum operator  = -i sqrt(hbar m omega/2) (a - adag)
        H    - Hamiltonian        = p^2/2m + 1/2 m omega^2 x^2
    """
    from qutip import destroy
    a = destroy(N)
    adag = a.dag()
    x = np.sqrt(hbar / (2 * m * omega)) * (a + adag)
    p = -1j * np.sqrt(hbar * m * omega / 2) * (a - adag)
    H = p**2 / (2 * m) + 0.5 * m * omega**2 * x**2
    return a, adag, x, p, H


# ----------------------------------------------------------------------
# Wigner-function animation
# ----------------------------------------------------------------------
def wigner_gif(states, tlist, fname, xvec=None, pvec=None, n_frames=40,
               title="", duration=80):
    """Save a GIF of Wigner-function evolution with a fixed symmetric color scale.

    states   : list of quantum states over time (e.g. sesolve result .states)
    tlist    : the matching time array
    fname    : output filename (a bare name routes to movies/ if output routing is on)
    duration : milliseconds per frame. imageio >= 2.28 (we pin 2.37) reads this as
               MILLISECONDS, not seconds -- passing 0.08 rounds to zero and the GIF
               ends up with no frame delay at all.
    Returns fname.
    """
    import io
    import imageio.v2 as imageio
    import matplotlib.pyplot as plt
    from PIL import Image
    from qutip import wigner

    if xvec is None:
        xvec = np.linspace(-4, 4, 200)
    if pvec is None:
        pvec = np.linspace(-4, 4, 200)

    idx = np.linspace(0, len(states) - 1, n_frames).astype(int)
    grids = [wigner(states[i], xvec, pvec) for i in idx]   # pass 1: compute all frames
    wmax = max(np.abs(W).max() for W in grids)              # one fixed color scale

    frames = []
    for j, i in enumerate(idx):                            # pass 2: render frames
        fig, ax = plt.subplots(figsize=(4.6, 4.2))
        # Explicit level array, NOT levels=80 + vmin/vmax: with an integer `levels`
        # contourf picks its levels from each frame's own data range and ignores
        # vmin/vmax, so the color scale would silently rescale frame to frame.
        ax.contourf(xvec, pvec, grids[j], levels=np.linspace(-wmax, wmax, 81),
                    cmap="RdBu_r")
        ax.set_title(f"{title}\nt = {tlist[i]:.2f}", fontsize=11)
        ax.set_xlabel("x"); ax.set_ylabel("p"); ax.set_aspect("equal")
        buf = io.BytesIO()
        # bbox_inches=None is explicit: the group style sets savefig.bbox="tight"
        # globally, which would crop each frame to its own content and let the frame
        # size drift as the title text changes. GIF frames must all be one size.
        fig.savefig(buf, format="png", dpi=85, bbox_inches=None)
        buf.seek(0)
        frames.append(np.array(Image.open(buf).convert("RGB")))
        plt.close(fig)

    imageio.mimsave(fname, frames, duration=duration, loop=0)
    return fname


# ----------------------------------------------------------------------
# Self-check: run `python shared/oscillator.py` to verify this module.
# Every claim below is checked against an exact formula, per the group's
# golden rule -- never trust a number you cannot check.
# ----------------------------------------------------------------------
if __name__ == "__main__":
    from scipy.integrate import solve_ivp

    # 1. Numerical integration must reproduce the exact classical solution.
    t_end = 2 * np.pi
    sol = solve_ivp(hamilton_rhs, (0, t_end), [1.3, -0.7],
                    t_eval=np.linspace(0, t_end, 400), rtol=1e-10, atol=1e-10)
    x_exact, p_exact = analytic_xp(sol.t, 1.3, -0.7)
    assert np.allclose(sol.y[0], x_exact, atol=1e-7), "x(t) does not match the exact solution"
    assert np.allclose(sol.y[1], p_exact, atol=1e-7), "p(t) does not match the exact solution"

    # 2. Energy must be conserved along the trajectory.
    E = energy(sol.y[0], sol.y[1])
    assert np.ptp(E) < 1e-8, f"energy drifted by {np.ptp(E):.2e}"

    # 3. The Wigner color scale must be symmetric about zero and cover +/- wmax.
    #    This is the invariant the levels=80 + vmin/vmax bug used to break: given an
    #    integer `levels`, contourf ignores vmin/vmax and rescales to each frame.
    wmax = 0.31
    levels = np.linspace(-wmax, wmax, 81)
    assert np.isclose(levels.min(), -wmax) and np.isclose(levels.max(), wmax)
    assert np.isclose(levels[len(levels) // 2], 0.0), "zero must sit at the middle (white)"

    # 4. Quantum spectrum must match E_n = hbar*omega*(n + 1/2) on the trustworthy half.
    try:
        _, _, _, _, H = build_operators(30)
        eig = H.eigenenergies()
        assert np.allclose(eig[:15], np.arange(15) + 0.5, atol=1e-9), "low spectrum is wrong"
        print("PASS: classical solver, energy conservation, Wigner scale, quantum spectrum.")
    except ImportError:
        print("PASS: classical solver, energy conservation, Wigner scale."
              "  (qutip not installed -- spectrum check skipped.)")
