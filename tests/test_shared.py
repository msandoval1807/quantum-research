"""The helper modules in shared/, tested directly.

These are the functions every notebook imports, so a regression here is invisible until
someone reads a figure and finds it wrong. Each test checks against a closed-form answer
rather than against the function's own output.
"""
from __future__ import annotations

import numpy as np
import pytest

import oscillator          # provided by the .pth file created during setup (see SETUP.md)


def test_energy_is_the_hamiltonian():
    x, p, m, w = 1.3, -0.7, 2.0, 3.0
    assert oscillator.energy(x, p, m, w) == pytest.approx(
        p ** 2 / (2 * m) + 0.5 * m * w ** 2 * x ** 2, rel=1e-12)


def test_energy_is_vectorised():
    x = np.linspace(-2, 2, 11)
    assert oscillator.energy(x, np.zeros_like(x)).shape == x.shape


def test_hamilton_rhs_is_hamiltons_equations():
    """xdot = dH/dp = p/m and pdot = -dH/dx = -m w^2 x, checked numerically against energy()."""
    x, p, m, w, h = 0.6, 0.4, 1.7, 2.3, 1e-6
    xdot, pdot = oscillator.hamilton_rhs(0.0, [x, p], m, w)
    dH_dp = (oscillator.energy(x, p + h, m, w) - oscillator.energy(x, p - h, m, w)) / (2 * h)
    dH_dx = (oscillator.energy(x + h, p, m, w) - oscillator.energy(x - h, p, m, w)) / (2 * h)
    assert xdot == pytest.approx(dH_dp, rel=1e-6)
    assert pdot == pytest.approx(-dH_dx, rel=1e-6)


def test_analytic_solution_satisfies_the_initial_conditions():
    x0, p0, m, w = 0.9, -0.3, 1.4, 2.1
    x, p = oscillator.analytic_xp(0.0, x0, p0, m, w)
    assert x == pytest.approx(x0) and p == pytest.approx(p0)


def test_analytic_momentum_is_m_times_dx_dt():
    """The classic place to get a sign wrong."""
    x0, p0, m, w, h = 0.9, -0.3, 1.4, 2.1, 1e-6
    t = 0.37
    _, p = oscillator.analytic_xp(t, x0, p0, m, w)
    xp, _ = oscillator.analytic_xp(t + h, x0, p0, m, w)
    xm, _ = oscillator.analytic_xp(t - h, x0, p0, m, w)
    assert p == pytest.approx(m * (xp - xm) / (2 * h), rel=1e-5)


def test_analytic_solution_conserves_energy():
    x0, p0, m, w = 0.9, -0.3, 1.4, 2.1
    t = np.linspace(0, 10, 400)
    x, p = oscillator.analytic_xp(t, x0, p0, m, w)
    E = oscillator.energy(x, p, m, w)
    assert np.ptp(E) < 1e-12


def test_operators_obey_the_canonical_commutator():
    """[x, p] = i*hbar on the subspace the truncation does not touch."""
    pytest.importorskip("qutip")
    N = 40
    _, _, x, p, _ = oscillator.build_operators(N)
    comm = (x * p - p * x).full()
    # [x, p] = i*hbar, so with hbar = 1 the diagonal is exactly 1j. Truncation breaks the
    # identity in the top corner, which is why only the lower half is checked.
    diag = np.diag(comm)[: N // 2]
    assert np.allclose(diag, 1j, atol=1e-10), "[x, p] must equal i*hbar away from the cutoff"


def test_operators_are_hermitian():
    pytest.importorskip("qutip")
    _, _, x, p, H = oscillator.build_operators(20)
    for op, name in ((x, "x"), (p, "p"), (H, "H")):
        assert np.allclose(op.full(), op.full().conj().T, atol=1e-12), f"{name} must be Hermitian"


def test_operator_hamiltonian_gives_the_right_spectrum():
    pytest.importorskip("qutip")
    N = 30
    *_, H = oscillator.build_operators(N)
    got = H.eigenenergies()[:15]
    assert np.max(np.abs(got - (np.arange(15) + 0.5))) < 1e-12


def test_setup_self_check_passes(capsys):
    """The one command SETUP.md tells a new user to run."""
    oscillator.setup(verbose=False)


def test_group_plot_style_imports_and_applies():
    import matplotlib
    matplotlib.use("Agg")
    import group_plot_style
    group_plot_style.apply_group_style()
    import matplotlib.pyplot as plt
    assert plt.rcParams["axes.labelsize"] >= 12, "group style should enlarge axis labels for slides"
