"""Vectorized gradient noise without compiled extension dependencies."""

import numpy as np


def perlin2(points, seed, octaves=3, lacunarity=1.7):
    """Return smooth, seeded 2D noise at an array of (x, y) points."""
    rng = np.random.RandomState(seed)
    permutation = rng.permutation(256)
    angles = rng.uniform(0, 2 * np.pi, 256)
    gradients = np.column_stack((np.cos(angles), np.sin(angles)))
    result = np.zeros(len(points))
    amplitude = frequency = 1.0
    total_amplitude = 0.0
    for _ in range(octaves):
        coords = np.asarray(points) * frequency
        lattice = np.floor(coords).astype(np.int64)
        fraction = coords - lattice
        fade = fraction ** 3 * (fraction * (fraction * 6 - 15) + 10)

        def dot(dx, dy):
            index = permutation[(permutation[(lattice[:, 0] + dx) % 256]
                                 + lattice[:, 1] + dy) % 256]
            offset = fraction - (dx, dy)
            return np.sum(gradients[index] * offset, axis=1)

        bottom = (1 - fade[:, 0]) * dot(0, 0) + fade[:, 0] * dot(1, 0)
        top = (1 - fade[:, 0]) * dot(0, 1) + fade[:, 0] * dot(1, 1)
        result += amplitude * ((1 - fade[:, 1]) * bottom + fade[:, 1] * top)
        total_amplitude += amplitude
        amplitude *= 0.5
        frequency *= lacunarity
    return result / total_amplitude
