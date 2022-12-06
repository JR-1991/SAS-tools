"""Implementation of SAXS Analyzer interface."""


import numpy as np


class SAXSAnalyzer:
    """Contains methods for analyzing SAXS data."""

    def __init__(self) -> None:
        pass

    def calculate_scattering_vector(d: float) -> float:
        q = (2 * np.pi) / (d / 10)
        return q

    def calculate_linear_regression(m: float, x: float, b: float) -> float:
        y = m * x + b
        return y

    def calculate_lattice_plane(q: float) -> float:
        d = (2 * np.pi) / q
        return d

    def calculate_lattice_ratio(d: float, d_0: float) -> float:
        d_ratio = d / d_0
        return d_ratio

    def determine_phase(d_ratios: list) -> bool:
        H1 = [
            (1 / np.sqrt(3)),
            (1 / np.sqrt(4)),
            (1 / np.sqrt(7)),
            (1 / np.sqrt(9)),
        ]
        V1 = [
            (1 / np.sqrt(2)),
            (1 / np.sqrt(3)),
            (1 / np.sqrt(4)),
            (1 / np.sqrt(5)),
        ]
        La = [(1 / 2), (1 / 3), (1 / 4), (1 / 5)]
        
        for i, j in enumerate(d_ratios):
            if (abs(d_ratios[i] - H1[i])) < 0.03:
                return "hexagonal"
            elif (abs(d_ratios[i] - V1[i])) < 0.03:
                return "cubic"
            elif (abs(d_ratios[i] - La[i])) < 0.03:
                return "lamellar"
            else:
                return "indeterminate"

    def calculate_a_H1(d: float, h: int, k: int) -> float:
        a_H1 = d * np.sqrt((4/3)*((h**2 + k**2 + (h * k))))
        return a_H1

    def calculate_a_V1(d: float, h: int, k: int, l: int) -> float:
        a_V1 = d * (np.sqrt((h ** 2) + (k ** 2) + (l ** 2)))
        return a_V1

    def d_reciprocal(peak_center):
        d_reciprocal = ((peak_center)/(2*np.pi))
        return d_reciprocal

    def sqrt_miller(h, k, l):
        sq_root = np.sqrt(h**2 + k**2 + l**2)
        return sq_root    
