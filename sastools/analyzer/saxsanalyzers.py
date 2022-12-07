"""Implementation of SAXS Analyzer interface."""

import numpy as np

from enums import SAXSStandards


class PrepareStandard:
    """
    Contains methods for preparing the calibration of measured data
    using a standard.
    """

    def __init__(
        self, standard: SAXSStandards = None, q_std_lit: list = None
    ) -> None:
        """
        Select standard for calibration of SAXS data from
        `SAXSStandards` enum. If no standard is given, `q_std_lit`
        values have to be provided directly or calculated from
        `d_std_lit` manually using `calculate_scattering_vector()`.
        """
        self.standard = standard
        self.q_std_lit = q_std_lit

        if self.standard and self.q_std_lit:
            raise ValueError(
                f"Both a standard = '{standard.name}' and a custom q_std_lit = '{q_std_lit}' were given. These arguments are mutually exclusive, please choose only one!"
            )
        elif self.standard == SAXSStandards.CHOLESTERYL_PALMITATE:
            self.calculate_scattering_vector()
        elif self.standard is None and self.q_std_lit:
            pass
        elif self.standard is None and self.q_std_lit is None:
            pass
        else:
            raise NotImplementedError(
                f"SAXS Standard {standard.name} is not yet implemented."
            )

    def calculate_scattering_vector(self, d_std_lit: list = None) -> list:
        """
        Calculate scattering vector `q_std_lit` (nm^-1) for calibration
        from literature lattice plane distance `d_std_lit` (nm).

        Args:
            d_std_lit (float): Lattice plane distance from literature

        Returns:
            float: Scattering vector q_std_lit
        """
        if self.q_std_lit:
            print(
                f"INFO: q_std_lit = {self.q_std_lit} has already been provided or calculated. Passing method call."
            )
            return self.q_std_lit
        elif self.standard == SAXSStandards.CHOLESTERYL_PALMITATE:
            d_std_lit = [5.249824535, 2.624912267, 1.749941512]
            # Reference: D. L. Dorset, Journal of Lipid Research 1987,
            # 28, 993-1005.
        else:
            if d_std_lit is None:
                raise ValueError(
                    "d_std_lit has to be given, as neither a SAXS standard nor q_std_lit have been initialized!"
                )
            elif len(d_std_lit) < 1:
                raise ValueError(
                    f"d_std_lit = {d_std_lit} cannot be an empty list!"
                )

        self.q_std_lit = [(2 * np.pi) / d for d in d_std_lit]
        return self.q_std_lit

    def calculate_linear_regression(self, q_std_meas: list) -> tuple:
        """
        Calculate the linear regression from `q_std_meas` against
        `q_std_lit` using `numpy.polyfit()` and return `slope` and
        `intercept` as a tuple.

        Args:
            q_std_meas (list): List of measured q values for standard

        Returns:
            tuple: Tuple of slope and intercept from linear regression
        """
        slope, intercept = np.polyfit(x=q_std_meas, y=self.q_std_lit, deg=1)
        return (slope, intercept)


class SAXSAnalyzer:
    """Contains methods for analyzing SAXS data."""

    def data_calibration(m: float, x: float, b: float) -> float:
        """
        Calculate linear regression from

        Args:
            m (float): _description_
            x (float): _description_
            b (float): _description_

        Returns:
            float: _description_
        """
        y = m * x + b
        return y

    def calculate_lattice_plane(q: float) -> float:
        d = (2 * np.pi) / q
        return d

    def calculate_lattice_ratio(d: float, d_0: float) -> float:
        d_ratio = d / d_0
        return d_ratio

    # V1 depends on space group
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

    # Space group has to be considered
    def calculate_a_H1(d: float, h: int, k: int) -> float:
        a_H1 = d * np.sqrt((4 / 3) * ((h**2 + k**2 + (h * k))))
        return a_H1

    def calculate_a_V1(d: float, h: int, k: int, l: int) -> float:
        a_V1 = d * (np.sqrt((h**2) + (k**2) + (l**2)))
        return a_V1

    # Specific for space group
    def d_reciprocal(peak_center):
        d_reciprocal = (peak_center) / (2 * np.pi)
        return d_reciprocal

    def sqrt_miller(h, k, l):
        sq_root = np.sqrt(h**2 + k**2 + l**2)
        return sq_root


if __name__ == "__main__":
    test = PrepareStandard(standard=SAXSStandards.CHOLESTERYL_PALMITATE)
    print(test.calculate_linear_regression(q_std_meas=[1, 2, 3]))
