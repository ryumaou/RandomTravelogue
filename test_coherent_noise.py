import unittest

import numpy as np

from coherent_noise import perlin2


class NoiseTests(unittest.TestCase):
    def test_repeatable_and_seeded(self):
        points = np.random.RandomState(0).uniform(-2, 2, (100, 2))
        values = perlin2(points, seed=42)
        np.testing.assert_array_equal(values, perlin2(points, seed=42))
        self.assertFalse(np.allclose(values, perlin2(points, seed=43)))
        self.assertTrue(np.isfinite(values).all())
        self.assertGreater(np.std(values), 0.01)

    def test_continuity_across_lattice_boundaries(self):
        points = np.array([[-1., .3], [0., .3], [1., .3]])
        left = perlin2(points - [1e-7, 0], seed=42)
        right = perlin2(points + [1e-7, 0], seed=42)
        np.testing.assert_allclose(left, right, atol=1e-5, rtol=0)


if __name__ == "__main__":
    unittest.main()
