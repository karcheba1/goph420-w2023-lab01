import unittest

import numpy as np

from fem_1d_heat.geometry import (
        global_to_local,
)


class TestGlobalToLocalValues(unittest.TestCase):
    
    def setUp(self):
        self.z = 3.0
        self.z_e = np.array([0, 6])

    def test_value(self):
        s_exp = 0.5
        s_act = global_to_local(self.z, self.z_e)
        self.assertAlmostEqual(s_exp, s_act)
        self.assertIsInstance(s_act, float)


if __name__ == "__main__":
    unittest.main()

