"""Physics that must hold, recomputed from scratch.

Nothing here reads a result out of a notebook and compares it to itself. Each test either
derives the quantity independently or checks it against a closed-form answer, which is the
project's working rule: never trust a numerical result you cannot check against something
external.

Derivatives are taken NUMERICALLY on purpose. An earlier version of this audit hand-derived
dU/dphi, got a sign wrong, and reported four false failures against correct code.
"""
from __future__ import annotations

import numpy as np
import pytest
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

from conftest import EC, EJ, EL, PHI_EXT

H = 1e-6


def U(phi):
    """The fluxonium potential in scqubits' convention, written out here so the test is
    independent of the library; test_matches_library below checks they agree."""
    return 0.5 * EL * phi ** 2 - EJ * np.cos(phi + PHI_EXT)


def dU(phi):
    return (U(phi + H) - U(phi - H)) / (2 * H)


def d2U(phi):
    return (U(phi + H) - 2 * U(phi) + U(phi - H)) / H ** 2


# --------------------------------------------------------------- the parameter mapping
def test_mass_maps_to_charging_energy():
    """m = 1/(8 E_C) is exactly the value that turns p^2/2m into 4 E_C n^2."""
    m = 1.0 / (8 * EC)
    assert 1.0 / (2 * m) == pytest.approx(4 * EC, rel=1e-12)


def test_frequency_maps_to_inductive_energy():
    """omega = sqrt(8 E_C E_L) is exactly the value that turns 1/2 m omega^2 x^2 into 1/2 E_L phi^2."""
    m, w = 1.0 / (8 * EC), np.sqrt(8 * EC * EL)
    assert m * w * w == pytest.approx(EL, rel=1e-12)


# --------------------------------------------------------------- the double well
def test_potential_matches_the_installed_library(fluxonium):
    """Our written-out potential is the one scqubits actually solves."""
    phis = np.linspace(-6, 6, 601)
    assert np.max(np.abs(fluxonium.potential(phis) - U(phis))) < 1e-12


def test_well_minimum_is_near_2_85():
    assert brentq(dU, 1.0, 4.0) == pytest.approx(2.85, abs=5e-3)


def test_wells_are_minima_and_origin_is_a_barrier():
    """The whole coordinate-convention bug came from getting this backwards."""
    phi_min = brentq(dU, 1.0, 4.0)
    assert d2U(phi_min) > 0, "the well must be a minimum"
    assert d2U(0.0) < 0, "phi = 0 must be the barrier top, not a well"


def test_barrier_height():
    assert U(0) - U(brentq(dU, 1.0, 4.0)) == pytest.approx(7.76, abs=5e-3)


def test_double_well_is_symmetric():
    phi_min = brentq(dU, 1.0, 4.0)
    assert U(-phi_min) == pytest.approx(U(phi_min), abs=1e-12)


def test_tunnelling_doublet(fluxonium):
    """Two nearly degenerate levels far below the next one: the signature of the double well."""
    ev = fluxonium.eigenvals(evals_count=4)
    gap01, gap12 = ev[1] - ev[0], ev[2] - ev[1]
    assert gap01 == pytest.approx(0.134, abs=5e-3)
    assert gap12 / gap01 > 20, "the doublet must sit well below the next level"


# --------------------------------------------------------------- the handout's mapping
def test_handout_mapping_is_exact_only_at_zero_flux():
    """The handout's classical form centres both terms on x=0; the fluxonium does not.

    This is a real error in the assignment, kept as a test so it cannot be quietly
    'fixed' back to the handout's version. See Findings_and_Corrections.md.
    """
    xs = np.linspace(-6, 6, 1201)
    m, w = 1.0 / (8 * EC), np.sqrt(8 * EC * EL)
    handout = 0.5 * m * w ** 2 * xs ** 2 - EJ * np.cos(xs)

    at_zero_flux = 0.5 * EL * xs ** 2 - EJ * np.cos(xs + 0.0)
    assert np.max(np.abs(handout - at_zero_flux)) < 1e-12, "should be exact at zero flux"

    assert np.max(np.abs(handout - U(xs))) == pytest.approx(2 * EJ, abs=1e-9), (
        "at half flux the two forms differ by exactly 2*E_J")


