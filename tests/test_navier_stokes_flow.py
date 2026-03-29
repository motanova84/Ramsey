#!/usr/bin/env python3
"""
tests/test_navier_stokes_flow.py
Tests for network/navier_stokes_flow.py — SuperfluidFlow (Brecha B)

Validates:
1. Initialization and metadata
2. Velocity field structure (cyclic permutation matrix)
3. det(V) = 1 (incompressible flow / Haar measure preservation)
4. Unitarity of the velocity matrix (V V^T = I)
5. Norm preservation after step (isometry in L²)
6. Ramsey connection: 7-node cycle corresponds to C₇ primes
"""

import unittest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from network.navier_stokes_flow import SuperfluidFlow


class TestSuperfluidFlowInit(unittest.TestCase):
    """Test initialization of SuperfluidFlow."""

    def setUp(self):
        self.flow = SuperfluidFlow()

    def test_default_nodes(self):
        self.assertEqual(self.flow.n, 7)

    def test_default_dt(self):
        expected_dt = 1.0 / 141700.1
        self.assertAlmostEqual(self.flow.dt, expected_dt, places=15)

    def test_velocity_field_shape(self):
        self.assertEqual(self.flow.velocity_field.shape, (7, 7))

    def test_custom_nodes(self):
        flow = SuperfluidFlow(nodes=5, f0=100.0)
        self.assertEqual(flow.n, 5)
        self.assertAlmostEqual(flow.dt, 0.01, places=10)
        self.assertEqual(flow.velocity_field.shape, (5, 5))

    def test_metadata(self):
        from network.navier_stokes_flow import (
            __author__, __architecture__, __license__, __f0__
        )
        self.assertIn("JMMB", __author__)
        self.assertEqual(__architecture__, "QCAL ∞³")
        self.assertEqual(__f0__, 141.7001)


class TestVelocityFieldStructure(unittest.TestCase):
    """Test the cyclic permutation structure of the velocity field."""

    def setUp(self):
        self.flow = SuperfluidFlow()

    def test_is_binary_matrix(self):
        """Each entry is 0 or 1."""
        for val in self.flow.velocity_field.flat:
            self.assertIn(val, [0.0, 1.0])

    def test_each_row_sums_to_one(self):
        """Row-stochastic: each row has exactly one 1."""
        for row in self.flow.velocity_field:
            self.assertAlmostEqual(row.sum(), 1.0, places=12)

    def test_each_col_sums_to_one(self):
        """Column-stochastic: each column has exactly one 1."""
        for col in self.flow.velocity_field.T:
            self.assertAlmostEqual(col.sum(), 1.0, places=12)

    def test_cyclic_shift(self):
        """V equals np.roll(I, 1, axis=0)."""
        expected = np.roll(np.eye(7), 1, axis=0)
        np.testing.assert_array_equal(self.flow.velocity_field, expected)


class TestIncompressibility(unittest.TestCase):
    """Test det(V) = 1 — Haar measure preservation / incompressible flow."""

    def test_det_equals_one_default(self):
        flow = SuperfluidFlow()
        self.assertAlmostEqual(abs(flow.det), 1.0, places=10)

    def test_det_equals_one_custom(self):
        for n in [3, 5, 7, 9]:
            flow = SuperfluidFlow(nodes=n)
            self.assertAlmostEqual(
                abs(flow.det), 1.0, places=10,
                msg=f"det ≠ 1 for n={n}"
            )


class TestUnitarity(unittest.TestCase):
    """Test V V^T = I (unitary operator — Brecha B closure)."""

    def test_is_unitary_default(self):
        flow = SuperfluidFlow()
        self.assertTrue(flow.is_unitary())

    def test_v_vt_equals_identity(self):
        flow = SuperfluidFlow()
        product = np.dot(flow.velocity_field, flow.velocity_field.T)
        np.testing.assert_allclose(product, np.eye(7), atol=1e-10)

    def test_vt_v_equals_identity(self):
        flow = SuperfluidFlow()
        product = np.dot(flow.velocity_field.T, flow.velocity_field)
        np.testing.assert_allclose(product, np.eye(7), atol=1e-10)


class TestNormPreservation(unittest.TestCase):
    """Test ‖step(ψ)‖ = ‖ψ‖ — isometry in L² (core of Brecha B)."""

    def setUp(self):
        self.flow = SuperfluidFlow()
        self.rng = np.random.default_rng(seed=42)

    def test_norm_preserved_unit_vector(self):
        psi = np.zeros(7)
        psi[0] = 1.0
        result = self.flow.step(psi)
        self.assertAlmostEqual(
            self.flow.norm(result), self.flow.norm(psi), places=12
        )

    def test_norm_preserved_random_vector(self):
        for _ in range(10):
            psi = self.rng.standard_normal(7)
            result = self.flow.step(psi)
            self.assertAlmostEqual(
                self.flow.norm(result), self.flow.norm(psi), places=10
            )

    def test_norm_preserved_after_multiple_steps(self):
        """After n full steps (one complete cycle), state is unchanged."""
        psi = self.rng.standard_normal(7)
        original_norm = self.flow.norm(psi)
        state = psi.copy()
        for _ in range(7):
            state = self.flow.step(state)
        # After 7 cyclic shifts, the state returns to its original value.
        np.testing.assert_allclose(state, psi, atol=1e-10)
        self.assertAlmostEqual(self.flow.norm(state), original_norm, places=10)

    def test_step_output_shape(self):
        psi = np.ones(7)
        result = self.flow.step(psi)
        self.assertEqual(result.shape, (7,))


class TestRamseyConnection(unittest.TestCase):
    """Test the C₇ cycle structure connecting to the 7 primes {2,3,5,7,11,13,17}."""

    def test_seven_nodes(self):
        """C₇ has exactly 7 nodes — one per prime."""
        flow = SuperfluidFlow(nodes=7)
        self.assertEqual(flow.n, 7)

    def test_cyclic_orbit_length(self):
        """A single basis vector returns to itself after exactly 7 steps."""
        flow = SuperfluidFlow(nodes=7)
        e0 = np.zeros(7)
        e0[0] = 1.0
        state = e0.copy()
        for step_idx in range(1, 8):
            state = flow.step(state)
            if step_idx < 7:
                # Not yet back
                self.assertFalse(np.allclose(state, e0))
        # After 7 steps exactly back to start
        np.testing.assert_allclose(state, e0, atol=1e-12)

    def test_frequency_sampling_rate(self):
        """dt = 1/f₀ matches the quantum integrator sampling period."""
        f0 = 141700.1
        flow = SuperfluidFlow(nodes=7, f0=f0)
        self.assertAlmostEqual(flow.dt * f0, 1.0, places=10)


if __name__ == "__main__":
    unittest.main(verbosity=2)