def test_our_convention_reproduces_the_potential_exactly():
    """x = phi with V0 = -E_J is what the notebooks use, and it is exact."""
    xs = np.linspace(-6, 6, 1201)
    m, w = 1.0 / (8 * EC), np.sqrt(8 * EC * EL)
    ours = 0.5 * m * w ** 2 * xs ** 2 - (-EJ) * np.cos(xs)
    assert np.max(np.abs(ours - U(xs))) < 1e-12


# --------------------------------------------------------------- classical dynamics
def test_solver_matches_the_exact_solution():
    m = w = 1.0
    x0, p0 = 1.0, 0.5
    T = 2 * np.pi / w
    sol = solve_ivp(lambda t, y: [y[1] / m, -m * w * w * y[0]], (0, 4 * T), [x0, p0],
                    t_eval=np.linspace(0, 4 * T, 2000), rtol=1e-10, atol=1e-10)
    A = np.hypot(x0, p0 / (m * w))
    ph = np.arctan2(-p0 / (m * w), x0)
    xe = A * np.cos(w * sol.t + ph)
    pe = -m * w * A * np.sin(w * sol.t + ph)
    assert np.max(np.hypot(sol.y[0] - xe, sol.y[1] - pe)) < 1e-7


def test_energy_is_conserved():
    m = w = 1.0
    sol = solve_ivp(lambda t, y: [y[1] / m, -m * w * w * y[0]], (0, 8 * np.pi), [1.0, 0.5],
                    t_eval=np.linspace(0, 8 * np.pi, 2000), rtol=1e-10, atol=1e-10)
    E = sol.y[1] ** 2 / (2 * m) + 0.5 * m * w * w * sol.y[0] ** 2
    assert np.max(np.abs(E - E[0])) < 1e-7


def test_cosine_oscillator_small_amplitude_frequency():
    """At small x the cosine stiffens the spring: omega_eff = sqrt(omega^2 + V0 k^2 / m)."""
    m = w = V0 = k = 1.0
    sol = solve_ivp(lambda t, y: [y[1] / m, -m * w * w * y[0] - V0 * k * np.sin(k * y[0])],
                    (0, 20), [1e-3, 0.0], t_eval=np.linspace(0, 20, 20001),
                    rtol=1e-11, atol=1e-13)
    zc = np.where(np.diff(np.sign(sol.y[0])))[0]
    period = 2 * np.mean(np.diff(sol.t[zc]))
    assert 2 * np.pi / period == pytest.approx(np.sqrt(2), abs=2e-3)


def test_coupling_changes_the_poincare_crossing_direction():
    """xdot2 = p2/m + lambda*p1 does not share the sign of p2 once the coupling is on.

    The handout suggests filtering on p2 > 0; that mis-signs some crossings. Kept as a
    test so the surface-of-section condition cannot regress to the handout's version.
    """
    m, lam, p1, p2 = 1.0, 0.3, 0.4, -0.1
    assert np.sign(p2 / m + lam * p1) != np.sign(p2)


# --------------------------------------------------------------- quantum spectrum
def test_harmonic_spectrum_matches_the_closed_form():
    qt = pytest.importorskip("qutip")
    N, hbar, m, w = 30, 1.0, 1.0, 1.0
    a = qt.destroy(N)
    x = np.sqrt(hbar / (2 * m * w)) * (a + a.dag())
    p = -1j * np.sqrt(hbar * m * w / 2) * (a - a.dag())
    H_op = (p * p) / (2 * m) + 0.5 * m * w ** 2 * (x * x)
    got = H_op.eigenenergies()[:15]
    exact = hbar * w * (np.arange(15) + 0.5)
    assert np.max(np.abs(got - exact)) < 1e-12


def test_only_the_lower_half_of_the_spectrum_is_trustworthy():
    """Truncation puts one spurious eigenvalue at (N-1)/2; sorting then displaces
    everything above it by exactly one rung. So the error is a plateau at 1.0, not a drift."""
    qt = pytest.importorskip("qutip")
    N = 30
    a = qt.destroy(N)
    x = np.sqrt(0.5) * (a + a.dag())
    p = -1j * np.sqrt(0.5) * (a - a.dag())
    ev = ((p * p) / 2 + 0.5 * (x * x)).eigenenergies()
    exact = np.arange(N) + 0.5
    err = np.abs(ev - exact)
    cutoff = int(np.ceil((N - 1) / 2))
    assert np.max(err[:cutoff]) < 1e-10, "the low half must be exact"
    assert err[-1] == pytest.approx(1.0, abs=1e-6), "the top must be off by exactly one rung"
